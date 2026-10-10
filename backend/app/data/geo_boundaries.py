"""
CLYMEX AI - Geospatial Data: Mozambique & Greater Maputo / Incomati Basin
Accurate GeoJSON FeatureCollections for Administrative Boundaries & Hydrography.
"""

from typing import Dict, Any, List

# Incomati Basin & Greater Maputo Districts
# Center coordinates approx: Lat -25.0 to -26.0, Lng 32.0 to 33.2
INCOMATI_DISTRICTS_GEOJSON: Dict[str, Any] = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "manhica",
            "properties": {
                "id": "manhica",
                "name": "Manhiça",
                "province": "Maputo Província",
                "country": "Mozambique",
                "area_sqkm": 2373.0,
                "population": 210000,
                "dominant_risk": "FLOOD",
                "basin": "Incomati Basin",
                "center": [-25.40, 32.80]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [32.65, -25.20],
                    [32.95, -25.15],
                    [33.05, -25.45],
                    [32.90, -25.65],
                    [32.60, -25.55],
                    [32.55, -25.30],
                    [32.65, -25.20]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "marracuene",
            "properties": {
                "id": "marracuene",
                "name": "Marracuene",
                "province": "Maputo Província",
                "country": "Mozambique",
                "area_sqkm": 703.0,
                "population": 240000,
                "dominant_risk": "FLOOD",
                "basin": "Lower Incomati / Estuary",
                "center": [-25.72, 32.68]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [32.55, -25.55],
                    [32.80, -25.60],
                    [32.85, -25.80],
                    [32.65, -25.85],
                    [32.50, -25.70],
                    [32.55, -25.55]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "matola",
            "properties": {
                "id": "matola",
                "name": "Matola",
                "province": "Maputo Província",
                "country": "Mozambique",
                "area_sqkm": 373.0,
                "population": 1100000,
                "dominant_risk": "WATER_STRESS",
                "basin": "Matola River Catchment",
                "center": [-25.96, 32.46]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [32.38, -25.85],
                    [32.55, -25.87],
                    [32.53, -26.02],
                    [32.35, -26.01],
                    [32.38, -25.85]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "boane",
            "properties": {
                "id": "boane",
                "name": "Boane",
                "province": "Maputo Província",
                "country": "Mozambique",
                "area_sqkm": 820.0,
                "population": 165000,
                "dominant_risk": "WATER_STRESS",
                "basin": "Umbeluzi Catchment",
                "center": [-26.04, 32.33]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [32.20, -25.92],
                    [32.42, -25.95],
                    [32.45, -26.15],
                    [32.18, -26.18],
                    [32.20, -25.92]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "magude",
            "properties": {
                "id": "magude",
                "name": "Magude",
                "province": "Maputo Província",
                "country": "Mozambique",
                "area_sqkm": 6961.0,
                "population": 65000,
                "dominant_risk": "DROUGHT",
                "basin": "Upper Incomati Basin",
                "center": [-25.02, 32.65]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [32.15, -24.70],
                    [32.85, -24.65],
                    [33.10, -25.10],
                    [32.65, -25.25],
                    [32.10, -25.15],
                    [32.15, -24.70]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "moamba",
            "properties": {
                "id": "moamba",
                "name": "Moamba",
                "province": "Maputo Província",
                "country": "Mozambique",
                "area_sqkm": 4628.0,
                "population": 85000,
                "dominant_risk": "DROUGHT",
                "basin": "Middle Incomati / Corumana",
                "center": [-25.60, 32.24]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [31.95, -25.30],
                    [32.45, -25.35],
                    [32.40, -25.80],
                    [31.90, -25.75],
                    [31.95, -25.30]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "maputo_city",
            "properties": {
                "id": "maputo_city",
                "name": "Maputo Cidade",
                "province": "Maputo Cidade",
                "country": "Mozambique",
                "area_sqkm": 347.0,
                "population": 1250000,
                "dominant_risk": "FLOOD",
                "basin": "Maputo Coastal Catchment",
                "center": [-25.92, 32.58]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [32.52, -25.85],
                    [32.65, -25.88],
                    [32.68, -26.05],
                    [32.50, -26.02],
                    [32.52, -25.85]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "chokwe",
            "properties": {
                "id": "chokwe",
                "name": "Chókwè",
                "province": "Gaza Província",
                "country": "Mozambique",
                "area_sqkm": 2466.0,
                "population": 220000,
                "dominant_risk": "FLOOD",
                "basin": "Lower Limpopo / Agricultural Perimeter",
                "center": [-24.53, 33.00]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [32.80, -24.30],
                    [33.20, -24.25],
                    [33.30, -24.75],
                    [32.85, -24.70],
                    [32.80, -24.30]
                ]]
            }
        }
    ]
}

# Hydrography - Major Rivers of the Incomati Basin
INCOMATI_RIVERS_GEOJSON: Dict[str, Any] = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "incomati_main",
            "properties": {
                "name": "Rio Incomati (Leito Principal)",
                "length_km": 480.0,
                "type": "Perennial River",
                "discharge_avg_m3s": 110.0,
                "flood_stage_alert_m": 6.5
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [32.05, -24.85],
                    [32.30, -24.95],
                    [32.55, -25.02],
                    [32.68, -25.18],
                    [32.80, -25.35],
                    [32.75, -25.55],
                    [32.72, -25.68],
                    [32.70, -25.80],
                    [32.65, -25.88]
                ]
            }
        },
        {
            "type": "Feature",
            "id": "umbeluzi",
            "properties": {
                "name": "Rio Umbeluzi",
                "length_km": 160.0,
                "type": "Perennial River",
                "discharge_avg_m3s": 25.0,
                "flood_stage_alert_m": 4.2
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [32.08, -26.08],
                    [32.22, -26.04],
                    [32.32, -26.02],
                    [32.45, -25.98],
                    [32.55, -25.95]
                ]
            }
        },
        {
            "type": "Feature",
            "id": "sabie_tributary",
            "properties": {
                "name": "Rio Sábiè (Afluente Incomati)",
                "length_km": 110.0,
                "type": "Seasonal River",
                "discharge_avg_m3s": 35.0,
                "flood_stage_alert_m": 5.0
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [31.98, -25.15],
                    [32.25, -25.22],
                    [32.55, -25.02]
                ]
            }
        }
    ]
}

# Flood Inundation Extent Polygon (Simulated Sentinel-1 SAR change detection footprint)
FLOOD_EXTENT_SAR_GEOJSON: Dict[str, Any] = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "flood_zone_manhica_valley",
            "properties": {
                "name": "Mancha de Inundação Aluvial - Vale do Incomati",
                "sensor": "Sentinel-1 C-Band SAR",
                "polarization": "VV/VH Backscatter Difference",
                "acquisition_date": "2026-09-17T05:30:00Z",
                "water_depth_est_m": 1.45,
                "severity": "CRITICAL"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [32.72, -25.30],
                    [32.84, -25.32],
                    [32.82, -25.50],
                    [32.74, -25.58],
                    [32.68, -25.42],
                    [32.72, -25.30]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "flood_zone_marracuene_estuary",
            "properties": {
                "name": "Zona de Transbordo Estuarino - Marracuene",
                "sensor": "Sentinel-1 C-Band SAR",
                "polarization": "VV/VH Backscatter Difference",
                "acquisition_date": "2026-09-17T05:30:00Z",
                "water_depth_est_m": 0.85,
                "severity": "HIGH"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [32.68, -25.68],
                    [32.76, -25.72],
                    [32.74, -25.82],
                    [32.66, -25.80],
                    [32.68, -25.68]
                ]]
            }
        }
    ]
}
