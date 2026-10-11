"""Offline contract checks for the Earth Engine processor."""
import datetime as dt

import pytest
from fastapi import HTTPException

from app.services.gee_processing import (
    DATASETS,
    EarthEngineProcessor,
    district_geometry,
    validate_window,
)


def test_registry_points_to_processing_collections():
    assert DATASETS["ndvi"] == "COPERNICUS/S2_SR_HARMONIZED"
    assert DATASETS["flood_sar"] == "COPERNICUS/S1_GRD"
    assert DATASETS["precipitation"] == "UCSB-CHG/CHIRPS/DAILY"
    assert DATASETS["elevation"] == "COPERNICUS/DEM/GLO30"


@pytest.mark.parametrize(
    "start,end",
    [
        ("2026-01-01", "2026-01-01"),
        ("2026-01-03", "2026-01-01"),
        ("2024-01-01", "2026-01-02"),
        ("invalid", "2026-02-01"),
        ("2026-01-01", "2027-01-01"),
    ],
)
def test_rejects_invalid_observation_dates(start, end):
    with pytest.raises(HTTPException) as exc:
        validate_window(start, end)
    assert exc.value.status_code == 422


def test_valid_interval_is_exclusive():
    assert validate_window("2024-05-01", "2024-05-31") == (
        dt.date(2024, 5, 1),
        dt.date(2024, 5, 31),
    )


def test_district_geometry_uses_geomoz_polygon_not_bounding_box(monkeypatch):
    polygon = {
        "type": "MultiPolygon",
        "coordinates": [
            [[
                [32.1, -25.1], [32.2, -25.1], [32.3, -25.2], [32.1, -25.1]
            ]]
        ],
    }
    monkeypatch.setattr(
        "app.services.gee_processing.districts_geojson",
        lambda focus_only=False: {
            "features": [{"id": "manhica", "geometry": polygon}]
        },
    )
    district_geometry.cache_clear()
    assert district_geometry("manhica") is polygon
    with pytest.raises(HTTPException) as exc:
        district_geometry("not_a_district")
    assert exc.value.status_code == 404
    district_geometry.cache_clear()


def test_invalid_index_does_not_initialize_earth_engine():
    with pytest.raises(HTTPException) as exc:
        EarthEngineProcessor.compute(
            "not_an_index", "manhica", "2024-05-01", "2024-05-31"
        )
    assert exc.value.status_code == 422
