import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from app.tools.convert_ttf.service import convert_ttf_to_woff2
from app.tools.convert_ttf.db import add_file, get_file, cleanup

router = APIRouter()

BASE_DIR = "storage/tools/convert_ttf/files"


@router.post("/convert/ttf-to-woff2")
async def ttf_to_woff2(file: UploadFile = File(...)):
    result = await convert_ttf_to_woff2(file)

    file_id = result["file_id"]
    original_name = result["original_name"]

    add_file(file_id, original_name)

    return {
        "file_id": file_id,
        "download_url": f"/api/download/ttf-to-woff2/{file_id}",
        "original_name": original_name
    }


@router.get("/download/ttf-to-woff2/{file_id}")
def download(file_id: str):
    path = os.path.join(BASE_DIR, f"{file_id}.woff2")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    meta = get_file(file_id)
    original_name = meta["name"] if meta else file_id

    return FileResponse(
        path,
        filename=f"{original_name}.woff2",
        media_type="font/woff2"
    )
    
@router.get("/cron/cleanup/ttf-to-woff2") # This endpoint should be protected and only accessible by cron job or admin users
def cleanup_ttf():
    cleanup()
    
    for filename in os.listdir(BASE_DIR):
        if filename.endswith(".woff2"):
            path = os.path.join(BASE_DIR, filename)

            if os.path.exists(path):
                os.remove(path)
    
    return {
        "status": "ok", 
        "message": "Cleanup completed"
    }