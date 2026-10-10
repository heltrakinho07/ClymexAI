"""
CLYMEX AI - Early Warning Alerts API
"""

from typing import List
from fastapi import APIRouter
from app.models.domain import AlertRecord
from app.services.alert_engine import AlertEngine

router = APIRouter(prefix="/alerts", tags=["Alerts & Early Warning"])


@router.get("", response_model=List[AlertRecord])
def list_active_alerts():
    """
    Returns active multi-hazard alerts triggered by threshold exceedances across the basin.
    """
    return AlertEngine.generate_active_alerts()
