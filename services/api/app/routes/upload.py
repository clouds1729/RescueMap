from pathlib import Path

import cv2
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.utils.files import MEDIA_DIR, UPLOAD_DIR, ensure_runtime_dirs, new_project_id, project_image_path
from app.utils.pdf import first_page_to_png

router = APIRouter()
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf"}


@router.post("/upload")
async def upload_floorplan(file: UploadFile = File(...)) -> dict[str, object]:
    ensure_runtime_dirs()
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload PNG, JPG, JPEG, or PDF.")

    project_id = new_project_id()
    upload_path = UPLOAD_DIR / f"{project_id}{suffix}"
    upload_path.write_bytes(await file.read())
    image_path = project_image_path(project_id)

    try:
        if suffix == ".pdf":
            first_page_to_png(upload_path, image_path)
        else:
            image = cv2.imread(str(upload_path), cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("Uploaded image could not be decoded.")
            cv2.imwrite(str(image_path), image)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=500, detail="Could not load converted floorplan image.")
    height, width = image.shape[:2]
    return {"project_id": project_id, "image_url": f"/media/{image_path.name}", "width": width, "height": height}
