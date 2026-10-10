"""
CLYMEX AI - Water Stress Engine
Evaluates hydrological water stress, reservoir storage, and agricultural/domestic supply pressure.
"""

from typing import Dict, Any, List, Tuple
from app.models.domain import ContributingFactor, EnvironmentalIndicators


class WaterStressEngine:
    """
    Explainable Water Stress Engine.
    Computes hydrological and socio-ecological water stress score [0-100].
    """

    WEIGHT_RESERVOIR_STORAGE = 0.35
    WEIGHT_SURFACE_WATER = 0.25
    WEIGHT_SOIL_MOISTURE = 0.25
    WEIGHT_EVAPOTRANSPIRATION = 0.15

    @classmethod
    def calculate_hazard(
        cls,
        district_id: str,
        indicators: EnvironmentalIndicators
    ) -> Tuple[float, List[ContributingFactor]]:
        """
        Calculates water stress and outputs contributing factors.
        """
        # Specific regional storage baselines for Maputo water supply
        # Pequenos Libombos / Corumana dams
        if district_id in ["boane", "matola", "maputo_city"]:
            reservoir_level_pct = 54.2  # Pequenos Libombos storage %
        elif district_id in ["moamba", "magude"]:
            reservoir_level_pct = 68.5  # Corumana storage %
        else:
            reservoir_level_pct = 60.0

        # Low reservoir level (< 40%) creates acute water stress
        storage_stress = min(100.0, max(0.0, (80.0 - reservoir_level_pct) * 1.5))

        # Surface water extent deficit
        if indicators.surface_water_change_pct < 0:
            surface_stress = min(100.0, abs(indicators.surface_water_change_pct) * 2.0)
        else:
            surface_stress = max(0.0, 30.0 - indicators.surface_water_change_pct)

        # Soil moisture stress
        soil_stress = min(100.0, max(0.0, (30.0 - indicators.soil_moisture_pct) * 3.0))

        # Thermal / Evapotranspiration stress
        et_stress = min(100.0, max(0.0, indicators.temperature_anomaly_c * 20.0 + 20.0))

        hazard_score = (
            storage_stress * cls.WEIGHT_RESERVOIR_STORAGE +
            surface_stress * cls.WEIGHT_SURFACE_WATER +
            soil_stress * cls.WEIGHT_SOIL_MOISTURE +
            et_stress * cls.WEIGHT_EVAPOTRANSPIRATION
        )
        hazard_score = round(min(100.0, max(0.0, hazard_score)), 1)

        factors = [
            ContributingFactor(
                factor_name="Capacidade dos Reservatórios Estratégicos",
                metric_value=f"{reservoir_level_pct:.1f}% da capacidade útil de armazenamento",
                weight=cls.WEIGHT_RESERVOIR_STORAGE,
                contribution_pct=round(((storage_stress * cls.WEIGHT_RESERVOIR_STORAGE) / max(1.0, hazard_score)) * 100, 1),
                description="Volumes operacionais nas albufeiras de Pequenos Libombos e Corumana que abastecem a Grande Maputo.",
                direction="INCREASING_RISK" if reservoir_level_pct < 60 else "DECREASING_RISK"
            ),
            ContributingFactor(
                factor_name="Dinâmica dos Corpos Hídricos Superficiais",
                metric_value=f"{indicators.surface_water_extent_sqkm:.1f} km² ({indicators.surface_water_change_pct:+.1f}%)",
                weight=cls.WEIGHT_SURFACE_WATER,
                contribution_pct=round(((surface_stress * cls.WEIGHT_SURFACE_WATER) / max(1.0, hazard_score)) * 100, 1),
                description="Índice de Diferença Normalizada da Água (NDWI) rastreando lagoas, meandros e afluentes.",
                direction="INCREASING_RISK" if indicators.surface_water_change_pct < -10 else "DECREASING_RISK"
            ),
            ContributingFactor(
                factor_name="Pressão de Demanda Agrícola e Consuntiva",
                metric_value="Intensidade de irrigação no Vale do Incomati e Consumo Urbano",
                weight=cls.WEIGHT_SOIL_MOISTURE,
                contribution_pct=round(((soil_stress * cls.WEIGHT_SOIL_MOISTURE) / max(1.0, hazard_score)) * 100, 1),
                description="Balanço entre captação autorizada para cana-de-açúcar/hortícolas e vazão ecológica mínima do rio.",
                direction="INCREASING_RISK"
            )
        ]

        return hazard_score, factors
