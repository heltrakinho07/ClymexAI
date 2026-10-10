"""
CLYMEX AI - Flood Risk Engine
Combines CHIRPS/ERA5 rainfall, Copernicus DEM GLO-30, TWI, and Sentinel-1 SAR change detection.
"""

from typing import Dict, Any, List, Tuple
from app.models.domain import ContributingFactor, EnvironmentalIndicators


class FloodEngine:
    """
    Explainable Flood Hazard Engine.
    Computes Hazard Score [0-100] and decomposes key geophysical drivers.
    """

    # Model Weights (sum = 1.0)
    WEIGHT_RAINFALL_ANOMALY = 0.25
    WEIGHT_CUMULATIVE_7D = 0.20
    WEIGHT_ELEVATION_SLOPE = 0.15
    WEIGHT_TWI = 0.15
    WEIGHT_RIVER_PROXIMITY = 0.15
    WEIGHT_SAR_SURFACE_WATER = 0.10

    @classmethod
    def calculate_hazard(
        cls,
        district_id: str,
        indicators: EnvironmentalIndicators
    ) -> Tuple[float, List[ContributingFactor]]:
        """
        Calculates the Flood Hazard score and outputs interpretable contributing factors.
        """
        # 1. Rainfall Anomaly Sub-score (0-100)
        # Normal is 0% anomaly. Above +100% anomaly is extreme.
        rain_anomaly_norm = min(100.0, max(0.0, indicators.rainfall_anomaly_pct * 0.75))

        # 2. Cumulative 7-day Rainfall Sub-score (0-100)
        # 0mm -> 0, 150mm+ -> 100
        cum_rain_norm = min(100.0, (indicators.rainfall_7d_mm / 150.0) * 100.0)

        # 3. Elevation & Slope Vulnerability Sub-score (0-100)
        # Low elevation (< 20m) and flat slope (< 1.5 deg) = maximum water accumulation
        elev_factor = max(0.0, (100.0 - indicators.elevation_mean_m) * 1.0)
        slope_factor = max(0.0, (10.0 - min(10.0, indicators.slope_mean_deg)) * 10.0)
        terrain_score = min(100.0, (elev_factor * 0.5 + slope_factor * 0.5))

        # 4. Topographic Wetness Index (TWI) Sub-score (0-100)
        # Typical TWI in alluvial basins ranges 6 to 14. 12+ is saturated valley bottom.
        twi_score = min(100.0, max(0.0, (indicators.topographic_wetness_index - 5.0) / 9.0 * 100.0))

        # 5. Proximity to River Network (0-100)
        # 0 km -> 100, > 15 km -> 0
        proximity_score = max(0.0, (15.0 - min(15.0, indicators.distance_to_river_km)) / 15.0 * 100.0)

        # 6. Sentinel-1 SAR Surface Water Expansion (0-100)
        # Expansion of water area compared to dry-season baseline
        sar_score = min(100.0, max(0.0, indicators.surface_water_change_pct * 1.5))

        # Composite Hazard Score
        hazard_score = (
            rain_anomaly_norm * cls.WEIGHT_RAINFALL_ANOMALY +
            cum_rain_norm * cls.WEIGHT_CUMULATIVE_7D +
            terrain_score * cls.WEIGHT_ELEVATION_SLOPE +
            twi_score * cls.WEIGHT_TWI +
            proximity_score * cls.WEIGHT_RIVER_PROXIMITY +
            sar_score * cls.WEIGHT_SAR_SURFACE_WATER
        )
        hazard_score = round(min(100.0, max(0.0, hazard_score)), 1)

        # Build Explainability Factors
        factors = [
            ContributingFactor(
                factor_name="Precipitação Acumulada em 7 Dias",
                metric_value=f"{indicators.rainfall_7d_mm:.1f} mm (+{indicators.rainfall_anomaly_pct:.0f}% vs histórico)",
                weight=cls.WEIGHT_RAINFALL_ANOMALY + cls.WEIGHT_CUMULATIVE_7D,
                contribution_pct=round(((rain_anomaly_norm * cls.WEIGHT_RAINFALL_ANOMALY + cum_rain_norm * cls.WEIGHT_CUMULATIVE_7D) / max(1.0, hazard_score)) * 100, 1),
                description="Precipitação convectiva intensa e escoamento superficial acelerado na bacia a montante.",
                direction="INCREASING_RISK" if indicators.rainfall_anomaly_pct > 0 else "DECREASING_RISK"
            ),
            ContributingFactor(
                factor_name="Morfologia do Terreno & Índice de Umidade Topográfica (TWI)",
                metric_value=f"Elevação média {indicators.elevation_mean_m:.0f}m | TWI {indicators.topographic_wetness_index:.1f}",
                weight=cls.WEIGHT_ELEVATION_SLOPE + cls.WEIGHT_TWI,
                contribution_pct=round(((terrain_score * cls.WEIGHT_ELEVATION_SLOPE + twi_score * cls.WEIGHT_TWI) / max(1.0, hazard_score)) * 100, 1),
                description="Planície aluvial de baixa cota com declive inferior a 2° propícia ao empossamento e retenção de cheia.",
                direction="INCREASING_RISK"
            ),
            ContributingFactor(
                factor_name="Proximidade ao Leito do Rio Incomati",
                metric_value=f"{indicators.distance_to_river_km:.1f} km do canal principal",
                weight=cls.WEIGHT_RIVER_PROXIMITY,
                contribution_pct=round(((proximity_score * cls.WEIGHT_RIVER_PROXIMITY) / max(1.0, hazard_score)) * 100, 1),
                description="Alta susceptibilidade a transbordamento lateral de diques e vazão afluente da barragem de Corumana.",
                direction="INCREASING_RISK" if indicators.distance_to_river_km < 5.0 else "DECREASING_RISK"
            ),
            ContributingFactor(
                factor_name="Expansão de Lâmina d'Água (Sentinel-1 SAR)",
                metric_value=f"+{indicators.surface_water_change_pct:.1f}% expansão ({indicators.surface_water_extent_sqkm:.1f} km²)",
                weight=cls.WEIGHT_SAR_SURFACE_WATER,
                contribution_pct=round(((sar_score * cls.WEIGHT_SAR_SURFACE_WATER) / max(1.0, hazard_score)) * 100, 1),
                description="Variação no retroespalhamento de radar em micro-ondas C-Band confirma saturação do solo e inundações ativas.",
                direction="INCREASING_RISK" if indicators.surface_water_change_pct > 10 else "DECREASING_RISK"
            )
        ]

        return hazard_score, factors
