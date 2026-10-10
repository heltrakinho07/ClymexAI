"""
CLYMEX AI - Automated Unit & API Integration Tests
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.risk_engine import ClimateRiskEngine
from app.services.flood_engine import FloodEngine
from app.services.drought_engine import DroughtEngine
from app.services.water_stress_engine import WaterStressEngine
from app.services.exposure_engine import ExposureEngine
from app.models.domain import HazardType, RiskLevel, EnvironmentalIndicators


def test_flood_engine_calculation():
    indicators = EnvironmentalIndicators(
        rainfall_24h_mm=60.0,
        rainfall_7d_mm=140.0,
        rainfall_30d_mm=220.0,
        rainfall_anomaly_pct=110.0,
        ndvi_current=0.65,
        ndvi_baseline=0.55,
        ndvi_anomaly_pct=18.0,
        soil_moisture_pct=38.0,
        soil_moisture_anomaly_pct=60.0,
        temperature_mean_c=24.5,
        temperature_anomaly_c=-0.5,
        elevation_mean_m=14.0,
        slope_mean_deg=1.0,
        topographic_wetness_index=12.5,
        distance_to_river_km=1.0,
        surface_water_extent_sqkm=45.0,
        surface_water_change_pct=65.0
    )
    hazard_score, drivers = FloodEngine.calculate_hazard("manhica", indicators)
    assert 0.0 <= hazard_score <= 100.0
    assert hazard_score > 60.0  # High flood conditions
    assert len(drivers) == 4
    for d in drivers:
        assert d.contribution_pct >= 0


def test_risk_classification():
    assert ClimateRiskEngine.classify_risk_level(15.0) == RiskLevel.LOW
    assert ClimateRiskEngine.classify_risk_level(35.0) == RiskLevel.MODERATE
    assert ClimateRiskEngine.classify_risk_level(55.0) == RiskLevel.HIGH
    assert ClimateRiskEngine.classify_risk_level(75.0) == RiskLevel.VERY_HIGH
    assert ClimateRiskEngine.classify_risk_level(90.0) == RiskLevel.CRITICAL


def test_exposure_engine_polygon():
    # Triangle covering parts of Incomati valley
    polygon = [
        [32.65, -25.20],
        [32.95, -25.15],
        [32.90, -25.65],
        [32.65, -25.20]
    ]
    exposure = ExposureEngine.calculate_custom_polygon_exposure(polygon)
    assert exposure.population_exposed > 0
    assert exposure.buildings_count > 0
    assert exposure.roads_km > 0


@pytest.mark.asyncio
async def test_api_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Healthcheck
        res = await client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"

        # 2. Risk Overview
        res = await client.get("/api/v1/risk?mode=demo")
        assert res.status_code == 200
        risks = res.json()
        assert len(risks) >= 6
        assert any(r["area_id"] == "manhica" for r in risks)

        # 3. Specific District Risk (Manhiça)
        res = await client.get("/api/v1/risk/manhica?mode=demo")
        assert res.status_code == 200
        data = res.json()
        assert data["area_name"] == "Manhiça"
        assert data["risk_score"] > 0
        assert "primary_drivers" in data

        # 4. Areas GeoJSON
        res = await client.get("/api/v1/areas")
        assert res.status_code == 200
        geojson = res.json()
        assert geojson["type"] == "FeatureCollection"
        assert geojson["source"] == "geomoz"
    assert len(geojson["features"]) >= 6

        # 5. Alerts
        res = await client.get("/api/v1/alerts")
        assert res.status_code == 200
        alerts = res.json()
        assert len(alerts) > 0

        # 6. Sensors
        res = await client.get("/api/v1/sensors")
        assert res.status_code == 200
        sensors = res.json()
        assert len(sensors) >= 5

        # 7. Situation Report
        res = await client.get("/api/v1/reports/manhica")
        assert res.status_code == 200
        sitrep = res.json()
        assert "report_id" in sitrep
        assert "executive_summary" in sitrep

        # 8. Google Earth Engine (GEE) Status & Tile Generation
        res = await client.get("/api/v1/satellite/gee/status")
        assert res.status_code == 200
        gee_status = res.json()
        assert "connected" in gee_status
        assert gee_status["project_id"] == "geoprocessamento-426809"
        assert "ndvi" in gee_status["indices"]

        # 9. GEE Tile Computation
        res = await client.post(
            "/api/v1/satellite/gee/tile",
            json={"index": "ndvi", "district_id": "manhica"}
        )
        assert res.status_code == 200
        tile_data = res.json()
        assert "tile_url" in tile_data
        assert tile_data["tile_url"].startswith("http")
        assert "attribution" in tile_data

        # 10. District Satellite Metrics
        res = await client.get("/api/v1/satellite/gee/metrics/manhica")
        assert res.status_code == 200
        sat_metrics = res.json()
        assert "ndvi_mean" in sat_metrics
        assert "sar_flood_inundated_sqkm" in sat_metrics
