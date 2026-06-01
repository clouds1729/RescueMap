from pathlib import Path
from uuid import uuid4

ROOT_DIR = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT_DIR / ".runtime"
UPLOAD_DIR = RUNTIME_DIR / "uploads"
MEDIA_DIR = RUNTIME_DIR / "media"


def ensure_runtime_dirs() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)


def new_project_id() -> str:
    return f"project_{uuid4().hex[:12]}"


def project_image_path(project_id: str) -> Path:
    return MEDIA_DIR / f"{project_id}.png"
