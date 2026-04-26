import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

BASE_DIR = "storage/converted"

@router.get("/download/{file_id}")
def download(file_id: str):
    path = os.path.join(BASE_DIR, f"{file_id}.woff2")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=path,
        filename="converted.woff2",
        media_type="font/woff2"
    )