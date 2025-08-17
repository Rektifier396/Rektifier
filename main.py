"""Main application entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from api.routes import router
from config import settings
from services.http_client import close_client, get_client
from services.scheduler import create_scheduler, update_once
from services.store import DataStore

logging.basicConfig(level=getattr(logging, settings.log_level))
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.INFO)

store = DataStore()
scheduler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global scheduler
    get_client()  # ensure client is created
    await update_once(settings, store)
    scheduler = create_scheduler(settings, store)
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)
        await close_client()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/", include_in_schema=False)
async def root() -> HTMLResponse:
    """Serve the lightweight trading dashboard UI."""
    index_path = Path(__file__).parent / "templates" / "index.html"
    return HTMLResponse(index_path.read_text(), media_type="text/html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=False)
