"""
CLYMEX AI - Situation Reports (SitRep) API
"""

from fastapi import APIRouter, Query
from app.models.domain import SituationReport
from app.services.report_generator import ReportGenerator

router = APIRouter(prefix="/reports", tags=["Decision Reports"])


@router.get("/{district_id}", response_model=SituationReport)
def get_situation_report(district_id: str):
    """
    Generates a formal, printable Situation Report (SitRep) for the designated district.
    """
    return ReportGenerator.generate_district_report(district_id)
