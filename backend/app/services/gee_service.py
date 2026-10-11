"""Google Earth Engine bridge backed by actual planetary datasets.

Never present an ESRI/RainViewer map as a processed GEE index. Metrics and tiles
require server-side credentials; API errors remain explicit.
"""
import datetime as dt
import logging
import time
from typing import Dict, Any, Optional

from fastapi import HTTPException

from app.services.gee_processing import EarthEngineProcessor, DATASETS, validate_window
from app.services.gee_presets import INDEX_REGISTRY

LOG = logging.getLogger(__name__)


class GoogleEarthEngineBridge:
    _tile_cache: Dict[tuple, tuple] = {}
    _metrics_cache: Dict[str, tuple] = {}
    TTL = 900  # 15 minutes: Earth Engine tile tokens expire; do not cache indefinitely.

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        return EarthEngineProcessor.status()

    @classmethod
    def configure(cls, project_id: Optional[str] = None, sa_key: Optional[str] = None) -> Dict[str, Any]:
        """Project selection is development-only at the API layer; keys are server secrets."""
        if sa_key:
            raise HTTPException(status_code=400, detail="Configuração de credenciais GEE por API não suportada.")
        cls._tile_cache.clear()
        cls._metrics_cache.clear()
        EarthEngineProcessor.initialize(project=project_id, force=True)
        return cls.get_status()

    @classmethod
    def compute_index_tile(
        cls, index: str, district_id: str = "manhica",
        start_date: Optional[str] = None, end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        now = dt.datetime.now(dt.timezone.utc).date() + dt.timedelta(days=1)
        final = end_date or now.isoformat()
        begin = start_date or (dt.date.fromisoformat(final) - dt.timedelta(days=30 if index == "flood_sar" else 120)).isoformat()
        validate_window(begin, final)
        if index not in DATASETS:
            raise HTTPException(status_code=422, detail="Índice não suportado.")
        key = (index, district_id, begin, final, EarthEngineProcessor._project)
        cached = cls._tile_cache.get(key)
        if cached and time.monotonic() - cached[0] < cls.TTL:
            return cached[1]
        result = EarthEngineProcessor.compute(index, district_id, begin, final)
        cls._tile_cache[key] = (time.monotonic(), result)
        return result

    @classmethod
    def get_district_satellite_metrics(cls, district_id: str) -> Dict[str, Any]:
        """Measured EO-derived metrics, each with explicit source and observation date.

        Uses native-resolution reductions with bestEffort; area estimates are
        preliminary and must not be used for real emergency planning without QA.
        """
        cached = cls._metrics_cache.get(district_id)
        if cached and time.monotonic() - cached[0] < cls.TTL:
            return cached[1]

        processor = EarthEngineProcessor
        ee = processor.ee()
        region = processor.region(district_id)
        today = dt.datetime.now(dt.timezone.utc).date() + dt.timedelta(days=1)
        start = (today - dt.timedelta(days=120)).isoformat()
        end = today.isoformat()
        values = {
            "district_id": district_id,
            "data_mode": "ESTIMATED",
            "data_source": "Google Earth Engine — processamento de observações orbitais e estimativas derivadas",
            "ndvi_mean": None,
            "ndwi_water_extent_sqkm": None,
            "sar_flood_inundated_sqkm": None,
            "dem_elevation_mean_m": None,
            "dem_slope_mean_deg": None,
            "rainfall_7d_mm": None,
            "dates": {},
            "methods": {},
            "warnings": [],
        }

        def scalar(image, band: str, reducer, scale: int):
            data = image.reduceRegion(
                reducer=reducer, geometry=region, scale=scale,
                bestEffort=True, maxPixels=1e8, tileScale=4
            ).getInfo()
            value = data.get(band)
            return None if value is None else round(float(value), 2)

        try:
            ndvi, collection = processor.sentinel2_index("ndvi", region, start, end)
            ndwi, _ = processor.sentinel2_index("ndwi", region, start, end)
            values["ndvi_mean"] = scalar(ndvi, "ndvi", ee.Reducer.mean(), 20)
            water_km2 = ee.Image.pixelArea().updateMask(ndwi.gt(0.1)).divide(1e6).rename("water_km2")
            values["ndwi_water_extent_sqkm"] = scalar(water_km2, "water_km2", ee.Reducer.sum(), 20)
            values["dates"]["sentinel2"] = ee.Date(collection.aggregate_max("system:time_start")).format("YYYY-MM-dd").getInfo()
            values["methods"]["ndwi"] = "NDWI > 0.1; área indicativa, não delimitação validada"
        except HTTPException as exc:
            if exc.status_code == 503:
                raise
            values["warnings"].append("Sem cenas Sentinel-2 utilizáveis na janela.")
        except Exception as exc:
            LOG.warning("S2 metrics unavailable: %s", type(exc).__name__)
            values["warnings"].append("Não foi possível calcular índices Sentinel-2.")

        try:
            dem = processor.terrain(region, "elevation")
            slope = processor.terrain(region, "slope")
            values["dem_elevation_mean_m"] = scalar(dem, "elevation", ee.Reducer.mean(), 30)
            values["dem_slope_mean_deg"] = scalar(slope, "slope", ee.Reducer.mean(), 30)
            values["methods"]["dem"] = "Copernicus DEM GLO30; modelo estático de superfície"
        except Exception as exc:
            LOG.warning("DEM metrics unavailable: %s", type(exc).__name__)
            values["warnings"].append("Modelo de elevação indisponível.")

        try:
            candidates, sar_images, orbit = processor.sar_candidate(
                region, (today - dt.timedelta(days=30)).isoformat(), end
            )
            area_km2 = ee.Image.pixelArea().updateMask(candidates).divide(1e6).rename("flood_km2")
            values["sar_flood_inundated_sqkm"] = scalar(area_km2, "flood_km2", ee.Reducer.sum(), 30)
            values["dates"]["sentinel1"] = ee.Date(sar_images.aggregate_max("system:time_start")).format("YYYY-MM-dd").getInfo()
            values["methods"]["sar"] = "VV change > 3 dB, VV <-15 dB, slope <5°, JRC water occurrence <80%; candidat(o)s, não cheias confirmadas"
            values["methods"]["sar_orbit"] = orbit
        except Exception as exc:
            LOG.warning("S1 metrics unavailable: %s", type(exc).__name__)
            values["warnings"].append("Sem pares Sentinel-1 adequados para detecção preliminar.")

        try:
            source = ee.ImageCollection(DATASETS["precipitation"]).filterBounds(region).filterDate(start, end)
            if source.size().getInfo() > 0:
                latest_millis = source.aggregate_max("system:time_start").getInfo()
                latest = dt.datetime.fromtimestamp(latest_millis / 1000, tz=dt.timezone.utc).date()
                rain_start = (latest - dt.timedelta(days=6)).isoformat()
                rain_end = (latest + dt.timedelta(days=1)).isoformat()
                rain, _ = processor.chirps(region, rain_start, rain_end)
                values["rainfall_7d_mm"] = scalar(rain, "precipitation", ee.Reducer.mean(), 5566)
                values["dates"]["chirps"] = latest.isoformat()
                values["methods"]["rainfall"] = f"CHIRPS 7 dias encerrados em {latest.isoformat()}, não previsão nem precipitação de hoje"
            else:
                values["warnings"].append("CHIRPS sem dados publicados na janela pesquisada.")
        except Exception as exc:
            LOG.warning("CHIRPS metrics unavailable: %s", type(exc).__name__)
            values["warnings"].append("Precipitação CHIRPS indisponível.")

        values["acquisition_date"] = values["dates"].get("sentinel2")
        values["ndvi_status"] = "Índice médio derivado de cenas Sentinel-2, sujeito a nuvens"
        values["satellite_sensor"] = "Sentinel-2 / Sentinel-1 / Copernicus DEM / CHIRPS (segundo disponibilidade)"
        if all(values[k] is None for k in ("ndvi_mean", "dem_elevation_mean_m", "rainfall_7d_mm")):
            raise HTTPException(status_code=502, detail="Nenhuma métrica GEE foi calculada com sucesso.")
        cls._metrics_cache[district_id] = (time.monotonic(), values)
        return values
