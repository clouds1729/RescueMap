from app.vectorizer.geojson_export import wall_segments_to_geojson


def test_walls_convert_to_feature_collection():
    collection = wall_segments_to_geojson([(0, 0, 10, 0)])
    assert collection["type"] == "FeatureCollection"
    assert len(collection["features"]) == 1


def test_feature_ids_and_feature_type_created():
    feature = wall_segments_to_geojson([(0, 0, 10, 0)])["features"][0]
    assert feature["properties"]["id"].startswith("wall_")
    assert feature["properties"]["feature_type"] == "wall"
