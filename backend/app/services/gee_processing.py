"""Google Earth Engine processing for CLYMEX AI.

All scientific tiles come from ee.Image computations, clipped to GeoMoz
admin polygons. No basemap URLs or synthetic values are returned as satellite
observations. Flood output is a SAR change *candidate*, not validated flooding.
"""
import datetime as dt
import json
import logging
import os
from functools import lru_cache
from typing import Any, Optional

from fastapi import HTTPException
from app.services.administrative_boundaries import districts_geojson
from app.services.gee_presets import INDEX_REGISTRY

LOG = logging.getLogger(__name__)

DATASETS = {
    "ndvi": "COPERNICUS/S2_SR_HARMONIZED",
    "ndwi": "COPERNICUS/S2_SR_HARMONIZED",
    "mndwi": "COPERNICUS/S2_SR_HARMONIZED",
    "flood_sar": "COPERNICUS/S1_GRD",
    "elevation": "COPERNICUS/DEM/GLO30",
    "slope": "COPERNICUS/DEM/GLO30",
    "precipitation": "UCSB-CHG/CHIRPS/DAILY",
}
SCOPES = ["https://www.googleapis.com/auth/earthengine", "https://www.googleapis.com/auth/cloud-platform"]


def validate_window(start_date: str, end_date: str, max_days: int = 366):
    try:
        start = dt.date.fromisoformat(start_date)
        end = dt.date.fromisoformat(end_date)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail="Datas devem usar o formato YYYY-MM-DD.") from exc
    if end <= start or (end - start).days > max_days:
        raise HTTPException(status_code=422, detail="Janela temporal inválida ou demasiado longa.")
    if end > dt.datetime.now(dt.timezone.utc).date() + dt.timedelta(days=1):
        raise HTTPException(status_code=422, detail="Não é permitido processamento satelital de datas futuras.")
    return start, end


@lru_cache(maxsize=32)
def district_geometry(district_id: str) -> dict:
    """GeoMoz-based polygon; missing districts are rejected, never substituted."""
    features = districts_geojson(focus_only=False)["features"]
    for feature in features:
        if feature["id"] == district_id:
            if feature.get("geometry") and feature["geometry"].get("coordinates"):
                return feature["geometry"]
            break
    # Maputo City can be province-equivalent; GeoMoz adapter handles this case.
    if district_id == "maputo_city":
        for feature in districts_geojson(focus_only=True)["features"]:
            if feature["id"] == district_id and feature.get("geometry"):
                return feature["geometry"]
    raise HTTPException(status_code=404, detail="Distrito não encontrado no GeoMoz.")


def credentials_and_project(project_override: Optional[str] = None):
    """Use server-only secrets or ADC; never receive raw keys from requests."""
    project = project_override or os.environ.get("GEE_PROJECT_ID", "geoprocessamento-426809")
    path = os.environ.get("GEE_PRIVATE_KEY_PATH")
    raw = os.environ.get("GEE_SERVICE_ACCOUNT_JSON")
    from google.oauth2 import service_account
    if raw:
        return service_account.Credentials.from_service_account_info(json.loads(raw), scopes=SCOPES), project, "service_account"
    if path:
        return service_account.Credentials.from_service_account_file(path, scopes=SCOPES), project, "service_account"
    import google.auth
    creds, _ = google.auth.default(scopes=SCOPES)
    return creds, project, "application_default_credentials"


