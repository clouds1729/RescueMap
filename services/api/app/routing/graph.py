from typing import Any

import networkx as nx
from shapely.geometry import shape

from app.utils.geometry import distance


def point_for_feature(feature: dict[str, Any]) -> tuple[float, float] | None:
    geom = shape(feature["geometry"])
    if geom.geom_type == "Point":
        return (float(geom.x), float(geom.y))
    if geom.geom_type == "Polygon":
        point = geom.representative_point()
        return (float(point.x), float(point.y))
    if geom.geom_type == "LineString":
        point = geom.interpolate(0.5, normalized=True)
        return (float(point.x), float(point.y))
    return None


def build_navigation_graph(
    feature_collection: dict[str, Any],
    start: tuple[float, float] | None = None,
    connect_threshold: float = 250,
) -> tuple[nx.Graph, list[str]]:
    graph = nx.Graph()
    exits: list[str] = []
    features = feature_collection.get("features", [])
    nodes: list[tuple[str, tuple[float, float], str]] = []

    if start is not None:
        graph.add_node("route_start", coord=start, feature_type="route_start")
        nodes.append(("route_start", start, "route_start"))

    for feature in features:
        props = feature.get("properties", {})
        feature_type = props.get("feature_type")
        if feature_type not in {"room", "door", "exit", "stairwell"}:
            continue
        point = point_for_feature(feature)
        fid = props.get("id")
        if not point or not fid:
            continue
        graph.add_node(fid, coord=point, feature_type=feature_type)
        nodes.append((fid, point, feature_type))
        if feature_type == "exit":
            exits.append(fid)

    for index, (node_id, node_point, _) in enumerate(nodes):
        for other_id, other_point, _ in nodes[index + 1 :]:
            edge_distance = distance(node_point, other_point)
            if edge_distance > connect_threshold:
                continue
            graph.add_edge(node_id, other_id, weight=edge_distance)
    return graph, exits


def nearest_feature_node(graph: nx.Graph, point: tuple[float, float]) -> str | None:
    if graph.number_of_nodes() == 0:
        return None
    return min(graph.nodes, key=lambda node: distance(point, graph.nodes[node]["coord"]))
