from typing import Any

from shapely.errors import ShapelyError

from app.routing.shortest_path import route_to_nearest_exit
from app.utils.geometry import SUPPORTED_GEOMETRY, feature_id, shapely_geometry


def _issue(id_: str, severity: str, message: str, feature_ids: list[str] | None = None) -> dict[str, Any]:
    return {"id": id_, "severity": severity, "message": message, "feature_ids": feature_ids or []}


def _empty_response(issue: dict[str, Any], total_features: int = 0) -> dict[str, Any]:
    return {"summary": {"total_features": total_features, "errors": 1, "warnings": 0, "info": 0}, "checks": [issue]}


def _summary(features: list[dict[str, Any]], issues: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total_features": len(features),
        "errors": sum(1 for item in issues if item["severity"] == "error"),
        "warnings": sum(1 for item in issues if item["severity"] == "warning"),
        "info": sum(1 for item in issues if item["severity"] == "info"),
    }


def run_qa_checks(feature_collection: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(feature_collection, dict) or feature_collection.get("type") != "FeatureCollection":
        return _empty_response(_issue("malformed_feature_collection", "error", "Input must be a GeoJSON FeatureCollection."))
    features = feature_collection.get("features")
    if not isinstance(features, list):
        return _empty_response(
            _issue("malformed_feature_collection", "error", "FeatureCollection.features must be a list."), 0
        )

    issues: list[dict[str, Any]] = [
        _issue(
            "local_coordinates_notice",
            "info",
            "Coordinates are local floorplan pixels until the project is georeferenced.",
        )
    ]
    rooms: list[tuple[str, Any, dict[str, Any]]] = []
    doors: list[tuple[str, Any]] = []
    exits: list[tuple[str, Any]] = []
    walls: list[tuple[str, Any]] = []

    for index, feature in enumerate(features):
        fid = feature_id(feature)
        if not fid:
            issues.append(_issue("missing_feature_id", "error", f"Feature at index {index} is missing properties.id."))
        feature_type = feature.get("properties", {}).get("feature_type")
        if not feature_type:
            issues.append(_issue("missing_feature_type", "error", f"Feature {fid or index} is missing feature_type.", [fid] if fid else []))
            continue
        geom_type = feature.get("geometry", {}).get("type")
        if feature_type not in SUPPORTED_GEOMETRY:
            issues.append(_issue("unsupported_feature_type", "error", f"Unsupported feature_type '{feature_type}'.", [fid]))
            continue
        if geom_type not in SUPPORTED_GEOMETRY[feature_type]:
            issues.append(
                _issue(
                    "unsupported_geometry_for_type",
                    "error",
                    f"{feature_type} must use {sorted(SUPPORTED_GEOMETRY[feature_type])}, not {geom_type}.",
                    [fid],
                )
            )
            continue
        try:
            geom = shapely_geometry(feature)
        except (KeyError, TypeError, ShapelyError, ValueError) as exc:
            issues.append(_issue("invalid_geometry", "error", f"Feature {fid or index} has invalid geometry: {exc}", [fid] if fid else []))
            continue
        if feature_type in {"room", "restricted_area", "hazard", "stairwell"} and geom_type == "Polygon" and not geom.is_valid:
            issues.append(_issue("invalid_polygon", "error", f"Polygon geometry is invalid for feature {fid}.", [fid]))
        if feature_type == "room":
            rooms.append((fid, geom, feature))
            if not (feature.get("properties", {}).get("label") or feature.get("properties", {}).get("name")):
                issues.append(_issue("missing_room_label", "warning", f"Room {fid} is missing a label.", [fid]))
        elif feature_type == "door":
            doors.append((fid, geom))
        elif feature_type == "exit":
            exits.append((fid, geom))
        elif feature_type == "wall":
            walls.append((fid, geom))

    if not exits:
        issues.append(_issue("missing_exit", "warning", "No exit features found.", []))

    for i, (fid_a, geom_a, _) in enumerate(rooms):
        for fid_b, geom_b, _ in rooms[i + 1 :]:
            if geom_a.is_valid and geom_b.is_valid and geom_a.intersects(geom_b) and geom_a.intersection(geom_b).area > 1:
                issues.append(_issue("overlapping_rooms", "warning", f"Rooms {fid_a} and {fid_b} overlap.", [fid_a, fid_b]))

    if doors:
        boundary_targets = [room[1].boundary for room in rooms if room[1].is_valid] + [wall[1] for wall in walls]
        for fid, geom in doors:
            probe = geom if geom.geom_type == "Point" else geom.centroid
            if not boundary_targets or min(probe.distance(target) for target in boundary_targets) > 8:
                issues.append(_issue("isolated_door", "warning", f"Door {fid} is not near a wall or room boundary.", [fid]))

    if rooms and exits:
        for fid, geom, _ in rooms:
            start = geom.representative_point()
            try:
                result = route_to_nearest_exit(feature_collection, (start.x, start.y))
                status = result["route"]["properties"]["status"]
            except Exception:
                status = "error"
            if status in {"error", "fallback"}:
                issues.append(_issue("room_without_exit_route", "warning", f"Room {fid} has no graph route to an exit.", [fid]))

    return {"summary": _summary(features, issues), "checks": issues}
