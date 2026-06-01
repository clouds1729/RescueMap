from typing import Any
from uuid import uuid4

import networkx as nx

from app.routing.graph import build_navigation_graph
from app.utils.geometry import distance


def _exit_points(feature_collection: dict[str, Any]) -> list[tuple[float, float]]:
    points = []
    for feature in feature_collection.get("features", []):
        if feature.get("properties", {}).get("feature_type") == "exit" and feature.get("geometry", {}).get("type") == "Point":
            x, y = feature["geometry"]["coordinates"]
            points.append((float(x), float(y)))
    return points


def _route_feature(coords: list[tuple[float, float]], status: str) -> dict[str, Any]:
    total = sum(distance(coords[i], coords[i + 1]) for i in range(len(coords) - 1)) if len(coords) > 1 else 0
    props: dict[str, Any] = {
        "id": f"route_{uuid4().hex[:8]}",
        "feature_type": "route",
        "distance_px": round(total, 2),
        "status": status,
    }
    return {"type": "Feature", "geometry": {"type": "LineString", "coordinates": coords}, "properties": props}


def route_to_nearest_exit(feature_collection: dict[str, Any], start: tuple[float, float]) -> dict[str, Any]:
    exits = _exit_points(feature_collection)
    if not exits:
        return {
            "route": _route_feature([start], "error"),
            "warnings": ["Add at least one exit before routing."],
        }

    graph, exit_nodes = build_navigation_graph(feature_collection, start=start)
    if graph.has_node("route_start") and exit_nodes:
        try:
            paths = []
            for exit_node in exit_nodes:
                path = nx.shortest_path(graph, "route_start", exit_node, weight="weight")
                length = nx.shortest_path_length(graph, "route_start", exit_node, weight="weight")
                paths.append((length, path))
            _, best_path = min(paths, key=lambda item: item[0])
            coords = [graph.nodes[node]["coord"] for node in best_path]
            return {"route": _route_feature(coords, "ok"), "warnings": []}
        except (nx.NetworkXNoPath, ValueError):
            pass

    nearest_exit = min(exits, key=lambda point: distance(start, point))
    return {
        "route": _route_feature([start, nearest_exit], "fallback"),
        "warnings": ["Fallback straight-line route used because indoor network is incomplete."],
    }
