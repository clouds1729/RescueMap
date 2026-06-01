import json

from fastapi import APIRouter
from fastapi.responses import Response

from app.models import GeoJSONRequest

router = APIRouter()


@router.post("/export/geojson")
def export_geojson(request: GeoJSONRequest) -> Response:
    return Response(
        content=json.dumps(request.feature_collection, indent=2),
        media_type="application/geo+json",
        headers={"Content-Disposition": 'attachment; filename="rescuemap-export.geojson"'},
    )
