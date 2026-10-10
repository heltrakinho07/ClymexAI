"""
CLYMEX AI - Early Warning & Alert Engine
Generates multi-hazard actionable alerts for disaster risk reduction and civil protection.
"""

import datetime
from typing import List
from app.models.domain import AlertRecord, HazardType, RiskLevel
from app.services.risk_engine import ClimateRiskEngine


class AlertEngine:
    """
    Automated Alert Orchestrator detecting anomalies and threshold breaches.
    """

    @classmethod
    def generate_active_alerts(cls) -> List[AlertRecord]:
        """
        Scans all monitored districts and generates active alerts where risk > threshold.
        """
        assessments = ClimateRiskEngine.get_all_districts_overview()
        alerts: List[AlertRecord] = []

        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()

        for a in assessments:
            # 1. Flood Alert Criteria
            if a.hazard_type in [HazardType.FLOOD, HazardType.OVERALL_CLIMATE] and a.risk_score >= 50.0 and a.indicators.surface_water_change_pct > 25.0:
                is_critical = a.risk_score >= 70.0
                alerts.append(
                    AlertRecord(
                        id=f"ALT-FLD-{a.area_id.upper()}-01",
                        hazard=HazardType.FLOOD,
                        title=f"Alerta {'Crítico' if is_critical else 'Laranja'}: Risco de Cheia no Baixo Incomati ({a.area_name})",
                        location=f"{a.area_name}, {a.province}",
                        province=a.province,
                        timestamp=now_str,
                        risk_level=RiskLevel.CRITICAL if is_critical else RiskLevel.HIGH,
                        trigger_condition=(
                            f"Precipitação 7d atingiu {a.indicators.rainfall_7d_mm:.0f}mm (+{a.indicators.rainfall_anomaly_pct:.0f}% anomalia) "
                            f"com elevação de nível de água detectada por Sentinel-1 SAR (+{a.indicators.surface_water_change_pct:.0f}% expansão de lâmina)."
                        ),
                        affected_area_sqkm=round(a.indicators.surface_water_extent_sqkm * 1.8, 1),
                        estimated_population_exposed=a.exposure.population_exposed,
                        confidence_pct=a.confidence_pct,
                        recommended_action=(
                            f"1. Mobilizar comitês distritais de gestão de desastres (CLGRC) em {a.area_name}. "
                            f"2. Monitorar o calado da ponte da EN1 sobre o Incomati. "
                            f"3. Emitir avisos preventivos a comunidades agrícolas ribeirinhas e pecuaristas em zonas de várzea."
                        ),
                        data_sources=["Sentinel-1 SAR C-Band", "CHIRPS v2.0", "Estação Telemétrica E-33"],
                        is_active=True
                    )
                )

            # 2. Drought Alert Criteria
            if a.indicators.ndvi_anomaly_pct < -25.0 and a.indicators.soil_moisture_pct < 18.0:
                alerts.append(
                    AlertRecord(
                        id=f"ALT-DRT-{a.area_id.upper()}-02",
                        hazard=HazardType.DROUGHT,
                        title=f"Aviso Agroclimático: Estresse Hídrico e Seca no Alto Incomati ({a.area_name})",
                        location=f"{a.area_name}, {a.province}",
                        province=a.province,
                        timestamp=now_str,
                        risk_level=RiskLevel.HIGH,
                        trigger_condition=(
                            f"Déficit acentuado de vegetação (NDVI -{abs(a.indicators.ndvi_anomaly_pct):.1f}%) "
                            f"e umidade do solo em {a.indicators.soil_moisture_pct:.1f}% com déficit pluviométrico de 30 dias."
                        ),
                        affected_area_sqkm=1450.0,
                        estimated_population_exposed=a.exposure.population_exposed,
                        confidence_pct=84.0,
                        recommended_action=(
                            "1. Priorizar racionamento preventivo de água para irrigação secundária. "
                            "2. Apoiar criadores de gado com abertura de bebedouros de emergência. "
                            "3. Monitorar índice de biomassa forrageira via satélite."
                        ),
                        data_sources=["Sentinel-2 NDVI", "ERA5-Land Soil Moisture", "MODIS LST"],
                        is_active=True
                    )
                )

        return alerts
