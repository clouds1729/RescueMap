from fastapi import APIRouter

from app.models import RouteRequest
from app.routing.shortest_path import route_to_nearest_exit

router = APIRouter()


@router.post("/route")
def route(request: RouteRequest) -> dict:
    return route_to_nearest_exit(request.feature_collection, request.start)
