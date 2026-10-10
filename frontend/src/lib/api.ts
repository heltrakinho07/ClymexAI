/**
 * CLYMEX AI - API Client & Data Types
 * Connects to FastAPI backend with graceful fallback for seamless demonstration.
 */

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface ContributingFactor {
  factor_name: string;
  metric_value: string;
  weight: number;
  contribution_pct: number;
  description: string;
  direction: string;
}

export interface ExposureBreakdown {
  population_exposed: number;
  population_density_per_sqkm: number;
  buildings_count: number;
  schools_count: number;
  hospitals_count: number;
  roads_km: number;
  cropland_hectares: number;
  critical_infrastructure: string[];
}

export interface EnvironmentalIndicators {
  rainfall_24h_mm: number;
  rainfall_7d_mm: number;
  rainfall_30d_mm: number;
  rainfall_anomaly_pct: number;
  ndvi_current: number;
  ndvi_baseline: number;
  ndvi_anomaly_pct: number;
  soil_moisture_pct: number;
  soil_moisture_anomaly_pct: number;
  temperature_mean_c: number;
  temperature_anomaly_c: number;
  elevation_mean_m: number;
  slope_mean_deg: number;
  topographic_wetness_index: number;
  distance_to_river_km: number;
  surface_water_extent_sqkm: number;
  surface_water_change_pct: number;
}

export interface RiskAssessment {
  area_id: string;
  area_name: string;
  province: string;
  country: string;
  basin: string;
  hazard_type: "FLOOD" | "DROUGHT" | "WATER_STRESS" | "OVERALL_CLIMATE";
  hazard_score: number;
  exposure_score: number;
  vulnerability_score: number;
  risk_score: number;
  risk_level: "LOW" | "MODERATE" | "HIGH" | "VERY_HIGH" | "CRITICAL";
  trend: string;
  confidence_pct: number;
  primary_drivers: ContributingFactor[];
  exposure: ExposureBreakdown;
  indicators: EnvironmentalIndicators;
  timestamp: string;
  data_mode: string;
}

export interface AlertRecord {
  id: string;
  hazard: "FLOOD" | "DROUGHT" | "WATER_STRESS" | "OVERALL_CLIMATE";
  title: string;
  location: string;
  province: string;
  timestamp: string;
  risk_level: "LOW" | "MODERATE" | "HIGH" | "VERY_HIGH" | "CRITICAL";
  trigger_condition: string;
  affected_area_sqkm: number;
  estimated_population_exposed: number;
  confidence_pct: number;
  recommended_action: string;
  data_sources: string[];
  is_active: boolean;
  disclaimer: string;
}

export interface SensorTelemetry {
  sensor_id: string;
  station_name: string;
  basin: string;
  latitude: number;
  longitude: number;
  elevation_m: number;
  sensor_type: string;
  current_value: number;
  unit: string;
  status: "ONLINE" | "WARNING" | "ERROR" | "OFFLINE";
  battery_pct: number;
  installation_date: string;
  last_seen: string;
  data_quality_score: number;
  quality_flags: string[];
}

export interface DataProvenance {
  dataset_name: string;
  source_agency: string;
  acquisition_date: string;
  spatial_resolution: string;
  temporal_resolution: string;
  processing_method: string;
  data_mode: string;
  last_update: string;
  license_info: string;
}

export interface SituationReport {
  report_id: string;
  generated_at: string;
  title: string;
  country: string;
  region: string;
  executive_summary: string;
  overall_risk_score: number;
  overall_risk_level: string;
  hazard_matrix: Record<string, any>;
  total_population_exposed: number;
  total_buildings_exposed: number;
  critical_infrastructure_count: number;
  key_drivers: string[];
  recommended_mitigation_actions: string[];
  data_sources: DataProvenance[];
  disclaimer: string;
}

export async function fetchApi<T>(endpoint: string, fallbackData: T): Promise<T> {
  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, { cache: "no-store" });
    if (!res.ok) {
      return fallbackData;
    }
    return await res.json();
  } catch (err) {
    console.warn(`Fallback active for ${endpoint}:`, err);
    return fallbackData;
  }
}
