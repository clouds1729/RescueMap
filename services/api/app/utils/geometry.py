from math import hypot
from typing import Any

from shapely.geometry import shape


SUPPORTED_GEOMETRY = {
    "wall": {"LineString"},
    "door": {"LineString", "Point"},
    "room": {"Polygon"},
    "exit": {"Point"},
    "stairwell": {"Point", "Polygon"},
    "hazard": {"Point", "Polygon"},
    "restricted_area": {"Polygon"},
    "route": {"LineString"},
}


def feature_id(feature: dict[str, Any]) -> str:
    value = feature.get("properties", {}).get("id")
    return str(value) if value else ""


def shapely_geometry(feature: dict[str, Any]):
    return shape(feature["geometry"])


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return hypot(a[0] - b[0], a[1] - b[1])
