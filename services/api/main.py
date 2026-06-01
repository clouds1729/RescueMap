from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes import export, qa, routing, upload, vectorize
from app.utils.files import MEDIA_DIR

app = FastAPI(title="RescueMap API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "rescuemap-api"}


app.include_router(upload.router, prefix="/api")
app.include_router(vectorize.router, prefix="/api")
app.include_router(qa.router, prefix="/api")
app.include_router(routing.router, prefix="/api")
app.include_router(export.router, prefix="/api")
