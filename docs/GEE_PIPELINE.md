# CLYMEX AI — Earth Engine processing pipeline

**Status:** Implemented in source; Earth Engine / field validation pending.

The satellite service builds real Google Earth Engine images clipped to
administrative geometries supplied by the GeoMoz Python package. It does not
present basemap tiles as processed satellite imagery.

## Setup

1. Install Python dependencies from backend/requirements.txt (geomoz,
   earthengine-api, google-auth).
2. Enable Earth Engine API and register the GCP project for Earth Engine access.
3. Set GEE_PROJECT_ID to your approved project ID.
4. Supply server-only credentials through Cloud Run application default identity,
   or GEE_PRIVATE_KEY_PATH pointing to a mounted JSON file, or the
   GEE_SERVICE_ACCOUNT_JSON secret injected by deployment.
5. Ensure GeoMoz downloads/cache are available in the environment.
6. Never set GEE credentials in frontend NEXT_PUBLIC variables or submit
   service-account key JSON through public endpoints.

The backend verifies the connection with a real Earth Engine request.
Unconfigured GEE returns connected=false and the actual processing endpoints
respond with an error; no synthetic observation is substituted.

## Endpoints

- GET /api/v1/satellite/gee/status
- POST /api/v1/satellite/gee/tile
  JSON body: {"index":"ndvi","district_id":"manhica"}
  Optional dates: {"start_date":"2026-07-01","end_date":"2026-08-01"}
- GET /api/v1/satellite/gee/metrics/manhica
- GET /api/v1/satellite/gee/precipitation-series/manhica?days=30

Valid tile indices: ndvi, ndwi, mndwi, flood_sar, elevation, slope, precipitation.

End dates are exclusive. Tiles default to 120 days of lookback for most
datasets and 30 days for SAR change analysis. Dates are recorded per source.

The CHIRPS series uses the last published observation when no explicit end
date is provided. CHIRPS can lag the present calendar date by weeks. Never
interpret an empty interval as zero precipitation.

## Scientific methods and status

| Product | GEE collection | Derived output | Status |
| --- | --- | --- | --- |
| NDVI | COPERNICUS/S2_SR_HARMONIZED | Median cloud-masked (B8-B4)/(B8+B4) | Remote-derived, uncalibrated |
| NDWI | COPERNICUS/S2_SR_HARMONIZED | Median cloud-masked (B3-B8)/(B3+B8) | Indicative water |
| MNDWI | COPERNICUS/S2_SR_HARMONIZED | Median cloud-masked (B3-B11)/(B3+B11) | Exploratory |
| SAR | COPERNICUS/S1_GRD | VV pre/post dB change, same pass, slope and permanent-water filtering | CANDIDATE flood, NOT confirmed |
| Rainfall | UCSB-CHG/CHIRPS/DAILY | Daily and interval-total precipitation | Historical, with publication lag |
| Terrain | COPERNICUS/DEM/GLO30 | Mosaicked elevation and terrain slope | Static model |

Cloud masks use Sentinel-2 SCL. The SAR detector uses VV reduction >3 dB,
post VV <-15 dB, slope <5 degrees and JRC permanent-water occurrence <80%.
These are heuristic pilot thresholds. Terrain distortion, crop cycles and
backscatter variations can produce false flood classifications. Before use in
emergency decisions compare against independent reference masks; publish
precision, recall, F1/IoU and uncertainty.

Raster estimates use GeoMoz district geometries with Earth Engine reduceRegion.
Missing values are null; the frontend does not invent replacement NDVI,
CHIRPS or SAR measurements. CHIRPS historical chart does not claim to have
computed the 20-year climatological normal.

## Current limitations / next phase

- The risk-score engine still uses a separate rule-based system. Satellite
  observations are not assimilated into its scores yet.
- VCI and operational ML prediction horizons are not implemented.
- Maputo administrative districts use the 2017 GeoMoz geometry.
- Chókwè belongs to the Limpopo basin, not Incomati.
- Earth Engine model outputs and hazard areas are not field-validated.
- OAuth, monitoring/quotas, RBAC and persistent telemetry are not production-ready.

## Validation

- Execute the Python backend suite and Next.js build from CI.
- Confirm GEE status from real server identity.
- Compare actual indices/tiles with expected sensor observations.
- Validate the true date of last CHIRPS observation (not today's date).
- Test absent credentials, no acquisitions and invalid dates/indices.
- Validate GeoMoz shape and administrative attribution of each pilot district.
- Do not issue official emergency alerts on the basis of this demonstrator.

## Google technical references

- https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED
- https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD
- https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY
- https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30
- https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_GlobalSurfaceWater
- https://developers.google.com/earth-engine/guides/auth
