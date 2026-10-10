"""
CLYMEX AI - Risk Engine Endpoints
"Predict Risk. Protect Tomorrow."
"""

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from app.models.domain import RiskAssessment, HazardType
from app.services.risk_engine import ClimateRiskEngine

router = APIRouter(prefix="/risk", tags=["Climate Risk Engine"])


@router.get("", response_model=List[RiskAssessment])
async def get_all_risks(mode: Optional[str] = Query("live")):
    """
    Returns latest multi-hazard risk assessments for all demonstrator districts in Incomati basin.
    When mode='live', executes real geoprocessing across all districts concurrently.
    """
    if mode == "live":
        import asyncio
        districts = ["manhica", "marracuene", "matola", "boane", "magude", "moamba", "maputo_city", "chokwe"]
        return await asyncio.gather(*[
            ClimateRiskEngine.assess_district_live(d, HazardType.OVERALL_CLIMATE)
            for d in districts
        ])
    return ClimateRiskEngine.get_all_districts_overview()



@router.get("/{area_id}", response_model=RiskAssessment)
async def get_area_risk(
    area_id: str,
    hazard: Optional[HazardType] = Query(HazardType.OVERALL_CLIMATE, description="Target hazard type"),
    mode: Optional[str] = Query("live", description="Data mode: 'live' (real geoprocessing) or 'demo'")
):
    """
    Returns full explainable risk breakdown for a specific administrative district.
    Supports real-time geoprocessing with mode='live'.
    """
    if mode == "live":
        return await ClimateRiskEngine.assess_district_live(area_id, hazard)
    return ClimateRiskEngine.assess_district(area_id, hazard)



@router.get("/flood/{area_id}", response_model=RiskAssessment)
def get_flood_risk(area_id: str):
    """
    Returns flood risk score, topographic wetness index, Sentinel-1 SAR change, and contributing factors.
    """
    return ClimateRiskEngine.assess_district(area_id, HazardType.FLOOD)


@router.get("/drought/{area_id}", response_model=RiskAssessment)
def get_drought_risk(area_id: str):
    """
    Returns drought risk score, NDVI/VCI anomaly, soil moisture deficit, and CHIRPS precipitation deficit.
    """
    return ClimateRiskEngine.assess_district(area_id, HazardType.DROUGHT)


@router.get("/water-stress/{area_id}", response_model=RiskAssessment)
def get_water_stress_risk(area_id: str):
    """
    Returns water stress score, reservoir capacity (Corumana/Pequenos Libombos), and surface water deficit.
    """
    return ClimateRiskEngine.assess_district(area_id, HazardType.WATER_STRESS)
