from typing import Any, Literal

from pydantic import BaseModel, Field


Coordinate = list[float]


class VectorizeOptions(BaseModel):
    threshold_block_size: int = Field(default=31, ge=3)
    threshold_c: int = 10
    min_line_length: int = Field(default=40, ge=1)
    max_line_gap: int = Field(default=10, ge=0)
    merge_tolerance: float = Field(default=8, ge=0)


class VectorizeRequest(BaseModel):
    project_id: str
    options: VectorizeOptions = Field(default_factory=VectorizeOptions)


class GeoJSONRequest(BaseModel):
    feature_collection: dict[str, Any]


class RouteRequest(GeoJSONRequest):
    start: tuple[float, float]


class QAIssue(BaseModel):
    id: str
    severity: Literal["error", "warning", "info"]
    message: str
    feature_ids: list[str] = Field(default_factory=list)


class QAResponse(BaseModel):
    summary: dict[str, int]
    checks: list[QAIssue]
