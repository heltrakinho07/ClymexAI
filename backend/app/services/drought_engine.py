"""
CLYMEX AI - Drought Risk Engine
Monitors agricultural and meteorological drought using VCI (NDVI), Soil Moisture, and CHIRPS SPI.
"""

from typing import Dict, Any, List, Tuple
from app.models.domain import ContributingFactor, EnvironmentalIndicators


class DroughtEngine:
    """
    Explainable Drought Hazard Engine.
    Evaluates agricultural and meteorological drought intensity on a 0-100 scale.
    """

    WEIGHT_VCI_NDVI = 0.35
    WEIGHT_SOIL_MOISTURE = 0.30
    WEIGHT_RAINFALL_DEFICIT = 0.25
    WEIGHT_TEMPERATURE_ANOMALY = 0.10

    @classmethod
    def calculate_hazard(
        cls,
        district_id: str,
        indicators: EnvironmentalIndicators
    ) -> Tuple[float, List[ContributingFactor]]:
        """
        Calculates drought score and returns interpretable drivers.
        """
        # 1. NDVI / Vegetation Condition Index (VCI) Deficit
        # If NDVI anomaly is negative, drought stress increases
        # e.g., -30% anomaly -> high stress
        if indicators.ndvi_anomaly_pct < 0:
            vci_score = min(100.0, abs(indicators.ndvi_anomaly_pct) * 2.5)
        else:
            vci_score = max(0.0, 20.0 - indicators.ndvi_anomaly_pct)

        # 2. Soil Moisture Deficit
        # Low soil moisture (< 20%) -> high score
        soil_deficit_score = min(100.0, max(0.0, (35.0 - indicators.soil_moisture_pct) * 3.3))

        # 3. Precipitation Deficit (30-day accumulation deficit)
        if indicators.rainfall_anomaly_pct < 0:
            rain_deficit_score = min(100.0, abs(indicators.rainfall_anomaly_pct) * 1.5)
        else:
            rain_deficit_score = max(0.0, 15.0 - indicators.rainfall_anomaly_pct * 0.2)

        # 4. Thermal Stress (Temperature Anomaly)
        temp_score = min(100.0, max(0.0, indicators.temperature_anomaly_c * 25.0))

        # Composite Drought Hazard
        hazard_score = (
            vci_score * cls.WEIGHT_VCI_NDVI +
            soil_deficit_score * cls.WEIGHT_SOIL_MOISTURE +
            rain_deficit_score * cls.WEIGHT_RAINFALL_DEFICIT +
            temp_score * cls.WEIGHT_TEMPERATURE_ANOMALY
        )
        hazard_score = round(min(100.0, max(0.0, hazard_score)), 1)

        factors = [
            ContributingFactor(
                factor_name="Índice de Condição da Vegetação (VCI / NDVI)",
                metric_value=f"NDVI {indicators.ndvi_current:.2f} ({indicators.ndvi_anomaly_pct:+.1f}% vs baseline)",
                weight=cls.WEIGHT_VCI_NDVI,
                contribution_pct=round(((vci_score * cls.WEIGHT_VCI_NDVI) / max(1.0, hazard_score)) * 100, 1),
                description="Monitoramento multiespectral Sentinel-2/MODIS avaliando a fotossíntese e vigor da biomassa foliar.",
                direction="INCREASING_RISK" if indicators.ndvi_anomaly_pct < -5 else "DECREASING_RISK"
            ),
            ContributingFactor(
                factor_name="Déficit de Umidade no Solo (0-20 cm)",
                metric_value=f"{indicators.soil_moisture_pct:.1f}% ({indicators.soil_moisture_anomaly_pct:+.1f}% vs normal)",
                weight=cls.WEIGHT_SOIL_MOISTURE,
                contribution_pct=round(((soil_deficit_score * cls.WEIGHT_SOIL_MOISTURE) / max(1.0, hazard_score)) * 100, 1),
                description="Capacidade de campo reduzida na zona radicular das culturas agrícolas de sequeiro e pastagens.",
                direction="INCREASING_RISK" if indicators.soil_moisture_pct < 22 else "DECREASING_RISK"
            ),
            ContributingFactor(
                factor_name="Balanço Pluviométrico (CHIRPS SPI)",
                metric_value=f"{indicators.rainfall_30d_mm:.1f} mm acumulados em 30d ({indicators.rainfall_anomaly_pct:+.1f}%)",
                weight=cls.WEIGHT_RAINFALL_DEFICIT,
                contribution_pct=round(((rain_deficit_score * cls.WEIGHT_RAINFALL_DEFICIT) / max(1.0, hazard_score)) * 100, 1),
                description="Regularidade dos eventos de precipitação sazonal comparada à climatologia de 20 anos.",
                direction="INCREASING_RISK" if indicators.rainfall_anomaly_pct < 0 else "DECREASING_RISK"
            ),
            ContributingFactor(
                factor_name="Anomalia Térmica de Superfície (LST)",
                metric_value=f"Média {indicators.temperature_mean_c:.1f}°C ({indicators.temperature_anomaly_c:+.1f}°C anomalia)",
                weight=cls.WEIGHT_TEMPERATURE_ANOMALY,
                contribution_pct=round(((temp_score * cls.WEIGHT_TEMPERATURE_ANOMALY) / max(1.0, hazard_score)) * 100, 1),
                description="Temperaturas acima da média aceleram as taxas de evapotranspiração potencial e dessecação do solo.",
                direction="INCREASING_RISK" if indicators.temperature_anomaly_c > 1.0 else "DECREASING_RISK"
            )
        ]

        return hazard_score, factors
