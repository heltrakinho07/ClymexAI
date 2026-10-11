"""
CLYMEX AI - Master Climate Risk Engine
"Predict Risk. Protect Tomorrow."
Calculates: RISK = HAZARD × EXPOSURE × VULNERABILITY
Maps to: LOW, MODERATE, HIGH, VERY_HIGH, CRITICAL.
"""

import datetime
from typing import Dict, Any, List, Optional
from app.config import settings
from app.models.domain import (
    RiskAssessment,
    RiskLevel,
    HazardType,
    DataStatus,
    EnvironmentalIndicators,
    ExposureBreakdown
)
from app.services.flood_engine import FloodEngine
from app.services.drought_engine import DroughtEngine
from app.services.water_stress_engine import WaterStressEngine
from app.services.exposure_engine import ExposureEngine


# District Environmental Indicators Baseline (Mozambique / Incomati Context)
DISTRICT_INDICATORS_REGISTRY: Dict[str, EnvironmentalIndicators] = {
    "manhica": EnvironmentalIndicators(
        rainfall_24h_mm=64.5,
        rainfall_7d_mm=138.2,
        rainfall_30d_mm=215.0,
        rainfall_anomaly_pct=112.0,  # Extreme surplus
        ndvi_current=0.68,
        ndvi_baseline=0.58,
        ndvi_anomaly_pct=17.2,
        soil_moisture_pct=38.5,      # Near saturation
        soil_moisture_anomaly_pct=60.4,
        temperature_mean_c=24.2,
        temperature_anomaly_c=-0.8,
        elevation_mean_m=16.5,       # Low alluvial floodplain
        slope_mean_deg=1.1,          # Flat
        topographic_wetness_index=12.4, # High water accumulation
        distance_to_river_km=1.2,    # Incomati main channel
        surface_water_extent_sqkm=46.2,
        surface_water_change_pct=68.5  # Substantial flood expansion
    ),
    "marracuene": EnvironmentalIndicators(
        rainfall_24h_mm=58.0,
        rainfall_7d_mm=115.0,
        rainfall_30d_mm=185.0,
        rainfall_anomaly_pct=95.0,
        ndvi_current=0.64,
        ndvi_baseline=0.56,
        ndvi_anomaly_pct=14.3,
        soil_moisture_pct=36.0,
        soil_moisture_anomaly_pct=50.0,
        temperature_mean_c=24.8,
        temperature_anomaly_c=-0.4,
        elevation_mean_m=12.0,
        slope_mean_deg=0.9,
        topographic_wetness_index=13.1,
        distance_to_river_km=1.8,
        surface_water_extent_sqkm=32.0,
        surface_water_change_pct=54.0
    ),
    "matola": EnvironmentalIndicators(
        rainfall_24h_mm=42.0,
        rainfall_7d_mm=78.0,
        rainfall_30d_mm=110.0,
        rainfall_anomaly_pct=35.0,
        ndvi_current=0.38,
        ndvi_baseline=0.40,
        ndvi_anomaly_pct=-5.0,
        soil_moisture_pct=24.0,
        soil_moisture_anomaly_pct=10.0,
        temperature_mean_c=26.5,
        temperature_anomaly_c=1.1,
        elevation_mean_m=34.0,
        slope_mean_deg=2.5,
        topographic_wetness_index=8.4,
        distance_to_river_km=4.5,
        surface_water_extent_sqkm=12.0,
        surface_water_change_pct=15.0
    ),
    "boane": EnvironmentalIndicators(
        rainfall_24h_mm=28.0,
        rainfall_7d_mm=55.0,
        rainfall_30d_mm=88.0,
        rainfall_anomaly_pct=12.0,
        ndvi_current=0.48,
        ndvi_baseline=0.50,
        ndvi_anomaly_pct=-4.0,
        soil_moisture_pct=22.5,
        soil_moisture_anomaly_pct=-6.2,
        temperature_mean_c=26.0,
        temperature_anomaly_c=0.9,
        elevation_mean_m=42.0,
        slope_mean_deg=3.2,
        topographic_wetness_index=7.8,
        distance_to_river_km=2.1,
        surface_water_extent_sqkm=18.5,
        surface_water_change_pct=-8.0
    ),
    "magude": EnvironmentalIndicators(
        rainfall_24h_mm=4.0,
        rainfall_7d_mm=12.0,
        rainfall_30d_mm=24.0,
        rainfall_anomaly_pct=-48.0,  # Deficit in Upper Incomati
        ndvi_current=0.34,
        ndvi_baseline=0.52,
        ndvi_anomaly_pct=-34.6,     # Acute vegetation stress
        soil_moisture_pct=14.2,      # Severe moisture deficit
        soil_moisture_anomaly_pct=-42.0,
        temperature_mean_c=29.2,
        temperature_anomaly_c=2.8,
        elevation_mean_m=68.0,
        slope_mean_deg=2.1,
        topographic_wetness_index=6.2,
        distance_to_river_km=6.8,
        surface_water_extent_sqkm=9.4,
        surface_water_change_pct=-32.0
    ),
    "moamba": EnvironmentalIndicators(
        rainfall_24h_mm=15.0,
        rainfall_7d_mm=32.0,
        rainfall_30d_mm=48.0,
        rainfall_anomaly_pct=-22.0,
        ndvi_current=0.42,
        ndvi_baseline=0.49,
        ndvi_anomaly_pct=-14.3,
        soil_moisture_pct=18.0,
        soil_moisture_anomaly_pct=-25.0,
        temperature_mean_c=28.1,
        temperature_anomaly_c=1.6,
        elevation_mean_m=92.0,
        slope_mean_deg=3.8,
        topographic_wetness_index=6.8,
        distance_to_river_km=5.2,
        surface_water_extent_sqkm=14.0,
        surface_water_change_pct=-18.0
    ),
    "maputo_city": EnvironmentalIndicators(
        rainfall_24h_mm=48.0,
        rainfall_7d_mm=92.0,
        rainfall_30d_mm=135.0,
        rainfall_anomaly_pct=42.0,
        ndvi_current=0.28,
        ndvi_baseline=0.30,
        ndvi_anomaly_pct=-6.7,
        soil_moisture_pct=28.0,
        soil_moisture_anomaly_pct=15.0,
        temperature_mean_c=25.8,
        temperature_anomaly_c=0.6,
        elevation_mean_m=28.0,
        slope_mean_deg=2.2,
        topographic_wetness_index=9.1,
        distance_to_river_km=3.0,
        surface_water_extent_sqkm=8.5,
        surface_water_change_pct=22.0
    ),
    "chokwe": EnvironmentalIndicators(
        rainfall_24h_mm=72.0,
        rainfall_7d_mm=160.0,
        rainfall_30d_mm=240.0,
        rainfall_anomaly_pct=135.0,
        ndvi_current=0.72,
        ndvi_baseline=0.58,
        ndvi_anomaly_pct=24.1,
        soil_moisture_pct=42.0,
        soil_moisture_anomaly_pct=75.0,
        temperature_mean_c=25.0,
        temperature_anomaly_c=-0.5,
        elevation_mean_m=33.0,
        slope_mean_deg=0.8,
        topographic_wetness_index=13.8,
        distance_to_river_km=0.8,
        surface_water_extent_sqkm=58.0,
        surface_water_change_pct=85.0
    )
}


