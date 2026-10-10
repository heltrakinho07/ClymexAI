"""
CLYMEX AI - Satellite Earth Observation & Google Earth Engine API
"Predict Risk. Protect Tomorrow."
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from app.models.domain import DataProvenance
from app.data.historical_records import DATA_PROVENANCE_CATALOG
from app.services.gee_service import GoogleEarthEngineBridge

router = APIRouter(prefix="/satellite", tags=["Satellite Earth Observation"])


class GEEConfigureRequest(BaseModel):
    project_id: Optional[str] = None
    service_account_key: Optional[str] = None


class GEETileRequest(BaseModel):
    index: str = "ndvi"
    district_id: Optional[str] = "manhica"
    start_date: str = "2024-01-01"
    end_date: str = "2024-12-31"


@router.get("/metadata", response_model=List[DataProvenance])
def get_satellite_metadata_provenance():
    """
    Returns full scientific metadata, resolutions, revisit periods, and sensor provenance.
    """
    return DATA_PROVENANCE_CATALOG


@router.get("/gee/status", response_model=Dict[str, Any])
def get_gee_status():
    """
    Returns Google Earth Engine connection status, active GCP project, and available indices.
    """
    return GoogleEarthEngineBridge.get_status()


@router.post("/gee/configure", response_model=Dict[str, Any])
def configure_gee(req: GEEConfigureRequest):
    """
    Updates Google Earth Engine project ID or Service Account key dynamically.
    """
    return GoogleEarthEngineBridge.configure(
        project_id=req.project_id,
        sa_key=req.service_account_key
    )


@router.post("/gee/tile", response_model=Dict[str, Any])
def get_gee_index_tile(req: GEETileRequest):
    """
    Computes or retrieves satellite tile URL for any spectral, radar, or terrain index.
    """
    return GoogleEarthEngineBridge.compute_index_tile(
        index=req.index,
        district_id=req.district_id,
        start_date=req.start_date,
        end_date=req.end_date
    )


@router.get("/gee/metrics/{district_id}", response_model=Dict[str, Any])
def get_district_satellite_metrics(district_id: str):
    """
    Returns real Earth Observation metrics (Sentinel-2 NDVI, NDWI, SAR flood, DEM elevation).
    """
    return GoogleEarthEngineBridge.get_district_satellite_metrics(district_id)
