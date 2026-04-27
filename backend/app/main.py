import os
import time
import platform
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.tools.convert_ttf import route as convert_ttf

load_dotenv()

START_TIME = time.time()
VERSION = "mvp-0.1.0"
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

app.include_router(convert_ttf.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok",
            "version": VERSION,
    }

@app.get("/api/status") # Allow only trusted IP addresses to access this endpoint in production
def status():
    return {
        "status": "ok",
        "version": VERSION,
        "environment": ENV,
        "uptime_seconds": int(time.time() - START_TIME),
        "system": {
            "python": platform.python_version(),
            "platform": platform.system(),
        },
        "tools": [
            "convert-ttf",
        ],
    }