from datetime import UTC, datetime
from typing import Any


def build_qa_report(qa_result: dict[str, Any]) -> dict[str, Any]:
    return {"generated_at": datetime.now(UTC).isoformat(), "name": "RescueMap GIS QA Report", **qa_result}
