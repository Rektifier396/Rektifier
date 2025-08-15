"""Main application entry point."""
from __future__ import annotations

import asyncio
import logging

from fastapi import FastAPI

from api.routes import router
from config import settings
from services.scheduler import start_scheduler, update_once
from services.store import DataStore

logging.basicConfig(level=getattr(logging, settings.log_level))

app = FastAPI(title=settings.app_name)
app.include_router(router)

store = DataStore()


@app.on_event("startup")
async def startup_event() -> None:
    await update_once(settings, store)
    start_scheduler(settings, store)


@app.get("/")
async def root() -> dict:
    return {"app": settings.app_name}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=False)
