"""
CLYMEX AI - Geospatial Boundaries & Administrative Areas API
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Query
from app.data.geo_boundaries import (
    INCOMATI_DISTRICTS_GEOJSON,
    INCOMATI_RIVERS_GEOJSON,
    FLOOD_EXTENT_SAR_GEOJSON
)

router = APIRouter(prefix="/areas", tags=["Geospatial Boundaries"])


@router.get("", response_model=Dict[str, Any])
def get_administrative_areas(
    country: Optional[str] = Query("Mozambique", description="Filter by country"),
    region: Optional[str] = Query("Incomati Basin", description="Filter by region/basin")
):
    """
    Returns administrative district boundaries in GeoJSON format.
    """
    return INCOMATI_DISTRICTS_GEOJSON


@router.get("/rivers", response_model=Dict[str, Any])
def get_basin_rivers():
    """
    Returns hydrographic river network (Incomati, Umbeluzi, Sábiè) in GeoJSON format.
    """
    return INCOMATI_RIVERS_GEOJSON


@router.get("/flood-extent", response_model=Dict[str, Any])
def get_flood_extent():
    """
    Returns active flood extent polygons derived from Sentinel-1 SAR radar change detection.
    """
    return FLOOD_EXTENT_SAR_GEOJSON
