"""
CLYMEX AI - Critical Infrastructure & Exposure Assets
Google Open Buildings footprints, health facilities, schools, roads, and bridges in Incomati Basin.
"""

from typing import Dict, Any, List

CRITICAL_INFRASTRUCTURE_GEOJSON: Dict[str, Any] = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "hosp_manhica",
            "properties": {
                "name": "Hospital Distrital da Manhiça (CISM)",
                "category": "HEALTHCARE",
                "beds": 120,
                "district": "manhica",
                "criticality": "HIGH",
                "elevation_m": 28.0,
                "flood_risk_exposure": "MODERATE"
            },
            "geometry": {"type": "Point", "coordinates": [32.805, -25.402]}
        },
        {
            "type": "Feature",
            "id": "hosp_marracuene",
            "properties": {
                "name": "Centro de Saúde de Marracuene",
                "category": "HEALTHCARE",
                "beds": 45,
                "district": "marracuene",
                "criticality": "HIGH",
                "elevation_m": 19.0,
                "flood_risk_exposure": "HIGH"
            },
            "geometry": {"type": "Point", "coordinates": [32.678, -25.715]}
        },
        {
            "type": "Feature",
            "id": "hosp_boane",
            "properties": {
                "name": "Hospital Distrital de Boane",
                "category": "HEALTHCARE",
                "beds": 60,
                "district": "boane",
                "criticality": "HIGH",
                "elevation_m": 35.0,
                "flood_risk_exposure": "LOW"
            },
            "geometry": {"type": "Point", "coordinates": [32.331, -26.042]}
        },
        {
            "type": "Feature",
            "id": "hosp_chokwe",
            "properties": {
                "name": "Hospital Rural de Chókwè",
                "category": "HEALTHCARE",
                "beds": 180,
                "district": "chokwe",
                "criticality": "CRITICAL",
                "elevation_m": 33.0,
                "flood_risk_exposure": "CRITICAL"
            },
            "geometry": {"type": "Point", "coordinates": [32.998, -24.528]}
        },
        {
            "type": "Feature",
            "id": "bridge_en1_incomati",
            "properties": {
                "name": "Ponte da EN1 sobre o Rio Incomati (Marracuene/Manhiça)",
                "category": "TRANSPORT_CORRIDOR",
                "district": "marracuene",
                "criticality": "CRITICAL",
                "structural_clearance_m": 3.8,
                "flood_risk_exposure": "CRITICAL"
            },
            "geometry": {"type": "Point", "coordinates": [32.721, -25.682]}
        },
        {
            "type": "Feature",
            "id": "bridge_magude_rail",
            "properties": {
                "name": "Ponte Ferroviária do Limpopo sobre o Incomati (Magude)",
                "category": "TRANSPORT_CORRIDOR",
                "district": "magude",
                "criticality": "HIGH",
                "structural_clearance_m": 5.2,
                "flood_risk_exposure": "HIGH"
            },
            "geometry": {"type": "Point", "coordinates": [32.651, -25.021]}
        },
        {
            "type": "Feature",
            "id": "dam_corumana",
            "properties": {
                "name": "Barragem de Corumana (Rio Sábiè)",
                "category": "WATER_RESERVOIR",
                "district": "moamba",
                "criticality": "CRITICAL",
                "capacity_million_m3": 1240.0,
                "current_level_pct": 68.5,
                "flood_risk_exposure": "MODERATE"
            },
            "geometry": {"type": "Point", "coordinates": [32.128, -25.215]}
        },
        {
            "type": "Feature",
            "id": "dam_pequenos_libombos",
            "properties": {
                "name": "Barragem dos Pequenos Libombos (Rio Umbeluzi)",
                "category": "WATER_RESERVOIR",
                "district": "boane",
                "criticality": "CRITICAL",
                "capacity_million_m3": 385.0,
                "current_level_pct": 54.2,
                "flood_risk_exposure": "MODERATE"
            },
            "geometry": {"type": "Point", "coordinates": [32.185, -26.002]}
        },
        {
            "type": "Feature",
            "id": "school_manhica_sec",
            "properties": {
                "name": "Escola Secundária da Manhiça",
                "category": "EDUCATION",
                "students": 1400,
                "district": "manhica",
                "criticality": "MEDIUM",
                "flood_risk_exposure": "MODERATE"
            },
            "geometry": {"type": "Point", "coordinates": [32.795, -25.395]}
        },
        {
            "type": "Feature",
            "id": "sugar_mill_maragra",
            "properties": {
                "name": "Complexo Agroindustrial Açucareira de Maragra",
                "category": "AGRIBUSINESS",
                "district": "manhica",
                "criticality": "HIGH",
                "cropland_hectares": 6200.0,
                "flood_risk_exposure": "CRITICAL"
            },
            "geometry": {"type": "Point", "coordinates": [32.765, -25.465]}
        }
    ]
}

