from fastapi import APIRouter, UploadFile, File
from app.tools.convert_ttf.font_converter import convert_ttf_to_woff2

router = APIRouter()

@router.post("/ttf-to-woff2")
async def ttf_to_woff2(file: UploadFile = File(...)):
    file_id = await convert_ttf_to_woff2(file)

    return {
        "file_id": file_id,
        "download_url": f"/api/download/{file_id}"
    }