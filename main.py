"""Main application entry point."""
from __future__ import annotations

import asyncio
import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from api.routes import router
from config import settings
from services.scheduler import start_scheduler, update_once
from services.store import DataStore

logging.basicConfig(level=getattr(logging, settings.log_level))

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

store = DataStore()


@app.on_event("startup")
async def startup_event() -> None:
    await update_once(settings, store)
    start_scheduler(settings, store)


@app.get("/", include_in_schema=False)
async def root() -> HTMLResponse:
    """Serve the lightweight trading dashboard UI."""
    index_path = Path(__file__).parent / "templates" / "index.html"
    return HTMLResponse(index_path.read_text(), media_type="text/html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=False)
