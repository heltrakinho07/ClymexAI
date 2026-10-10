"""
CLYMEX AI - Main Application Entrypoint
"Predict Risk. Protect Tomorrow."
FastAPI Geospatial & Climate Intelligence Platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import (
    auth,
    risk,
    areas,
    exposure,
    satellite,
    weather,
    sensors,
    alerts,
    reports,
    export
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for development; configure strictly in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(risk.router, prefix=settings.API_V1_PREFIX)
app.include_router(areas.router, prefix=settings.API_V1_PREFIX)
app.include_router(exposure.router, prefix=settings.API_V1_PREFIX)
app.include_router(satellite.router, prefix=settings.API_V1_PREFIX)
app.include_router(weather.router, prefix=settings.API_V1_PREFIX)
app.include_router(sensors.router, prefix=settings.API_V1_PREFIX)
app.include_router(alerts.router, prefix=settings.API_V1_PREFIX)
app.include_router(reports.router, prefix=settings.API_V1_PREFIX)
app.include_router(export.router, prefix=settings.API_V1_PREFIX)



@app.get("/", tags=["Health & Status"])
def root_status():
    return {
        "platform": "CLYMEX AI",
        "slogan": "Predict Risk. Protect Tomorrow.",
        "version": settings.VERSION,
        "environment": settings.ENV,
        "demo_mode": settings.DEMO_MODE,
        "demonstrator_focus": {
            "country": settings.DEFAULT_COUNTRY,
            "region": settings.DEFAULT_REGION,
            "center": [settings.DEFAULT_CENTER_LAT, settings.DEFAULT_CENTER_LNG],
            "zoom": settings.DEFAULT_ZOOM
        },
        "docs_url": "/docs",
        "status": "OPERATIONAL"
    }


@app.get("/health", tags=["Health & Status"])
def health_check():
    return {
        "status": "healthy",
        "database": "spatial_mock_ready",
        "risk_engine": "online",
        "exposure_engine": "online",
        "alert_engine": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
