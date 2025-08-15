"""Alternative.me Fear & Greed Index client."""
from __future__ import annotations

import asyncio
from typing import Any

import httpx

BASE_URL = "https://api.alternative.me/fng/"


async def get_index(retries: int = 3) -> dict[str, Any]:
    backoff = 1
    async with httpx.AsyncClient(timeout=10) as client:
        for attempt in range(retries):
            try:
                resp = await client.get(BASE_URL)
                resp.raise_for_status()
                data = resp.json()
                return data["data"][0]
            except httpx.HTTPError:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(backoff)
                backoff *= 2
