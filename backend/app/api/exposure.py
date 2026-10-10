"""
CLYMEX AI - Exposure Engine API
Intersects hazards with Google Open Buildings, WorldPop, and critical infrastructure.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Body
from app.models.domain import ExposureBreakdown
from app.data.exposure_data import CRITICAL_INFRASTRUCTURE_GEOJSON, DISTRICT_EXPOSURE_STATS
from app.services.exposure_engine import ExposureEngine

router = APIRouter(prefix="/exposure", tags=["Exposure & Assets"])


@router.get("", response_model=Dict[str, Any])
def get_critical_infrastructure():
    """
    Returns spatial points of hospitals, schools, bridges, and dams in GeoJSON format.
    """
    return CRITICAL_INFRASTRUCTURE_GEOJSON


@router.get("/{district_id}", response_model=Dict[str, Any])
def get_district_exposure_details(district_id: str):
    """
    Returns granular exposure metrics for a selected district.
    """
    stats = DISTRICT_EXPOSURE_STATS.get(district_id.lower())
    if not stats:
        raise HTTPException(status_code=404, detail="Distrito não encontrado no cadastro de exposição.")
    return {
        "district_id": district_id.lower(),
        "metrics": stats,
        "source": "Google Open Buildings v3 & WorldPop Africa 100m"
    }


@router.post("/custom-polygon", response_model=ExposureBreakdown)
def calculate_custom_polygon(polygon: List[List[float]] = Body(..., example=[[32.65, -25.20], [32.95, -25.15], [32.90, -25.65], [32.65, -25.20]])):
    """
    Calculates population, building count, roads, and facilities within any user-drawn polygon.
    """
    if len(polygon) < 3:
        raise HTTPException(status_code=400, detail="Polígono deve conter ao menos 3 coordenadas.")
    return ExposureEngine.calculate_custom_polygon_exposure(polygon)
