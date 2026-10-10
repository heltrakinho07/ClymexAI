"""
CLYMEX AI - Historical Baseline Records, Metadata Provenance & Sensor Stations
Authoritative environmental and sensor data for Mozambique / Incomati Basin.
"""

from typing import Dict, Any, List
from app.models.domain import DataProvenance, DataStatus, SensorTelemetry, SensorStatus

# 1. Authoritative Data Sources & Provenance Metadata
DATA_PROVENANCE_CATALOG: List[DataProvenance] = [
    DataProvenance(
        dataset_name="Sentinel-1 C-SAR GRD",
        source_agency="European Space Agency (ESA) Copernicus",
        acquisition_date="2026-09-17T05:32:00Z",
        spatial_resolution="10 meters",
        temporal_resolution="6-12 days revisit",
        processing_method="Thermal noise removal, radiometric calibration, terrain correction, Lee speckle filtering, VV/VH backscatter change thresholding",
        data_mode=DataStatus.DEMO,
        last_update="2026-09-17T08:00:00Z",
        license_info="Copernicus Open Access / CC-BY 4.0"
    ),
    DataProvenance(
        dataset_name="Sentinel-2 MSI Level-2A BOA",
        source_agency="European Space Agency (ESA) Copernicus",
        acquisition_date="2026-09-16T08:14:00Z",
        spatial_resolution="10-20 meters",
        temporal_resolution="5 days revisit",
        processing_method="Atmospheric correction (Sen2Cor), SCL cloud masking, NDVI (NIR-Red)/(NIR+Red), NDWI (Green-NIR)/(Green+NIR)",
        data_mode=DataStatus.DEMO,
        last_update="2026-09-16T12:00:00Z",
        license_info="Copernicus Open Access / CC-BY 4.0"
    ),
    DataProvenance(
        dataset_name="CHIRPS v2.0 Quasi-Global Rainfall",
        source_agency="Climate Hazards Center, UC Santa Barbara / USGS",
        acquisition_date="2026-09-17T00:00:00Z",
        spatial_resolution="0.05° (~5.3 km)",
        temporal_resolution="Daily",
        processing_method="Satellite cold cloud duration (CCD) calibrated against in-situ WMO rain gauges, pentad anomaly calculation",
        data_mode=DataStatus.DEMO,
        last_update="2026-09-17T06:00:00Z",
        license_info="Public Domain / Open Data"
    ),
    DataProvenance(
        dataset_name="ERA5-Land Reanalysis",
        source_agency="European Centre for Medium-Range Weather Forecasts (ECMWF)",
        acquisition_date="2026-09-17T00:00:00Z",
        spatial_resolution="0.1° (~9 km)",
        temporal_resolution="Hourly / Daily",
        processing_method="Numerical weather model assimilation, 2m air temperature, 4-layer volumetric soil water layer 1 (0-7cm)",
        data_mode=DataStatus.DEMO,
        last_update="2026-09-17T07:30:00Z",
        license_info="Copernicus Climate Change Service (C3S)"
    ),
    DataProvenance(
        dataset_name="Copernicus DEM GLO-30",
        source_agency="ESA / Airbus Defence and Space",
        acquisition_date="2024-01-01T00:00:00Z",
        spatial_resolution="30 meters",
        temporal_resolution="Static Digital Elevation Model",
        processing_method="WorldSRTM gap-filled with TanDEM-X interferometry, hydrologically conditioned, D8 flow direction and Topographic Wetness Index (TWI)",
        data_mode=DataStatus.DEMO,
        last_update="2024-06-01T00:00:00Z",
        license_info="Copernicus Open Access"
    ),
    DataProvenance(
        dataset_name="Google Open Buildings v3",
        source_agency="Google Research Africa / AI for Social Good",
        acquisition_date="2024-05-15T00:00:00Z",
        spatial_resolution="Sub-meter satellite AI segmentation",
        temporal_resolution="Annual update",
        processing_method="Deep convolutional neural network building footprint extraction, fractional building presence score > 0.65",
        data_mode=DataStatus.DEMO,
        last_update="2024-10-01T00:00:00Z",
        license_info="Creative Commons Attribution (CC BY 4.0)"
    ),
    DataProvenance(
        dataset_name="WorldPop High Resolution Population",
        source_agency="WorldPop / University of Southampton",
        acquisition_date="2025-01-01T00:00:00Z",
        spatial_resolution="100 meters (1 hectare)",
        temporal_resolution="Annual constrained estimate",
        processing_method="Random forest dasymetric population disaggregation weighted by building density and road networks",
        data_mode=DataStatus.DEMO,
        last_update="2025-04-01T00:00:00Z",
        license_info="CC-BY 4.0 International"
    )
]

