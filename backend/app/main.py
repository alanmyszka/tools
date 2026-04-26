from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.tools.convert_ttf import convert_ttf, download

app = FastAPI(title="Tools API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(convert_ttf.router, prefix="/api/convert")
app.include_router(download.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok"}