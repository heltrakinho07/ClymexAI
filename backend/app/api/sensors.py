"""
CLYMEX AI - IoT Telemetry & Sensor Stations API (Phase 2 Ready)
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Body
from app.models.domain import SensorTelemetry
from app.services.iot_service import IoTTelemetryEngine

router = APIRouter(prefix="/sensors", tags=["IoT Sensor Network"])


@router.get("", response_model=List[SensorTelemetry])
def list_sensor_stations():
    """
    Returns real-time and telemetry status for all hydrometric and meteorological stations in the basin.
    """
    return IoTTelemetryEngine.get_all_sensors()


@router.get("/{sensor_id}", response_model=SensorTelemetry)
def get_sensor_station(sensor_id: str):
    """
    Returns telemetry profile and QC data quality rating for a specific sensor node.
    """
    sensor = IoTTelemetryEngine.get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor não encontrado.")
    return sensor


@router.post("/telemetry", response_model=Dict[str, Any])
def ingest_sensor_telemetry(payload: Dict[str, Any] = Body(...)):
    """
    Ingestion endpoint for ESP32 / LoRaWAN gateway telemetry packets.
    Executes automated Quality Control (range checks, rate-of-change delta, stuck sensor detection).
    """
    return IoTTelemetryEngine.ingest_telemetry_payload(payload)
