"""Official administrative geography adapter for Mozambique, powered by geomoz.

The GeoMoz 2017 district/province datasets are the sole source of polygon
geometry here. No synthetic administrative boundary fallback is allowed.
"""
import json
import re
import unicodedata
from functools import lru_cache
from typing import Optional

from fastapi import HTTPException


FOCUS_DISTRICTS = {
    "manhica": ("manhica",),
    "marracuene": ("marracuene",),
    "matola": ("matola",),
    "boane": ("boane",),
    "magude": ("magude",),
    "moamba": ("moamba",),
    "maputo_city": ("cidade de maputo", "maputo cidade"),
    "chokwe": ("chokwe",),
}


def _normalize(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.strip().lower())


def _district_id(name: str, province: str, code: str) -> str:
    normalized = _normalize(name)
    if normalized in FOCUS_DISTRICTS["maputo_city"] and "maputo" in _normalize(province):
        return "maputo_city"
    for key, aliases in FOCUS_DISTRICTS.items():
        if normalized in aliases:
            return key
    slug = re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")
    return f"{slug}_{str(code).strip()}" if code else slug


@lru_cache(maxsize=1)
def _load_provinces():
    from geomoz import read_province
    data = read_province()
    return data.to_crs(epsg=4326) if data.crs and data.crs.to_epsg() != 4326 else data


@lru_cache(maxsize=1)
def _load_districts():
    from geomoz import read_district
    data = read_district()
    return data.to_crs(epsg=4326) if data.crs and data.crs.to_epsg() != 4326 else data


def _collection(frame, level: str) -> dict:
    """GeoMoz GeoDataFrame -> GeoJSON with stable ids and data provenance."""
    data = json.loads(frame.to_json())
    for feature in data["features"]:
        props = feature["properties"]
        if level == "districts":
            name = str(props.get("Distrito", ""))
            province = str(props.get("Provincia", ""))
            code = str(props.get("CodDist", ""))
            feature_id = _district_id(name, province, code)
        else:
            name = str(props.get("Provincia", ""))
            province = name
            code = str(props.get("CodProv", ""))
            feature_id = f"province_{code}" if code else "province_" + re.sub(r"[^a-z0-9]+", "_", _normalize(name))
        feature["id"] = feature_id
        props.update({
            "id": feature_id,
            "name": name,
            "province": province,
            "code": code,
            "country": "Mozambique",
            "data_mode": "OBSERVED",  # administrative geometry, not climate measurement
            "source": "GeoMoz — Mozambique administrative boundaries (2017)",
        })
    data.update({
        "name": f"Mozambique_GeoMoz_{level}",
        "source": "geomoz",
        "reference_year": 2017,
        "coordinate_system": "EPSG:4326",
        "geometry_mode": "ADMINISTRATIVE_DATA",
    })
    return data


def _load_collection(level: str, province: Optional[str] = None) -> dict:
    try:
        if level == "provinces":
            frame = _load_provinces()
            if province:
                frame = frame[frame["Provincia"].map(_normalize) == _normalize(province)]
        else:
            frame = _load_districts()
            if province:
                frame = frame[frame["Provincia"].map(_normalize) == _normalize(province)]
        result = _collection(frame, level)
    except Exception as exc:
        # An unavailable GeoMoz download must never be passed off as real geometry.
        raise HTTPException(
            status_code=503,
            detail=f"GeoMoz indisponível. Verifique a instalação e acesso ao dataset: {type(exc).__name__}",
        ) from exc
    return result


def provinces_geojson(province: Optional[str] = None) -> dict:
    return _load_collection("provinces", province)


def districts_geojson(province: Optional[str] = None, focus_only: bool = False) -> dict:
    result = _load_collection("districts", province)
    if focus_only:
        result["features"] = [
            f for f in result["features"] if f["id"] in FOCUS_DISTRICTS
        ]
        missing = set(FOCUS_DISTRICTS) - {f["id"] for f in result["features"]}
        if "maputo_city" in missing:
            # Maputo City is an administrative unit equivalent to a province.
            # Only accept an explicitly named GeoMoz city province, not Maputo Province.
            prov = provinces_geojson()
            for feat in prov["features"]:
                if _normalize(feat["properties"]["name"]) in ("cidade de maputo", "maputo cidade"):
                    city = json.loads(json.dumps(feat))
                    city["id"] = "maputo_city"
                    city["properties"].update({
                        "id": "maputo_city",
                        "name": "Maputo Cidade",
                        "province": "Maputo Cidade",
                        "source": "GeoMoz — province-level Maputo City boundary (2017)",
                    })
                    result["features"].append(city)
                    missing.remove("maputo_city")
                    break
        result["missing_focus_areas"] = sorted(missing)
        result["focus_only"] = True
    return result
