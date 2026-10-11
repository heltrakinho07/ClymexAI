"""
CLYMEX AI - Satellite Earth Observation & Google Earth Engine API
"Predict Risk. Protect Tomorrow."
"""

from typing import Dict, Any, List, Optional
import datetime as dt
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import BaseModel
from app.models.domain import DataProvenance
from app.data.historical_records import DATA_PROVENANCE_CATALOG
from app.services.gee_service import GoogleEarthEngineBridge
from app.services.gee_processing import EarthEngineProcessor, DATASETS
from app.config import settings

router = APIRouter(prefix="/satellite", tags=["Satellite Earth Observation"])


class GEEConfigureRequest(BaseModel):
    project_id: Optional[str] = None
    service_account_key: Optional[str] = None


class GEETileRequest(BaseModel):
    index: str = "ndvi"
    district_id: Optional[str] = "manhica"
    start_date: Optional[str] = None
    end_date: Optional[str] = None


@router.get("/metadata", response_model=List[DataProvenance])
def get_satellite_metadata_provenance():
    """
    Returns full scientific metadata, resolutions, revisit periods, and sensor provenance.
    """
    return DATA_PROVENANCE_CATALOG


@router.get("/gee/status", response_model=Dict[str, Any])
def get_gee_status():
    """Return verified GEE status (remote connection test), not a project-id guess."""
    return GoogleEarthEngineBridge.get_status()


@router.post("/gee/configure", response_model=Dict[str, Any])
def configure_gee(req: GEEConfigureRequest):
    """
    Updates Google Earth Engine project ID or Service Account key dynamically.
    """
    if req.service_account_key:
        raise HTTPException(status_code=400, detail="Nunca envie chaves de conta de serviço pelo navegador.")
    if settings.ENV != "development":
        raise HTTPException(status_code=403, detail="A configuração GEE está desactivada fora do desenvolvimento.")
    return GoogleEarthEngineBridge.configure(project_id=req.project_id)


@router.post("/gee/tile", response_model=Dict[str, Any])
def get_gee_index_tile(req: GEETileRequest):
    """Return an actual processed GEE image tile or a clear error (no basemap fallback)."""
    return GoogleEarthEngineBridge.compute_index_tile(
        index=req.index,
        district_id=req.district_id,
        start_date=req.start_date,
        end_date=req.end_date
    )


@router.get("/gee/precipitation-series/{district_id}", response_model=Dict[str, Any])
def get_chirps_precipitation_series(
    district_id: str,
    days: int = Query(30, ge=7, le=180),
    end_date: Optional[str] = Query(None, description="Data final exclusiva YYYY-MM-DD; omita para último CHIRPS publicado."),
):
    """Historical CHIRPS actual daily observations, no invented climatological baseline."""
    ee = EarthEngineProcessor.ee()
    region = EarthEngineProcessor.region(district_id)
    end = dt.date.fromisoformat(end_date) if end_date else dt.datetime.now(dt.timezone.utc).date() + dt.timedelta(days=1)
    if end_date is None:
        # Account for the publication delay, returning the most recently available scene
        # and its real acquisition date rather than inventing values for missing days.
        collection = (ee.ImageCollection(DATASETS["precipitation"]).filterBounds(region)
            .filterDate((end - dt.timedelta(days=365)).isoformat(), end.isoformat()))
        if collection.size().getInfo() == 0:
            raise HTTPException(status_code=404, detail="Sem CHIRPS publicado nos últimos 365 dias.")
        timestamp = collection.aggregate_max("system:time_start").getInfo()
        end = dt.datetime.fromtimestamp(timestamp / 1000, tz=dt.timezone.utc).date() + dt.timedelta(days=1)
    start = end - dt.timedelta(days=days)
    return EarthEngineProcessor.rainfall_series(district_id, start.isoformat(), end.isoformat())


@router.get("/gee/metrics/{district_id}", response_model=Dict[str, Any])
def get_district_satellite_metrics(district_id: str):
    """Live Earth Engine-derived metrics, explicitly exposing estimates and source dates."""
    return GoogleEarthEngineBridge.get_district_satellite_metrics(district_id)
