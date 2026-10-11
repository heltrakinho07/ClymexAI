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
            f"SIMULAÇÃO CLYMEX AI: o distrito de {assessment.area_name} ({assessment.province}) "
            f"apresenta um índice de risco ilustrativo de {assessment.risk_score:.0f}/100 "
            f"({assessment.risk_level.value}). Estes indicadores provêm de um cenário demonstrativo "
            f"e não representam condições hidrometeorológicas actualmente observadas, "
            f"confirmação de inundação por Sentinel-1 nem alertas governamentais. "
            f"Exposição indicativa do cenário: {assessment.exposure.population_exposed:,} habitantes "
            f"e {assessment.exposure.buildings_count:,} edifícios estimados. "
            f"A avaliação real requer processamento satelital validado, dados hidrométricos "
            f"e confirmação das fontes e da qualidade dos dados."
        )

        hazard_matrix = {
            "flood": {
                "hazard_score": flood_assessment.hazard_score,
                "risk_score": flood_assessment.risk_score,
                "level": flood_assessment.risk_level.value,
                "status": flood_assessment.risk_level.value
            },
            "drought": {
                "hazard_score": drought_assessment.hazard_score,
                "risk_score": drought_assessment.risk_score,
                "level": drought_assessment.risk_level.value,
                "status": drought_assessment.risk_level.value
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
            "Cenário de treino: verificar os dados mais recentes nas autoridades meteorológicas e hidrológicas oficiais.",
            "Se o perigo for confirmado, avaliar exposição por bairro, estradas, escolas e postos de saúde com dados espaciais validados.",
            "Submeter as recomendações a revisão por profissionais e responsáveis de protecção civil antes de qualquer intervenção.",
            "Não desencadear evacuações ou operações de emergência exclusivamente com base nesta simulação.",
        ]

        disclaimer = (
            "DOCUMENTO DEMONSTRATIVO — NÃO OFICIAL. Resultados sintéticos e estimativas "
            "sem validação operacional; não substituir alertas do INAM, DNGRH/ARA-Sul, "
            "INGD ou autoridades competentes. Não representa uma observação confirmada de satélite."
        )

        return SituationReport(
            report_id=f"SITREP-{assessment.area_id.upper()}-{datetime.date.today().strftime('%Y%m%d')}",
            generated_at=now_str,
            title=f"SitRep DEMO — Cenário de Risco Climático ({assessment.area_name}, {assessment.basin})",
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
