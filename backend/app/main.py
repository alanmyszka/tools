import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.tools.convert_ttf import convert_ttf, download

load_dotenv()

ENV = os.getenv("ENVIRONMENT", "dev")

ENABLE_DOCS = ENV != "prod"

app = FastAPI(
    title="Tools API",
    docs_url="/api/swagger" if ENABLE_DOCS else None,
    redoc_url="/api/redoc" if ENABLE_DOCS else None,
    openapi_url="/api/openapi.json" if ENABLE_DOCS else None,
)

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