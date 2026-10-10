"""
CLYMEX AI - Google Earth Engine (GEE) Presets & Spectral Index Definitions
Adapted from GeoMoz Explorer for climate risk intelligence in Mozambique.
"""

from typing import Any, Dict

# Mozambique Bounding Box [West, South, East, North]
MZ_BBOX = [30.2, -26.9, 40.8, -10.5]

INDEX_REGISTRY: Dict[str, Dict[str, Any]] = {
    "ndvi": {
        "group": "spectral",
        "needs": ["s2"],
        "name": "NDVI — Índice de Vegetação (Sentinel-2)",
        "formula": "NDVI = (B8 − B4) / (B8 + B4)",
        "bands": "NIR (B8) e Vermelho (B4)",
        "description": "Mede o vigor fotossintético e biomassa vegetal. Valores baixos indicam seca agrícola ou solo degradado.",
        "vis": {
            "min": -0.15,
            "max": 0.85,
            "palette": ["8B4513", "D2B48C", "FFFACD", "ADFF2F", "32CD32", "006400"]
        },
        "norm": (-0.2, 0.9),
    },
    "ndwi": {
        "group": "water",
        "needs": ["s2"],
        "name": "NDWI — Índice de Água Superficial (McFeeters)",
        "formula": "NDWI = (B3 − B8) / (B3 + B8)",
        "bands": "Verde (B3) e NIR (B8)",
        "description": "Identifica corpos hídricos abertos e áreas alagadas. Valores > 0.0 indicam lâmina d'água superficial.",
        "vis": {
            "min": -0.5,
            "max": 0.5,
            "palette": ["8B4513", "FFFFFF", "00FFFF", "0000FF", "00008B"]
        },
        "norm": (-0.5, 0.5),
    },
    "mndwi": {
        "group": "water",
        "needs": ["s2"],
        "name": "MNDWI — Índice de Água Modificado (Xu, 2006)",
        "formula": "MNDWI = (B3 − B11) / (B3 + B11)",
        "bands": "Verde (B3) e SWIR1 (B11)",
        "description": "Supressão avançada de ruído urbano em zonas aluviais e estuários como o Rio Incomati e Baía de Maputo.",
        "vis": {
            "min": -0.6,
            "max": 0.6,
            "palette": ["7F2704", "FFFFFF", "9ECAE1", "4292C6", "08519C", "08306B"]
        },
        "norm": (-0.6, 0.6),
    },
    "flood_sar": {
        "group": "radar",
        "needs": ["s1"],
        "name": "Mancha de Cheia Radar — Sentinel-1 C-SAR",
        "formula": "Diferença radiométrica retroespalhamento VV/VH (dB)",
        "bands": "Sentinel-1 SAR C-band (VV + VH)",
        "description": "Detecção de inundação imune a cobertura de nuvens ou chuva extrema durante ciclones e tempestades tropicais.",
        "vis": {
            "min": -25.0,
            "max": 0.0,
            "palette": ["000814", "001d3d", "003566", "0077b6", "00b4d8", "90e0ef"]
        },
        "norm": (-25.0, 0.0),
    },
    "elevation": {
        "group": "terrain",
        "needs": ["dem"],
        "name": "Elevação — DEM Copernicus GLO-30",
        "formula": "Modelo Digital de Elevação Copernicus 30m",
        "bands": "Copernicus GLO-30 DEM",
        "description": "Morfologia do terreno e calhas de drenagem natural. Determina áreas aluviais de cota baixa vulneráveis.",
        "vis": {
            "min": 0,
            "max": 150,
            "palette": ["004b23", "38b000", "70e000", "ccff33", "f9c74f", "f9844a", "f94144"]
        },
        "norm": (0, 200),
    },
    "slope": {
        "group": "terrain",
        "needs": ["dem"],
        "name": "Declividade — Slope Copernicus GLO-30",
        "formula": "ee.Terrain.slope(DEM)",
        "bands": "Copernicus GLO-30 DEM",
        "description": "Graus de inclinação do relevo. Zonas planas (< 2°) acumulam lâmina de cheia e estagnação hídrica.",
        "vis": {
            "min": 0,
            "max": 20,
            "palette": ["2d6a4f", "52b788", "95d5b2", "d8f3dc", "fca311", "e76f51"]
        },
        "norm": (0, 30),
    },
    "vci": {
        "group": "drought",
        "needs": ["modis"],
        "name": "VCI — Índice de Condição da Vegetação (MODIS)",
        "formula": "VCI = ((NDVI − NDVI_min) / (NDVI_max − NDVI_min)) × 100",
        "bands": "MODIS MOD13A2 (16 dias, 1km)",
        "description": "Índice operacional de seca agrícola internacional. VCI < 40% indica seca moderada a severa.",
        "vis": {
            "min": 0,
            "max": 100,
            "palette": ["7f0000", "d73027", "f46d43", "fdae61", "fee08b", "d9ef8b", "a6d96a", "66bd63", "1a9850", "006837"]
        },
        "norm": (0, 100),
    },
    "precipitation": {
        "group": "climate",
        "needs": ["chirps"],
        "name": "Precipitação Acumulada — CHIRPS Daily",
        "formula": "Precipitação acumulada diária / mensal (mm)",
        "bands": "UCSB-CHG/CHIRPS/DAILY (0.05° ~5km)",
        "description": "Série temporal de chuva calibrada por satélite e estações terrestres para o sul de Moçambique.",
        "vis": {
            "min": 0,
            "max": 250,
            "palette": ["FFFFFF", "C6DBEF", "9ECAE1", "6BAED6", "3182BD", "08519C", "08306B"]
        },
        "norm": (0, 300),
    },
}
