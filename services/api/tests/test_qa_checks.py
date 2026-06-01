from app.qa.checks import run_qa_checks


def fc(features):
    return {"type": "FeatureCollection", "features": features}


def room(fid, coords, label=None):
    props = {"id": fid, "feature_type": "room", "floor": "1"}
    if label:
        props["label"] = label
    return {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [coords]}, "properties": props}


def test_missing_feature_collection_returns_error():
    result = run_qa_checks({"type": "Feature"})
    assert result["summary"]["errors"] == 1


def test_missing_feature_id_returns_error():
    result = run_qa_checks(
        fc(
            [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [0, 0]},
                    "properties": {"feature_type": "exit"},
                }
            ]
        )
    )
    assert any(issue["id"] == "missing_feature_id" for issue in result["checks"])


def test_unsupported_geometry_for_type_returns_error():
    result = run_qa_checks(
        fc(
            [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [0, 0]},
                    "properties": {"id": "wall_bad", "feature_type": "wall"},
                }
            ]
        )
    )
    assert any(issue["id"] == "unsupported_geometry_for_type" for issue in result["checks"])


def test_room_without_label_returns_warning():
    result = run_qa_checks(fc([room("room_1", [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]])]))
    assert any(issue["id"] == "missing_room_label" for issue in result["checks"])


def test_no_exit_returns_warning():
    result = run_qa_checks(fc([]))
    assert any(issue["id"] == "missing_exit" for issue in result["checks"])


def test_overlapping_rooms_returns_warning():
    result = run_qa_checks(
        fc(
            [
                room("room_1", [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]], "A"),
                room("room_2", [[5, 5], [15, 5], [15, 15], [5, 15], [5, 5]], "B"),
            ]
        )
    )
    assert any(issue["id"] == "overlapping_rooms" for issue in result["checks"])


def test_invalid_polygon_returns_error():
    result = run_qa_checks(fc([room("room_bad", [[0, 0], [10, 10], [10, 0], [0, 10], [0, 0]], "Bad")]))
    assert any(issue["id"] == "invalid_polygon" for issue in result["checks"])


def test_room_without_exit_route_returns_warning_when_graph_incomplete():
    result = run_qa_checks(
        fc(
            [
                room("room_far", [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]], "Far Room"),
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [1000, 1000]},
                    "properties": {"id": "exit_far", "feature_type": "exit", "label": "Far Exit"},
                },
            ]
        )
    )
    assert any(issue["id"] == "room_without_exit_route" for issue in result["checks"])


def test_local_coordinates_notice_returns_info():
    result = run_qa_checks(fc([]))
    assert result["summary"]["info"] == 1
    assert any(issue["id"] == "local_coordinates_notice" for issue in result["checks"])