# 2. Environmental Sensor Stations in the Incomati Basin (Phase 2 IoT Ready)
SENSOR_STATIONS_DATA: List[SensorTelemetry] = [
    SensorTelemetry(
        sensor_id="INC-MAG-01",
        station_name="Estação Hidrométrica Magude (E-32)",
        basin="Incomati Basin",
        latitude=-25.024,
        longitude=32.652,
        elevation_m=42.0,
        sensor_type="WATER_LEVEL",
        current_value=4.85,
        unit="m",
        status=SensorStatus.ONLINE,
        battery_pct=92.0,
        installation_date="2025-03-10",
        last_seen="2026-09-17T23:55:00Z",
        data_quality_score=98.5,
        quality_flags=["VALID_RANGE", "TELEMETRY_SYNCED"]
    ),
    SensorTelemetry(
        sensor_id="INC-MAN-02",
        station_name="Estação Manhiça Ponte EN1 (E-33)",
        basin="Incomati Basin",
        latitude=-25.405,
        longitude=32.808,
        elevation_m=12.5,
        sensor_type="WATER_LEVEL",
        current_value=6.12,  # Above flood alert threshold (6.0m)
        unit="m",
        status=SensorStatus.WARNING,
        battery_pct=88.0,
        installation_date="2025-03-12",
        last_seen="2026-09-17T23:58:00Z",
        data_quality_score=94.0,
        quality_flags=["STAGE_ALERT_EXCEEDED", "RAPID_RISE"]
    ),
    SensorTelemetry(
        sensor_id="INC-MAR-03",
        station_name="Estação Marracuene Estuário (E-34)",
        basin="Incomati Basin",
        latitude=-25.718,
        longitude=32.679,
        elevation_m=4.2,
        sensor_type="WATER_LEVEL",
        current_value=3.45,
        unit="m",
        status=SensorStatus.ONLINE,
        battery_pct=84.0,
        installation_date="2025-04-01",
        last_seen="2026-09-17T23:50:00Z",
        data_quality_score=96.0,
        quality_flags=["VALID_RANGE", "TIDAL_COMPENSATED"]
    ),
    SensorTelemetry(
        sensor_id="COR-DAM-04",
        station_name="Barragem de Corumana - Vertedouro",
        basin="Rio Sábiè / Incomati",
        latitude=-25.215,
        longitude=32.128,
        elevation_m=115.0,
        sensor_type="RESERVOIR_OUTFLOW",
        current_value=320.0,
        unit="m³/s",
        status=SensorStatus.ONLINE,
        battery_pct=99.0,
        installation_date="2024-11-20",
        last_seen="2026-09-17T23:59:00Z",
        data_quality_score=99.0,
        quality_flags=["OPERATIONAL_OPTIMAL"]
    ),
    SensorTelemetry(
        sensor_id="PL-BOA-05",
        station_name="Barragem Pequenos Libombos - Efluente",
        basin="Rio Umbeluzi",
        latitude=-26.002,
        longitude=32.185,
        elevation_m=48.0,
        sensor_type="RESERVOIR_STORAGE",
        current_value=54.2,
        unit="%",
        status=SensorStatus.ONLINE,
        battery_pct=91.0,
        installation_date="2024-10-15",
        last_seen="2026-09-17T23:45:00Z",
        data_quality_score=97.5,
        quality_flags=["STORAGE_MODERATE"]
    ),
    SensorTelemetry(
        sensor_id="MET-MAN-06",
        station_name="Estação Meteorológica e Pluviométrica Manhiça",
        basin="Incomati Basin",
        latitude=-25.398,
        longitude=32.795,
        elevation_m=22.0,
        sensor_type="RAINFALL",
        current_value=64.5,
        unit="mm/24h",
        status=SensorStatus.ONLINE,
        battery_pct=95.0,
        installation_date="2025-05-18",
        last_seen="2026-09-17T23:56:00Z",
        data_quality_score=99.2,
        quality_flags=["HEAVY_PRECIPITATION"]
    ),
    SensorTelemetry(
        sensor_id="AGR-MAG-07",
        station_name="Estação Agrometeorológica Magude (Solo)",
        basin="Upper Incomati",
        latitude=-24.980,
        longitude=32.610,
        elevation_m=58.0,
        sensor_type="SOIL_MOISTURE",
        current_value=16.8,
        unit="%",
        status=SensorStatus.WARNING,
        battery_pct=65.0,
        installation_date="2025-06-05",
        last_seen="2026-09-17T23:10:00Z",
        data_quality_score=82.0,
        quality_flags=["MOISTURE_DEFICIT", "DROUGHT_VULNERABILITY"]
    )
]