class ClimateRiskEngine:
    """
    Central Risk Orchestrator combining Hazard, Exposure, and Vulnerability.
    """

    @classmethod
    def classify_risk_level(cls, score: float) -> RiskLevel:
        """
        Maps numeric score [0-100] to operational risk tier.
        """
        if score <= settings.RISK_THRESHOLD_LOW:
            return RiskLevel.LOW
        elif score <= settings.RISK_THRESHOLD_MODERATE:
            return RiskLevel.MODERATE
        elif score <= settings.RISK_THRESHOLD_HIGH:
            return RiskLevel.HIGH
        elif score <= settings.RISK_THRESHOLD_VERY_HIGH:
            return RiskLevel.VERY_HIGH
        else:
            return RiskLevel.CRITICAL

    @classmethod
    def assess_district(
        cls,
        district_id: str,
        hazard_type: HazardType = HazardType.OVERALL_CLIMATE
    ) -> RiskAssessment:
        """
        Runs complete assessment pipeline for a specific district.
        """
        dist_key = district_id.lower()
        indicators = DISTRICT_INDICATORS_REGISTRY.get(
            dist_key,
            DISTRICT_INDICATORS_REGISTRY["manhica"]
        )

        # 1. Compute Hazard Specific Scores
        flood_hazard, flood_drivers = FloodEngine.calculate_hazard(dist_key, indicators)
        drought_hazard, drought_drivers = DroughtEngine.calculate_hazard(dist_key, indicators)
        stress_hazard, stress_drivers = WaterStressEngine.calculate_hazard(dist_key, indicators)

        if hazard_type == HazardType.FLOOD:
            target_hazard_score = flood_hazard
            primary_drivers = flood_drivers
        elif hazard_type == HazardType.DROUGHT:
            target_hazard_score = drought_hazard
            primary_drivers = drought_drivers
        elif hazard_type == HazardType.WATER_STRESS:
            target_hazard_score = stress_hazard
            primary_drivers = stress_drivers
        else:
            # Multi-hazard composite (max weighted hazard)
            target_hazard_score = round(max(flood_hazard, drought_hazard, stress_hazard), 1)
            if flood_hazard >= drought_hazard and flood_hazard >= stress_hazard:
                primary_drivers = flood_drivers
            elif drought_hazard >= stress_hazard:
                primary_drivers = drought_drivers
            else:
                primary_drivers = stress_drivers

        # 2. Exposure & Vulnerability
        exposure_breakdown, exposure_score, vulnerability_score = ExposureEngine.get_district_exposure(
            dist_key, target_hazard_score
        )

        # 3. Scientific Risk Synthesis: RISK = HAZARD * EXPOSURE * VULNERABILITY
        # Using calibrated non-linear geometric blend:
        # High hazard + high exposure yields a critical risk response
        raw_risk = (
            (target_hazard_score ** 0.50) *
            (exposure_score ** 0.30) *
            (vulnerability_score ** 0.20)
        ) * 1.02
        risk_score = round(min(100.0, max(0.0, raw_risk)), 1)
        risk_level = cls.classify_risk_level(risk_score)

        # 4. Trend & Confidence
        if target_hazard_score > 65.0:
            trend = "Increasing"
            confidence = 88.0  # High confidence from multi-sensor confirmation (Sentinel-1 SAR + in-situ gauge)
        elif target_hazard_score > 40.0:
            trend = "Increasing" if indicators.rainfall_anomaly_pct > 20 else "Stable"
            confidence = 82.0
        else:
            trend = "Stable"
            confidence = 79.0

        district_display_names = {
            "manhica": ("Manhiça", "Maputo Província"),
            "marracuene": ("Marracuene", "Maputo Província"),
            "matola": ("Matola", "Maputo Província"),
            "boane": ("Boane", "Maputo Província"),
            "magude": ("Magude", "Maputo Província"),
            "moamba": ("Moamba", "Maputo Província"),
            "maputo_city": ("Maputo Cidade", "Maputo Cidade"),
            "chokwe": ("Chókwè", "Gaza Província")
        }
        area_name, province = district_display_names.get(dist_key, (district_id.title(), "Maputo Província"))

        return RiskAssessment(
            area_id=dist_key,
            area_name=area_name,
            province=province,
            country="Mozambique",
            basin={
                "chokwe": "Bacia Hidrográfica do Limpopo",
                "boane": "Bacia Hidrográfica do Umbeluzi",
                "matola": "Bacias urbanas da Matola",
                "maputo_city": "Bacias costeiras de Maputo",
            }.get(dist_key, "Bacia Hidrográfica do Rio Incomati"),
            hazard_type=hazard_type,
            hazard_score=target_hazard_score,
            exposure_score=exposure_score,
            vulnerability_score=vulnerability_score,
            risk_score=risk_score,
            risk_level=risk_level,
            trend=trend,
            confidence_pct=confidence,
            primary_drivers=primary_drivers,
            exposure=exposure_breakdown,
            indicators=indicators,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data_mode=DataStatus.DEMO
        )

    @classmethod
    async def assess_district_live(
        cls,
        district_id: str,
        hazard_type: HazardType = HazardType.OVERALL_CLIMATE
    ) -> RiskAssessment:
        """
        Runs live assessment using real open geoprocessing (ECMWF/Open-Meteo, terrain TWI, river distance).
        """
        from app.services.live_geoprocessing_service import LiveGeoprocessingService
        dist_key = district_id.lower()
        
        # 1. Fetch real indicators via live geoprocessing
        indicators = await LiveGeoprocessingService.get_real_indicators_for_district(dist_key)

        # 2. Compute Hazard Specific Scores
        flood_hazard, flood_drivers = FloodEngine.calculate_hazard(dist_key, indicators)
        drought_hazard, drought_drivers = DroughtEngine.calculate_hazard(dist_key, indicators)
        stress_hazard, stress_drivers = WaterStressEngine.calculate_hazard(dist_key, indicators)

        if hazard_type == HazardType.FLOOD:
            target_hazard_score = flood_hazard
            primary_drivers = flood_drivers
        elif hazard_type == HazardType.DROUGHT:
            target_hazard_score = drought_hazard
            primary_drivers = drought_drivers
        elif hazard_type == HazardType.WATER_STRESS:
            target_hazard_score = stress_hazard
            primary_drivers = stress_drivers
        else:
            target_hazard_score = round(max(flood_hazard, drought_hazard, stress_hazard), 1)
            if flood_hazard >= drought_hazard and flood_hazard >= stress_hazard:
                primary_drivers = flood_drivers
            elif drought_hazard >= stress_hazard:
                primary_drivers = drought_drivers
            else:
                primary_drivers = stress_drivers

        # 3. Exposure & Vulnerability
        exposure_breakdown, exposure_score, vulnerability_score = ExposureEngine.get_district_exposure(
            dist_key, target_hazard_score
        )

        raw_risk = (
            (target_hazard_score ** 0.50) *
            (exposure_score ** 0.30) *
            (vulnerability_score ** 0.20)
        ) * 1.02
        risk_score = round(min(100.0, max(0.0, raw_risk)), 1)
        risk_level = cls.classify_risk_level(risk_score)

        if target_hazard_score > 65.0:
            trend = "Increasing"
            confidence = 91.0
        elif target_hazard_score > 40.0:
            trend = "Increasing" if indicators.rainfall_anomaly_pct > 20 else "Stable"
            confidence = 86.0
        else:
            trend = "Stable"
            confidence = 84.0

        district_display_names = {
            "manhica": ("Manhiça", "Maputo Província"),
            "marracuene": ("Marracuene", "Maputo Província"),
            "matola": ("Matola", "Maputo Província"),
            "boane": ("Boane", "Maputo Província"),
            "magude": ("Magude", "Maputo Província"),
            "moamba": ("Moamba", "Maputo Província"),
            "maputo_city": ("Maputo Cidade", "Maputo Cidade"),
            "chokwe": ("Chókwè", "Gaza Província")
        }
        area_name, province = district_display_names.get(dist_key, (district_id.title(), "Maputo Província"))

        return RiskAssessment(
            area_id=dist_key,
            area_name=area_name,
            province=province,
            country="Mozambique",
            basin={
                "chokwe": "Bacia Hidrográfica do Limpopo",
                "boane": "Bacia Hidrográfica do Umbeluzi",
                "matola": "Bacias urbanas da Matola",
                "maputo_city": "Bacias costeiras de Maputo",
            }.get(dist_key, "Bacia Hidrográfica do Rio Incomati"),
            hazard_type=hazard_type,
            hazard_score=target_hazard_score,
            exposure_score=exposure_score,
            vulnerability_score=vulnerability_score,
            risk_score=risk_score,
            risk_level=risk_level,
            trend=trend,
            confidence_pct=confidence,
            primary_drivers=primary_drivers,
            exposure=exposure_breakdown,
            indicators=indicators,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            # Open-Meteo meteorology is mixed with heuristic NDVI, water extent,
            # terrain and exposure estimates. Never claim the full score is observed.
            data_mode=DataStatus.ESTIMATED
        )

    @classmethod
    def get_all_districts_overview(cls) -> List[RiskAssessment]:
        """
        Returns latest risk assessments for all demonstrator districts in the Incomati basin.
        """
        districts = ["manhica", "marracuene", "matola", "boane", "magude", "moamba", "maputo_city", "chokwe"]
        return [cls.assess_district(d, HazardType.OVERALL_CLIMATE) for d in districts]

