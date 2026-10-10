"""Geospatial API — real Mozambique district/province polygons from GeoMoz.

Legacy /areas retains the initial eight-district demonstrator scope, while
/districts and /provinces expose the national geography.
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, Query

from app.services.administrative_boundaries import districts_geojson, provinces_geojson
from app.data.geo_boundaries import INCOMATI_RIVERS_GEOJSON, FLOOD_EXTENT_SAR_GEOJSON

router = APIRouter(prefix="/areas", tags=["Geospatial Boundaries"])


@router.get("", response_model=Dict[str, Any])
def get_administrative_areas(
    country: Optional[str] = Query("Mozambique"),
    region: Optional[str] = Query("Incomati Basin"),
):
    """Real GeoMoz boundaries of the 8 initial demonstrator districts."""
    return districts_geojson(focus_only=True)


@router.get("/provinces", response_model=Dict[str, Any])
def get_all_provinces(
    province: Optional[str] = Query(None, description="Exact province name"),
):
    """All Mozambique provinces (including Maputo City) in EPSG:4326."""
    return provinces_geojson(province)


@router.get("/districts", response_model=Dict[str, Any])
def get_all_districts(
    province: Optional[str] = Query(None, description="Exact province name"),
    focus_only: bool = Query(False),
):
    """GeoMoz districts; optionally filter province or focus demonstrator."""
    return districts_geojson(province=province, focus_only=focus_only)


@router.get("/rivers", response_model=Dict[str, Any])
def get_basin_rivers():
    """DEMO hydrographic geometries (not a verified hydrological dataset)."""
    return {
        **INCOMATI_RIVERS_GEOJSON,
        "data_mode": "DEMO",
        "source": "CLYMEX illustrative hydrography; NOT surveyed river geometry",
    }


@router.get("/flood-extent", response_model=Dict[str, Any])
def get_flood_extent():
    """DEMO flood footprint. Do not interpret as observed Sentinel-1 flood mapping."""
    return {
        **FLOOD_EXTENT_SAR_GEOJSON,
        "data_mode": "DEMO",
        "source": "CLYMEX simulated extent; NOT an observed Sentinel-1 classification",
    }
