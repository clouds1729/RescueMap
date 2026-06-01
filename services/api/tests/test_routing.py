from app.routing.shortest_path import route_to_nearest_exit


def test_start_and_exit_returns_route():
    fc = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [10, 0]}, "properties": {"id": "exit_1", "feature_type": "exit"}}
        ],
    }
    result = route_to_nearest_exit(fc, (0, 0))
    assert result["route"]["properties"]["status"] in {"ok", "fallback"}
    assert result["route"]["geometry"]["type"] == "LineString"


def test_no_exit_returns_error_gracefully():
    result = route_to_nearest_exit({"type": "FeatureCollection", "features": []}, (0, 0))
    assert result["route"]["properties"]["status"] == "error"
    assert result["warnings"] == ["Add at least one exit before routing."]


def test_disconnected_graph_returns_fallback_when_exit_exists():
    fc = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [1000, 1000]},
                "properties": {"id": "exit_far", "feature_type": "exit"},
            }
        ],
    }
    result = route_to_nearest_exit(fc, (0, 0))
    assert result["route"]["properties"]["status"] == "fallback"
    assert result["route"]["properties"]["distance_px"] > 0
    assert result["warnings"] == ["Fallback straight-line route used because indoor network is incomplete."]
