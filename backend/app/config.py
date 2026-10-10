"""
CLYMEX AI - Global Configuration & Risk Threshold Settings
"Predict Risk. Protect Tomorrow."
"""

from typing import Dict, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "CLYMEX AI"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DESCRIPTION: str = (
        "Production-grade Climate Intelligence and Climate Risk Platform. "
        "Transforms satellite Earth observation, weather, hydrology, terrain and "
        "socio-economic exposure into actionable decision intelligence."
    )
    
    # Environment & Demo Flag
    ENV: str = "development"
    DEMO_MODE: bool = True  # Visually & functionally distinguished from live data
    
    # Security & Auth
    SECRET_KEY: str = "clymex-ai-super-secure-jwt-secret-key-2026-incomati-resilience"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Multi-country / Regional configuration
    DEFAULT_COUNTRY: str = "Mozambique"
    DEFAULT_REGION: str = "Greater Maputo / Incomati Basin"
    DEFAULT_CENTER_LAT: float = -25.55
    DEFAULT_CENTER_LNG: float = 32.75
    DEFAULT_ZOOM: int = 9
    
    # Configurable Risk Thresholds (Score: 0 to 100)
    RISK_THRESHOLD_LOW: float = 20.0
    RISK_THRESHOLD_MODERATE: float = 40.0
    RISK_THRESHOLD_HIGH: float = 60.0
    RISK_THRESHOLD_VERY_HIGH: float = 80.0
    # > 80 is CRITICAL
    
    # Alert Trigger Thresholds
    ALERT_FLOOD_THRESHOLD: float = 60.0
    ALERT_DROUGHT_THRESHOLD: float = 60.0
    ALERT_WATER_STRESS_THRESHOLD: float = 65.0
    ALERT_RAINFALL_EXTREME_MM_24H: float = 80.0
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]
    
    # GEE & External services
    GEE_SERVICE_ACCOUNT: str = ""
    GEE_PRIVATE_KEY_PATH: str = ""
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