class EarthEngineProcessor:
    _ee = None
    _project: Optional[str] = None
    _auth_type = "unconfigured"
    _error: Optional[str] = None

    @classmethod
    def initialize(cls, project: Optional[str] = None, force: bool = False):
        if cls._ee is not None and not force and (not project or project == cls._project):
            return True
        cls._ee = None
        try:
            import ee
            credentials, selected_project, auth_type = credentials_and_project(project)
            ee.Initialize(credentials=credentials, project=selected_project)
            # A real remote call is required; project ID alone does not prove connectivity.
            ee.Number(1).getInfo()
            cls._ee, cls._project, cls._auth_type, cls._error = ee, selected_project, auth_type, None
            return True
        except Exception as exc:
            cls._project = project or os.environ.get("GEE_PROJECT_ID", "geoprocessamento-426809")
            cls._auth_type = "unconfigured"
            cls._error = type(exc).__name__
            LOG.warning("Earth Engine unavailable: %s", type(exc).__name__)
            return False

    @classmethod
    def status(cls):
        connected = cls.initialize()
        return {
            "connected": connected,
            "project_id": cls._project,
            "auth_type": cls._auth_type,
            "status": "AUTHENTICATED" if connected else "UNCONFIGURED",
            "message": "Earth Engine autenticado e verificado." if connected else "Credenciais GEE ou acesso ao projecto indisponíveis.",
            "error_type": cls._error,
            "indices": list(INDEX_REGISTRY),
            "index_catalog": INDEX_REGISTRY,
        }

    @classmethod
    def ee(cls):
        if not cls.initialize():
            raise HTTPException(status_code=503, detail="Google Earth Engine não autenticado; configure credenciais no servidor.")
        return cls._ee

    @classmethod
    def region(cls, district_id: str):
        ee = cls.ee()
        return ee.Geometry(district_geometry(district_id))

    @classmethod
    def s2_images(cls, region, start, end):
        ee = cls.ee()
        images = (ee.ImageCollection(DATASETS["ndvi"]).filterBounds(region)
            .filterDate(start, end).filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 85)))
        if images.size().getInfo() == 0:
            raise HTTPException(status_code=404, detail="Sem imagens Sentinel-2 para a janela e distrito seleccionados.")
        def mask_scl(im):
            scl = im.select("SCL")
            valid = (scl.neq(0).And(scl.neq(1)).And(scl.neq(3))
                .And(scl.neq(7)).And(scl.neq(8)).And(scl.neq(9))
                .And(scl.neq(10)).And(scl.neq(11)))
            return im.updateMask(valid)
        return images.map(mask_scl)

    @classmethod
    def sentinel2_index(cls, index, region, start, end):
        collection = cls.s2_images(region, start, end)
        mosaic = collection.median().clip(region)
        bands = {
            "ndvi": ["B8", "B4"],
            "ndwi": ["B3", "B8"],
            "mndwi": ["B3", "B11"],
        }
        return mosaic.normalizedDifference(bands[index]).rename(index), collection

    @classmethod
    def terrain(cls, region, index):
        ee = cls.ee()
        images = ee.ImageCollection(DATASETS["elevation"]).filterBounds(region).select("DEM")
        projection = images.first().projection()
        dem = images.mosaic().setDefaultProjection(projection).clip(region)
        if index == "elevation":
            return dem.rename("elevation")
        return ee.Terrain.slope(dem).rename("slope").clip(region)

    @classmethod
    def chirps(cls, region, start, end):
        ee = cls.ee()
        images = ee.ImageCollection(DATASETS["precipitation"]).filterDate(start, end).filterBounds(region).select("precipitation")
        if images.size().getInfo() == 0:
            raise HTTPException(status_code=404, detail="CHIRPS não contém dados no intervalo solicitado. A publicação tem atraso.")
        return images.sum().rename("precipitation").clip(region), images

    @classmethod
    def sar_candidate(cls, region, start, end):
        """Pre/post VV backscatter change, same pass and geometry; exploratory only.

        Uses preceding interval of equal length as baseline. The method does
        not account for all orbit, vegetation or roughness artefacts.
        """
        ee = cls.ee()
        days = (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days
        before_start = (dt.date.fromisoformat(start) - dt.timedelta(days=days)).isoformat()
        source = (ee.ImageCollection(DATASETS["flood_sar"]).filterBounds(region)
            .filter(ee.Filter.eq("instrumentMode", "IW"))
            .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV"))
            .filter(ee.Filter.eq("resolution_meters", 10)))
        chosen = None
        for orbit in ("DESCENDING", "ASCENDING"):
            grouped = source.filter(ee.Filter.eq("orbitProperties_pass", orbit))
            before = grouped.filterDate(before_start, start)
            after = grouped.filterDate(start, end)
            if before.size().getInfo() > 0 and after.size().getInfo() > 0:
                chosen = (before, after, orbit)
                break
        if chosen is None:
            raise HTTPException(status_code=404, detail="Sem pares Sentinel-1 VV da mesma passagem para a comparação temporal.")
        before, after, orbit = chosen
        early = before.select("VV").median()
        late = after.select("VV").median()
        slope = cls.terrain(region, "slope")
        permanent = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select("occurrence").unmask(0)
        # >3 dB reduction and low post-event backscatter indicate possible water.
        candidate = (early.subtract(late).gt(3).And(late.lt(-15))
                     .And(slope.lt(5)).And(permanent.lt(80))
                     .selfMask().rename("flood_sar").clip(region))
        return candidate, after, orbit

    @classmethod
    def compute(cls, index: str, district_id: str, start_date: str, end_date: str):
        if index not in DATASETS:
            raise HTTPException(status_code=422, detail="Índice GEE desconhecido.")
        validate_window(start_date, end_date)
        ee = cls.ee()
        region = cls.region(district_id)
        metadata = {
            "district_id": district_id,
            "requested_start": start_date,
            "requested_end": end_date,
            "index": index,
            "source": DATASETS[index],
            "data_mode": "OBSERVED" if index != "flood_sar" else "ESTIMATED",
            "is_processed_layer": True,
            "method": "RADAR_CHANGE_CANDIDATE_UNVALIDATED" if index == "flood_sar" else "EARTH_ENGINE_INDEX",
        }
        try:
            if index in ("ndvi", "ndwi", "mndwi"):
                image, scenes = cls.sentinel2_index(index, region, start_date, end_date)
                metadata["image_count"] = scenes.size().getInfo()
                metadata["last_image_date"] = ee.Date(scenes.aggregate_max("system:time_start")).format("YYYY-MM-dd").getInfo()
            elif index in ("elevation", "slope"):
                image = cls.terrain(region, index)
                metadata["last_image_date"] = None  # Static model, not a real-time scene.
            elif index == "precipitation":
                image, scenes = cls.chirps(region, start_date, end_date)
                metadata["image_count"] = scenes.size().getInfo()
                metadata["last_image_date"] = ee.Date(scenes.aggregate_max("system:time_start")).format("YYYY-MM-dd").getInfo()
            else:
                image, scenes, orbit = cls.sar_candidate(region, start_date, end_date)
                metadata["image_count"] = scenes.size().getInfo()
                metadata["orbit_pass"] = orbit
                metadata["last_image_date"] = ee.Date(scenes.aggregate_max("system:time_start")).format("YYYY-MM-dd").getInfo()

            settings = INDEX_REGISTRY[index]
            vis = settings["vis"].copy()
            if index == "flood_sar":
                vis = {"min": 0, "max": 1, "palette": ["00bcd4"]}
            tile = image.getMapId(vis)
            metadata.update({
                "tile_url": tile["tile_fetcher"].url_format,
                "attribution": "Google Earth Engine · " + DATASETS[index],
                "name": settings["name"],
                "formula": settings["formula"],
                "description": settings["description"],
                "bands": settings["bands"],
                "group": settings["group"],
                "resolution": "10 m" if index in ("ndvi", "ndwi", "flood_sar") else ("~5.6 km" if index == "precipitation" else "30 m"),
            })
            return metadata
        except HTTPException:
            raise
        except Exception as exc:
            LOG.error("GEE processing error for %s: %s", index, type(exc).__name__)
            raise HTTPException(status_code=502, detail=f"Falha no processamento GEE ({type(exc).__name__}); nenhum mapa substituto será exibido.") from exc

    @classmethod
    def rainfall_series(cls, district_id: str, start_date: str, end_date: str):
        validate_window(start_date, end_date, max_days=365)
        ee = cls.ee()
        region = cls.region(district_id)
        collection = ee.ImageCollection(DATASETS["precipitation"]).filterBounds(region).filterDate(start_date, end_date)
        if collection.size().getInfo() == 0:
            raise HTTPException(status_code=404, detail="Sem dados CHIRPS publicados no período.")
        def daily(img):
            value = img.select("precipitation").reduceRegion(
                reducer=ee.Reducer.mean(), geometry=region, scale=5566,
                bestEffort=True, maxPixels=1e8,
            ).get("precipitation")
            return ee.Feature(None, {"date": img.date().format("YYYY-MM-dd"), "actual": value})
        try:
            features = ee.FeatureCollection(collection.toList(collection.size()).map(lambda raw: daily(ee.Image(raw))))
            result = features.getInfo()["features"]
            points = []
            for feature in result:
                props = feature["properties"]
                if props["actual"] is not None:
                    points.append({"date": props["date"], "actual": round(float(props["actual"]), 2),
                                   "baseline": None, "anomaly_pct": None})
            return {
                "district_id": district_id,
                "dataset": DATASETS["precipitation"],
                "data_mode": "OBSERVED",
                "unit": "mm/day",
                "period": {"start": start_date, "end_exclusive": end_date},
                "climatological_baseline": "NOT_COMPUTED",
                "last_observation": points[-1]["date"] if points else None,
                "points": sorted(points, key=lambda point: point["date"]),
            }
        except Exception as exc:
            LOG.error("CHIRPS series processing failed: %s", type(exc).__name__)
            raise HTTPException(status_code=502, detail="Não foi possível calcular a série CHIRPS.") from exc
