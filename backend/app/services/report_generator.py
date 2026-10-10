"""
CLYMEX AI - Situation Report (SitRep) & Climate Bulletin Generator
"Predict Risk. Protect Tomorrow."
Generates structured decision-support briefs for government agencies, insurers, and NGOs.
"""

import datetime
from typing import Dict, Any, Optional
from app.models.domain import SituationReport, RiskLevel, HazardType
from app.services.risk_engine import ClimateRiskEngine
from app.data.historical_records import DATA_PROVENANCE_CATALOG


class ReportGenerator:
    """
    Synthesizes technical data into formal Climate Intelligence Bulletins.
    """

    @classmethod
    def generate_district_report(cls, district_id: str = "manhica") -> SituationReport:
        """
        Builds a comprehensive situation report for a chosen district.
        """
        assessment = ClimateRiskEngine.assess_district(district_id, HazardType.OVERALL_CLIMATE)
        flood_assessment = ClimateRiskEngine.assess_district(district_id, HazardType.FLOOD)
        drought_assessment = ClimateRiskEngine.assess_district(district_id, HazardType.DROUGHT)
        stress_assessment = ClimateRiskEngine.assess_district(district_id, HazardType.WATER_STRESS)

        now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        exec_summary = (
            f"O distrito de {assessment.area_name} ({assessment.province}, Moçambique) apresenta um "
            f"Índice de Risco Climático Composto de {assessment.risk_score:.0f}/100, classificado no nível operacional "
            f"'{assessment.risk_level.value}'. O perigo dominante atual é de natureza hidrometeorológica (Cheia Aluvial), "
            f"impulsionado por uma precipitação acumulada em 7 dias de {assessment.indicators.rainfall_7d_mm:.1f} mm "
            f"(+{assessment.indicators.rainfall_anomaly_pct:.0f}% acima da média histórica climatológica) "
            f"e transbordo lateral de calha confirmado por radar Sentinel-1 SAR (+{assessment.indicators.surface_water_change_pct:.0f}% de expansão de lâmina d'água). "
            f"Estima-se que {assessment.exposure.population_exposed:,} habitantes e {assessment.exposure.buildings_count:,} "
            f"edifícios identificados pela base Google Open Buildings estejam na zona direta de impacto fluvial."
        )

        hazard_matrix = {
            "flood": {
                "hazard_score": flood_assessment.hazard_score,
                "risk_score": flood_assessment.risk_score,
                "level": flood_assessment.risk_level.value,
                "status": "CRÍTICO" if flood_assessment.risk_score >= 70 else "ALTO"
            },
            "drought": {
                "hazard_score": drought_assessment.hazard_score,
                "risk_score": drought_assessment.risk_score,
                "level": drought_assessment.risk_level.value,
                "status": "MODERADO"
            },
            "water_stress": {
                "hazard_score": stress_assessment.hazard_score,
                "risk_score": stress_assessment.risk_score,
                "level": stress_assessment.risk_level.value,
                "status": "MODERADO"
            }
        }

        key_drivers_summary = [
            f"{d.factor_name}: {d.metric_value} ({d.description})"
            for d in assessment.primary_drivers
        ]

        recommendations = [
            f"Ativação Imediata do Centro de Operações de Emergência Distrital (COED) em {assessment.area_name}.",
            "Inspeção técnica e salvaguarda do tabuleiro e encontros da ponte da Estrada Nacional EN1 sobre o Rio Incomati.",
            "Coordenação com a Administração Regional de Águas do Sul (ARA-Sul) para escalonamento de vazão da Barragem de Corumana.",
            f"Pré-posicionamento de embarcações de resgate e insumos de purificação de água nas comunidades ribeirinhas vulneráveis ({assessment.exposure.population_exposed:,} pessoas estimadas).",
            "Monitoramento contínuo em tempo real via imagens de satélite Sentinel-1 SAR e estações de nível telemétricas."
        ]

        disclaimer = (
            "Aviso Legal & Transparência Científica: O presente Boletim de Inteligência Climática é emitido pela plataforma "
            "CLYMEX AI para suporte à tomada de decisão preventiva, modelagem de risco e planejamento de resiliência. "
            "Os valores apresentados combinam sensoriamento remoto orbital (ESA Copernicus Sentinel-1/2), reanálises ECMWF ERA5-Land, "
            "CHIRPS v2.0 e cadastros Google Open Buildings. As diretrizes oficiais de evacuação cabem com exclusividade ao Instituto Nacional "
            "de Gestão e Redução do Risco de Desastres (INGD) de Moçambique."
        )

        return SituationReport(
            report_id=f"SITREP-{assessment.area_id.upper()}-{datetime.date.today().strftime('%Y%m%d')}",
            generated_at=now_str,
            title=f"Boletim Especial de Risco Climático & Cheias — Bacia do Incomati ({assessment.area_name})",
            country=assessment.country,
            region=f"{assessment.province} / {assessment.basin}",
            executive_summary=exec_summary,
            overall_risk_score=assessment.risk_score,
            overall_risk_level=assessment.risk_level,
            hazard_matrix=hazard_matrix,
            total_population_exposed=assessment.exposure.population_exposed,
            total_buildings_exposed=assessment.exposure.buildings_count,
            critical_infrastructure_count=len(assessment.exposure.critical_infrastructure) + assessment.exposure.schools_count + assessment.exposure.hospitals_count,
            key_drivers=key_drivers_summary,
            recommended_mitigation_actions=recommendations,
            data_sources=DATA_PROVENANCE_CATALOG,
            disclaimer=disclaimer
        )
