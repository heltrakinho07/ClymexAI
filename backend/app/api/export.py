"""
CLYMEX AI - Data Export & Multi-District Comparison Matrix API
"Predict Risk. Protect Tomorrow."
Provides CSV, GeoJSON and comparative matrix exports for decision-makers.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Query, Response, HTTPException
from app.services.risk_engine import ClimateRiskEngine
from app.data.geo_boundaries import INCOMATI_DISTRICTS_GEOJSON
from app.services.report_generator import ReportGenerator

router = APIRouter(prefix="/exports", tags=["Data Export & Analytics Matrix"])


@router.get("/matrix", response_model=List[Dict[str, Any]])
async def get_multi_district_matrix(mode: Optional[str] = Query("live")):
    """
    Returns a multi-hazard comparison matrix for all Incomati districts.
    Includes Flood, Drought, Water Stress, Population, Google Open Buildings, TWI, and Distance to River.
    """
    districts = ["manhica", "marracuene", "matola", "boane", "magude", "moamba", "maputo_city", "chokwe"]
    matrix = []

    for dist_id in districts:
        if mode == "live":
            assessment = await ClimateRiskEngine.assess_district_live(dist_id)
        else:
            assessment = ClimateRiskEngine.assess_district(dist_id)

        flood_a = ClimateRiskEngine.assess_district(dist_id, "FLOOD")
        drought_a = ClimateRiskEngine.assess_district(dist_id, "DROUGHT")
        stress_a = ClimateRiskEngine.assess_district(dist_id, "WATER_STRESS")

        matrix.append({
            "id": assessment.area_id,
            "name": assessment.area_name,
            "province": assessment.province,
            "composite_risk_score": assessment.risk_score,
            "risk_level": assessment.risk_level.value,
            "dominant_hazard": assessment.hazard_type.value,
            "flood_score": flood_a.hazard_score,
            "drought_score": drought_a.hazard_score,
            "water_stress_score": stress_a.hazard_score,
            "population_exposed": assessment.exposure.population_exposed,
            "buildings_exposed": assessment.exposure.buildings_count,
            "roads_flooded_km": assessment.exposure.roads_km,
            "schools_exposed": assessment.exposure.schools_count,
            "hospitals_exposed": assessment.exposure.hospitals_count,
            "cropland_hectares": assessment.exposure.cropland_hectares,
            "rainfall_7d_mm": assessment.indicators.rainfall_7d_mm,
            "rainfall_anomaly_pct": assessment.indicators.rainfall_anomaly_pct,
            "soil_moisture_pct": assessment.indicators.soil_moisture_pct,
            "ndvi_current": assessment.indicators.ndvi_current,
            "distance_to_river_km": assessment.indicators.distance_to_river_km,
            "topographic_wetness_index": assessment.indicators.topographic_wetness_index,
            "confidence_pct": assessment.confidence_pct,
            "data_mode": assessment.data_mode.value
        })

    return matrix


@router.get("/csv/{district_id}")
async def export_district_csv(district_id: str):
    """
    Generates downloadable CSV bulletin for designated district.
    """
    report = ReportGenerator.generate_district_report(district_id)

    csv_rows = [
        "METRICA,VALOR,UNIDADE,FONTE",
        f"Distrito,{report.title.split('—')[-1].strip()},Nome,CLYMEX AI",
        f"Regiao,{report.region},Bacia,Geografia Oficial",
        f"Data Geracao,{report.generated_at},Data,UTC",
        f"Escore Risco Geral,{report.overall_risk_score},Pontos (0-100),Motor Central de Risco",
        f"Nivel Operacional,{report.overall_risk_level},Tier,Classificacao UNDRR",
        f"Populacao Exposta,{report.total_population_exposed},Habitantes,WorldPop Africa 100m",
        f"Edificios Expostos,{report.total_buildings_exposed},Estruturas,Google Open Buildings v3",
        f"Instalacoes Criticas,{report.critical_infrastructure_count},Pontos,OpenStreetMap & Cadastro",
        f"Perigo Cheia,{report.hazard_matrix['flood']['hazard_score']},Pontos (0-100),Sentinel-1 SAR / ERA5",
        f"Perigo Seca,{report.hazard_matrix['drought']['hazard_score']},Pontos (0-100),Sentinel-2 NDVI / VCI",
        f"Perigo Estresse Hidrico,{report.hazard_matrix['water_stress']['hazard_score']},Pontos (0-100),Albufeiras / Balanco"
    ]

    csv_content = "\n".join(csv_rows)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=clymex_risk_{district_id}.csv"}
    )


@router.get("/geojson")
def export_risk_geojson():
    """
    Exports administrative boundaries enriched with latest risk scores in GeoJSON format.
    """
    features = []
    for feat in INCOMATI_DISTRICTS_GEOJSON["features"]:
        dist_id = feat["properties"]["id"]
        assessment = ClimateRiskEngine.assess_district(dist_id)
        
        enriched_props = feat["properties"].copy()
        enriched_props.update({
            "risk_score": assessment.risk_score,
            "risk_level": assessment.risk_level.value,
            "hazard_score": assessment.hazard_score,
            "population_exposed": assessment.exposure.population_exposed,
            "buildings_exposed": assessment.exposure.buildings_count,
            "twi": assessment.indicators.topographic_wetness_index,
            "rainfall_7d_mm": assessment.indicators.rainfall_7d_mm,
            "data_mode": assessment.data_mode.value
        })

        features.append({
            "type": "Feature",
            "id": feat["id"],
            "properties": enriched_props,
            "geometry": feat["geometry"]
        })

    return {
        "type": "FeatureCollection",
        "name": "CLYMEX_AI_Incomati_Risk_GeoJSON",
        "features": features
    }