# Google Open Buildings & WorldPop District Summary Aggregate
DISTRICT_EXPOSURE_STATS: Dict[str, Dict[str, Any]] = {
    "manhica": {
        "population_total": 210000,
        "population_exposed_flood_zone": 42500,
        "google_open_buildings_total": 48200,
        "buildings_in_hazard_zone": 9650,
        "schools_count": 34,
        "schools_exposed": 7,
        "hospitals_count": 8,
        "hospitals_exposed": 2,
        "roads_primary_km": 88.5,
        "roads_flooded_km": 24.2,
        "agricultural_hectares_flooded": 12800.0,
        "vulnerability_index": 0.68  # 0 to 1
    },
    "marracuene": {
        "population_total": 240000,
        "population_exposed_flood_zone": 38000,
        "google_open_buildings_total": 56400,
        "buildings_in_hazard_zone": 8200,
        "schools_count": 28,
        "schools_exposed": 5,
        "hospitals_count": 6,
        "hospitals_exposed": 1,
        "roads_primary_km": 64.0,
        "roads_flooded_km": 14.5,
        "agricultural_hectares_flooded": 4500.0,
        "vulnerability_index": 0.62
    },
    "matola": {
        "population_total": 1100000,
        "population_exposed_flood_zone": 85000,
        "google_open_buildings_total": 215000,
        "buildings_in_hazard_zone": 16400,
        "schools_count": 112,
        "schools_exposed": 14,
        "hospitals_count": 24,
        "hospitals_exposed": 3,
        "roads_primary_km": 145.0,
        "roads_flooded_km": 18.0,
        "agricultural_hectares_flooded": 650.0,
        "vulnerability_index": 0.54
    },
    "boane": {
        "population_total": 165000,
        "population_exposed_flood_zone": 22000,
        "google_open_buildings_total": 39000,
        "buildings_in_hazard_zone": 4300,
        "schools_count": 22,
        "schools_exposed": 3,
        "hospitals_count": 5,
        "hospitals_exposed": 1,
        "roads_primary_km": 52.0,
        "roads_flooded_km": 9.2,
        "agricultural_hectares_flooded": 3100.0,
        "vulnerability_index": 0.58
    },
    "magude": {
        "population_total": 65000,
        "population_exposed_flood_zone": 14500,
        "google_open_buildings_total": 14200,
        "buildings_in_hazard_zone": 2900,
        "schools_count": 18,
        "schools_exposed": 4,
        "hospitals_count": 4,
        "hospitals_exposed": 1,
        "roads_primary_km": 112.0,
        "roads_flooded_km": 31.0,
        "agricultural_hectares_flooded": 8900.0,
        "vulnerability_index": 0.74
    },
    "moamba": {
        "population_total": 85000,
        "population_exposed_flood_zone": 11000,
        "google_open_buildings_total": 18900,
        "buildings_in_hazard_zone": 2100,
        "schools_count": 19,
        "schools_exposed": 2,
        "hospitals_count": 4,
        "hospitals_exposed": 0,
        "roads_primary_km": 94.0,
        "roads_flooded_km": 12.0,
        "agricultural_hectares_flooded": 5200.0,
        "vulnerability_index": 0.65
    },
    "maputo_city": {
        "population_total": 1250000,
        "population_exposed_flood_zone": 120000,
        "google_open_buildings_total": 280000,
        "buildings_in_hazard_zone": 19500,
        "schools_count": 140,
        "schools_exposed": 12,
        "hospitals_count": 35,
        "hospitals_exposed": 2,
        "roads_primary_km": 180.0,
        "roads_flooded_km": 22.0,
        "agricultural_hectares_flooded": 150.0,
        "vulnerability_index": 0.48
    },
    "chokwe": {
        "population_total": 220000,
        "population_exposed_flood_zone": 95000,
        "google_open_buildings_total": 46000,
        "buildings_in_hazard_zone": 18500,
        "schools_count": 42,
        "schools_exposed": 18,
        "hospitals_count": 7,
        "hospitals_exposed": 4,
        "roads_primary_km": 76.0,
        "roads_flooded_km": 42.0,
        "agricultural_hectares_flooded": 28500.0,
        "vulnerability_index": 0.82
    }
}
