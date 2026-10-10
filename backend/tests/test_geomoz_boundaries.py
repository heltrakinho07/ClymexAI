"""Network-independent contract tests for CLYMEX/GeoMoz integration."""
import copy
import json

from app.services import administrative_boundaries as geo


def test_district_slug_accents_and_maputo_city():
    assert geo._district_id("Chókwè", "Gaza", "40") == "chokwe"
    assert geo._district_id("Manhiça", "Maputo Província", "41") == "manhica"
    assert geo._district_id("Maputo", "Maputo Cidade", "01") == "maputo_city"
    assert geo._district_id("Maputo", "Maputo Província", "01") != "maputo_city"


class SampleFrame:
    def to_json(self):
        return json.dumps({
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "Distrito": "Chókwè",
                        "Provincia": "Gaza",
                        "CodDist": "42",
                        "CodProv": "09",
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[33.0, -25.0], [33.1, -25.0], [33.1, -24.9], [33.0, -25.0]]],
                    },
                }
            ],
        })


def test_geojson_contract_and_geometry_preserved():
    source = json.loads(SampleFrame().to_json())["features"][0]["geometry"]
    result = geo._collection(SampleFrame(), "districts")
    feature = result["features"][0]
    assert result["source"] == "geomoz"
    assert result["reference_year"] == 2017
    assert feature["properties"]["name"] == "Chókwè"
    assert feature["id"] == "chokwe"
    assert feature["geometry"] == source


def test_focus_does_not_invent_missing_district_polygons(monkeypatch):
    district_data = {
        "type": "FeatureCollection",
        "features": [
            {"id": "manhica", "properties": {"id": "manhica", "name": "Manhiça"}, "geometry": {"type": "Polygon", "coordinates": []}},
            {"id": "maputo_city", "properties": {"id": "maputo_city", "name": "Maputo Cidade"}, "geometry": {"type": "Polygon", "coordinates": []}},
            {"id": "other_area", "properties": {"id": "other_area", "name": "Other"}, "geometry": {"type": "Polygon", "coordinates": []}},
        ],
    }
    monkeypatch.setattr(geo, "_load_collection", lambda level, province=None: copy.deepcopy(district_data))
    result = geo.districts_geojson(focus_only=True)
    assert {f["id"] for f in result["features"]} == {"manhica", "maputo_city"}
    assert "chokwe" in result["missing_focus_areas"]
    assert result["focus_only"] is True
