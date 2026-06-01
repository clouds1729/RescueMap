from fastapi import APIRouter

from app.models import GeoJSONRequest
from app.qa.checks import run_qa_checks

router = APIRouter()


@router.post("/qa")
def qa_feature_collection(request: GeoJSONRequest) -> dict:
    return run_qa_checks(request.feature_collection)