# 3. Multi-temporal Historical Series for Key Indicators (30 days daily sample)
def get_mock_timeseries(indicator: str, district: str = "manhica") -> List[Dict[str, Any]]:
    import datetime
    
    base_date = datetime.date(2026, 9, 17)
    points = []
    
    # 30-day simulated trend leading up to recent rainfall surge in September 2026
    for i in range(29, -1, -1):
        day = base_date - datetime.timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        
        if indicator == "rainfall":
            baseline = 2.4 + (i % 3) * 0.5
            if i < 4:
                # Extreme rainfall event in last 4 days
                actual = [22.0, 58.4, 76.2, 64.5][3 - i]
            elif i < 7:
                actual = 14.5 + i * 1.2
            else:
                actual = max(0.0, baseline + ((i * 7) % 5) - 2.0)
            anomaly = ((actual - baseline) / max(baseline, 1.0)) * 100
            points.append({
                "date": day_str,
                "actual": round(actual, 1),
                "baseline": round(baseline, 1),
                "anomaly_pct": round(anomaly, 1),
                "unit": "mm"
            })
            
        elif indicator == "ndvi":
            # Normalized Difference Vegetation Index
            baseline = 0.58
            # In drought or flooded zone, slight drop or rise
            actual = round(0.54 - (i * 0.002) if district == "magude" else 0.62 + (i * 0.001), 3)
            anomaly = round(((actual - baseline) / baseline) * 100, 1)
            points.append({
                "date": day_str,
                "actual": actual,
                "baseline": baseline,
                "anomaly_pct": anomaly,
                "unit": "index (-1 to 1)"
            })
            
        elif indicator == "soil_moisture":
            baseline = 24.0
            if district in ["manhica", "marracuene"]:
                # Saturated soil from heavy rains
                actual = round(min(45.0, 26.0 + (30 - i) * 0.6), 1)
            else:
                # Deficit in interior Magude
                actual = round(max(12.0, 22.0 - (30 - i) * 0.3), 1)
            anomaly = round(((actual - baseline) / baseline) * 100, 1)
            points.append({
                "date": day_str,
                "actual": actual,
                "baseline": baseline,
                "anomaly_pct": anomaly,
                "unit": "%"
            })
            
        elif indicator == "river_stage":
            baseline = 2.8
            if i < 4:
                actual = round([4.1, 5.2, 5.85, 6.12][3 - i], 2)
            else:
                actual = round(2.6 + (30 - i) * 0.05, 2)
            anomaly = round(((actual - baseline) / baseline) * 100, 1)
            points.append({
                "date": day_str,
                "actual": actual,
                "baseline": baseline,
                "anomaly_pct": anomaly,
                "unit": "m"
            })
            
    return points
