"""
CLYMEX AI - Domain Data Models & Schemas
"Predict Risk. Protect Tomorrow."
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    CRITICAL = "CRITICAL"


class HazardType(str, Enum):
    FLOOD = "FLOOD"
    DROUGHT = "DROUGHT"
    WATER_STRESS = "WATER_STRESS"
    OVERALL_CLIMATE = "OVERALL_CLIMATE"


class DataStatus(str, Enum):
    OBSERVED = "OBSERVED"
    ESTIMATED = "ESTIMATED"
    PREDICTED = "PREDICTED"
    DEMO = "DEMO"


class SensorStatus(str, Enum):
    ONLINE = "ONLINE"
    WARNING = "WARNING"
    ERROR = "ERROR"
    OFFLINE = "OFFLINE"


class DataProvenance(BaseModel):
    dataset_name: str
    source_agency: str
    acquisition_date: str
    spatial_resolution: str
    temporal_resolution: str
    processing_method: str
    data_mode: DataStatus = DataStatus.DEMO
    last_update: str
    license_info: str = "Open Access / Public Domain"


class ContributingFactor(BaseModel):
    factor_name: str
    metric_value: str
    weight: float
    contribution_pct: float
    description: str
    direction: str = "INCREASING_RISK"  # or DECREASING_RISK


class ExposureBreakdown(BaseModel):
    population_exposed: int
    population_density_per_sqkm: float
    buildings_count: int
    schools_count: int
    hospitals_count: int
    roads_km: float
    cropland_hectares: float
    critical_infrastructure: List[str] = Field(default_factory=list)


class EnvironmentalIndicators(BaseModel):
    rainfall_24h_mm: float
    rainfall_7d_mm: float
    rainfall_30d_mm: float
    rainfall_anomaly_pct: float
    ndvi_current: float
    ndvi_baseline: float
    ndvi_anomaly_pct: float
    soil_moisture_pct: float
    soil_moisture_anomaly_pct: float
    temperature_mean_c: float
    temperature_anomaly_c: float
    elevation_mean_m: float
    slope_mean_deg: float
    topographic_wetness_index: float
    distance_to_river_km: float
    surface_water_extent_sqkm: float
    surface_water_change_pct: float


class RiskAssessment(BaseModel):
    area_id: str
    area_name: str
    province: str
    country: str = "Mozambique"
    basin: str = "Incomati Basin"
    hazard_type: HazardType
    hazard_score: float = Field(..., ge=0.0, le=100.0)
    exposure_score: float = Field(..., ge=0.0, le=100.0)
    vulnerability_score: float = Field(..., ge=0.0, le=100.0)
    risk_score: float = Field(..., ge=0.0, le=100.0)
    risk_level: RiskLevel
    trend: str = "Stable"  # "Increasing", "Stable", "Decreasing"
    confidence_pct: float = Field(..., ge=0.0, le=100.0)
    primary_drivers: List[ContributingFactor]
    exposure: ExposureBreakdown
    indicators: EnvironmentalIndicators
    timestamp: str
    data_mode: DataStatus = DataStatus.DEMO


class AlertRecord(BaseModel):
    id: str
    hazard: HazardType
    title: str
    location: str
    province: str
    timestamp: str
    risk_level: RiskLevel
    trigger_condition: str
    affected_area_sqkm: float
    estimated_population_exposed: int
    confidence_pct: float
    recommended_action: str
    data_sources: List[str]
    is_active: bool = True
    disclaimer: str = (
        "CLYMEX AI early warning alerts are for decision-support and disaster risk reduction "
        "planning. They do not supersede official government emergency evacuation directives."
    )


class SensorTelemetry(BaseModel):
    sensor_id: str
    station_name: str
    basin: str
    latitude: float
    longitude: float
    elevation_m: float
    sensor_type: str  # WATER_LEVEL, RAINFALL, SOIL_MOISTURE, AIR_TEMPERATURE
    current_value: float
    unit: str
    status: SensorStatus
    battery_pct: float
    installation_date: str
    last_seen: str
    data_quality_score: float  # 0 to 100
    quality_flags: List[str] = Field(default_factory=list)


class SensorReading(BaseModel):
    reading_id: str
    sensor_id: str
    timestamp: str
    value: float
    battery: float
    signal_rssi: int
    is_valid: bool
    rejection_reason: Optional[str] = None


class TimeSeriesRecord(BaseModel):
    indicator: str
    unit: str
    temporal_scale: str  # 7d, 30d, 90d, 1y, 5y
    data_points: List[Dict[str, Any]]  # date, current, baseline, anomaly


class SituationReport(BaseModel):
    report_id: str
    generated_at: str
    title: str
    country: str
    region: str
    executive_summary: str
    overall_risk_score: float
    overall_risk_level: RiskLevel
    hazard_matrix: Dict[str, Dict[str, Any]]
    total_population_exposed: int
    total_buildings_exposed: int
    critical_infrastructure_count: int
    key_drivers: List[str]
    recommended_mitigation_actions: List[str]
    data_sources: List[DataProvenance]
    disclaimer: str
