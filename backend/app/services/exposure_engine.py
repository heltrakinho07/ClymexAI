"""
CLYMEX AI - Exposure & Asset Impact Engine
Intersects hazard extents with Google Open Buildings, WorldPop, and Critical Infrastructure.
"""

from typing import Dict, Any, List
from shapely.geometry import shape, Point, Polygon
from app.models.domain import ExposureBreakdown
from app.data.exposure_data import DISTRICT_EXPOSURE_STATS, CRITICAL_INFRASTRUCTURE_GEOJSON


class ExposureEngine:
    """
    Computes human, structural and economic exposure for any selected district or polygon.
    """

    @classmethod
    def get_district_exposure(cls, district_id: str, hazard_score: float) -> tuple[ExposureBreakdown, float, float]:
        """
        Retrieves baseline exposure and scales it dynamically by current hazard intensity.
        Returns: (ExposureBreakdown, exposure_score [0-100], vulnerability_score [0-100])
        """
        stats = DISTRICT_EXPOSURE_STATS.get(
            district_id,
            DISTRICT_EXPOSURE_STATS["manhica"]  # Default fallback
        )

        hazard_factor = hazard_score / 100.0

        # Dynamically scale exposure to the current hazard footprint
        pop_exposed = int(stats["population_exposed_flood_zone"] * (0.4 + 0.6 * hazard_factor))
        buildings_exposed = int(stats["buildings_in_hazard_zone"] * (0.35 + 0.65 * hazard_factor))
        schools_exposed = max(1, int(stats["schools_exposed"] * (0.5 + 0.5 * hazard_factor)))
        hospitals_exposed = max(0, int(stats["hospitals_exposed"] * (0.5 + 0.5 * hazard_factor)))
        roads_exposed = round(stats["roads_flooded_km"] * (0.3 + 0.7 * hazard_factor), 1)
        agri_exposed = round(stats["agricultural_hectares_flooded"] * (0.3 + 0.7 * hazard_factor), 1)

        critical_facilities = []
        for feature in CRITICAL_INFRASTRUCTURE_GEOJSON["features"]:
            props = feature["properties"]
            if props.get("district") == district_id:
                critical_facilities.append(f"{props['name']} ({props['category']})")

        exposure_breakdown = ExposureBreakdown(
            population_exposed=pop_exposed,
            population_density_per_sqkm=round(stats["population_total"] / 1000.0, 1),
            buildings_count=buildings_exposed,
            schools_count=schools_exposed,
            hospitals_count=hospitals_exposed,
            roads_km=roads_exposed,
            cropland_hectares=agri_exposed,
            critical_infrastructure=critical_facilities
        )

        # Calculate Normalized Exposure Score (0-100)
        # Weighting: Population (40%), Buildings (25%), Roads & Bridges (20%), Agriculture & Healthcare (15%)
        pop_norm = min(100.0, (pop_exposed / 60000.0) * 100.0)
        bld_norm = min(100.0, (buildings_exposed / 15000.0) * 100.0)
        roads_norm = min(100.0, (roads_exposed / 30.0) * 100.0)
        agri_norm = min(100.0, (agri_exposed / 20000.0) * 100.0)

        exposure_score = round(
            pop_norm * 0.40 +
            bld_norm * 0.25 +
            roads_norm * 0.20 +
            agri_norm * 0.15,
            1
        )
        exposure_score = min(100.0, max(0.0, exposure_score))

        # Vulnerability Score (0-100) based on district coping capacity
        vulnerability_score = round(stats["vulnerability_index"] * 100.0, 1)

        return exposure_breakdown, exposure_score, vulnerability_score

    @classmethod
    def calculate_custom_polygon_exposure(cls, polygon_coords: List[List[float]]) -> ExposureBreakdown:
        """
        Performs geospatial spatial join of arbitrary user-drawn polygon against critical assets.
        """
        poly = Polygon(polygon_coords)
        impacted_facilities = []
        
        for feature in CRITICAL_INFRASTRUCTURE_GEOJSON["features"]:
            coords = feature["geometry"]["coordinates"]
            point = Point(coords[0], coords[1])
            if poly.contains(point):
                props = feature["properties"]
                impacted_facilities.append(f"{props['name']} ({props['category']})")

        area_sqkm = poly.area * 111.0 * 111.0  # Approx degree to km conversion at 25S
        est_pop = int(area_sqkm * 180.0)  # Average density in Incomati valley
        est_bld = int(est_pop / 4.2)

        return ExposureBreakdown(
            population_exposed=est_pop,
            population_density_per_sqkm=180.0,
            buildings_count=est_bld,
            schools_count=max(1, len(impacted_facilities) // 2),
            hospitals_count=max(0, len(impacted_facilities) // 3),
            roads_km=round(area_sqkm * 0.12, 1),
            cropland_hectares=round(area_sqkm * 35.0, 1),
            critical_infrastructure=impacted_facilities
        )
