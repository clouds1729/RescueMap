from typing import Any
from uuid import uuid4

from app.vectorizer.detect_lines import Segment


def make_feature(feature_type: str, geometry: dict[str, Any], properties: dict[str, Any] | None = None) -> dict[str, Any]:
    props = dict(properties or {})
    props.setdefault("id", f"{feature_type}_{uuid4().hex[:8]}")
    props.setdefault("feature_type", feature_type)
    props.setdefault("floor", "1")
    return {"type": "Feature", "geometry": geometry, "properties": props}


def wall_segments_to_geojson(segments: list[Segment]) -> dict[str, Any]:
    features = []
    for segment in segments:
        x1, y1, x2, y2 = segment
        features.append(
            make_feature(
                "wall",
                {"type": "LineString", "coordinates": [[x1, y1], [x2, y2]]},
                {"source": "auto", "confidence": 0.75},
            )
        )
    return {"type": "FeatureCollection", "features": features}
