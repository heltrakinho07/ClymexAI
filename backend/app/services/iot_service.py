"""
CLYMEX AI - IoT Sensor Telemetry & Data Quality Engine (Phase 2 Ready)
"Predict Risk. Protect Tomorrow."
Ingests water level, rain gauge, and soil sensor telemetry with automatic anomaly & quality scoring.
"""

import datetime
from typing import Dict, Any, List, Tuple
from app.models.domain import SensorTelemetry, SensorReading, SensorStatus
from app.data.historical_records import SENSOR_STATIONS_DATA


class IoTTelemetryEngine:
    """
    Validates, scores, and ingests physical environmental sensor telemetry.
    """

    # Physical Bounds for sensor validation
    SENSOR_BOUNDS = {
        "WATER_LEVEL": {"min": 0.0, "max": 18.0, "max_delta_1h": 3.0, "unit": "m"},
        "RAINFALL": {"min": 0.0, "max": 350.0, "max_delta_1h": 120.0, "unit": "mm/24h"},
        "SOIL_MOISTURE": {"min": 0.0, "max": 100.0, "max_delta_1h": 25.0, "unit": "%"},
        "AIR_TEMPERATURE": {"min": 5.0, "max": 50.0, "max_delta_1h": 10.0, "unit": "°C"},
        "RESERVOIR_OUTFLOW": {"min": 0.0, "max": 5000.0, "max_delta_1h": 1000.0, "unit": "m³/s"},
        "RESERVOIR_STORAGE": {"min": 0.0, "max": 100.0, "max_delta_1h": 15.0, "unit": "%"}
    }

    @classmethod
    def get_all_sensors(cls) -> List[SensorTelemetry]:
        """
        Returns all registered sensor telemetry nodes in the basin.
        """
        return SENSOR_STATIONS_DATA

    @classmethod
    def get_sensor_by_id(cls, sensor_id: str) -> SensorTelemetry | None:
        """
        Finds a specific sensor by identifier.
        """
        for s in SENSOR_STATIONS_DATA:
            if s.sensor_id == sensor_id:
                return s
        return None

    @classmethod
    def validate_reading(
        cls,
        sensor_type: str,
        value: float,
        previous_value: float | None = None
    ) -> Tuple[bool, float, List[str]]:
        """
        Executes QC checks: range bounds, rate-of-change (spike), and physical plausibility.
        Returns: (is_valid, quality_score [0-100], flags)
        """
        bounds = cls.SENSOR_BOUNDS.get(sensor_type, {"min": -100.0, "max": 1000.0, "max_delta_1h": 50.0})
        flags = []
        score = 100.0

        # Check 1: Impossible values (hard physical limits)
        if value < bounds["min"] or value > bounds["max"]:
            flags.append(f"OUT_OF_BOUNDS: {value} outside [{bounds['min']}, {bounds['max']}]")
            score -= 60.0

        # Check 2: Sudden unphysical spike / rate of change
        if previous_value is not None:
            delta = abs(value - previous_value)
            if delta > bounds["max_delta_1h"]:
                flags.append(f"UNPHYSICAL_SPIKE: Delta of {delta:.2f} exceeds limit {bounds['max_delta_1h']}")
                score -= 35.0

        # Check 3: Zero or stuck reading detection
        if value == 0.0 and sensor_type in ["WATER_LEVEL", "SOIL_MOISTURE"]:
            flags.append("SUSPECT_ZERO_READING")
            score -= 20.0

        score = max(0.0, min(100.0, score))
        is_valid = score >= 50.0
        return is_valid, score, flags

    @classmethod
    def ingest_telemetry_payload(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulates ingestion of an incoming MQTT / HTTP payload from an ESP32 LoRaWAN gateway.
        """
        sensor_id = payload.get("sensor_id")
        value = float(payload.get("value", 0.0))
        battery = float(payload.get("battery", 100.0))
        sensor_type = payload.get("sensor_type", "WATER_LEVEL")

        is_valid, quality_score, flags = cls.validate_reading(sensor_type, value)

        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()

        status = SensorStatus.ONLINE
        if not is_valid:
            status = SensorStatus.ERROR
        elif quality_score < 80.0 or battery < 20.0:
            status = SensorStatus.WARNING

        # Update in-memory station record if it exists
        matched_sensor = None
        for s in SENSOR_STATIONS_DATA:
            if s.sensor_id == sensor_id:
                s.current_value = value
                s.battery_pct = int(battery)
                s.status = status
                s.data_quality_score = quality_score
                s.quality_flags = flags
                s.last_seen = now_str
                matched_sensor = s
                break

        return {
            "status": "ACCEPTED" if is_valid else "REJECTED_QC_FAIL",
            "sensor_id": sensor_id,
            "station_name": matched_sensor.station_name if matched_sensor else "Estação Remota",
            "timestamp": now_str,
            "processed_value": value,
            "quality_score": quality_score,
            "assigned_status": status,
            "quality_flags": flags,
            "storage_destination": "TimescaleDB / Hypertable sensor_readings"
        }
