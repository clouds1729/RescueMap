from fastapi import APIRouter, HTTPException

from app.models import VectorizeRequest
from app.utils.files import project_image_path
from app.vectorizer.detect_lines import detect_line_segments
from app.vectorizer.geojson_export import wall_segments_to_geojson
from app.vectorizer.merge_segments import merge_collinear_segments
from app.vectorizer.preprocess import load_image, preprocess_floorplan

router = APIRouter()


@router.post("/vectorize")
def vectorize_floorplan(request: VectorizeRequest) -> dict:
    image_path = project_image_path(request.project_id)
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Project image not found. Upload a floorplan first.")
    try:
        image = load_image(image_path)
        options = request.options
        binary = preprocess_floorplan(image, options.threshold_block_size, options.threshold_c)
        segments = detect_line_segments(binary, options.min_line_length, options.max_line_gap)
        merged = merge_collinear_segments(segments, distance_tolerance=options.merge_tolerance)
        return wall_segments_to_geojson(merged)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Vectorization failed: {exc}") from exc
