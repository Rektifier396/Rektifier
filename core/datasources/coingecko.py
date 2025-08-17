"""CoinGecko API client."""
from __future__ import annotations

import asyncio
from typing import Any

import httpx

from services.http_client import get_client

BASE_URL = "https://api.coingecko.com/api/v3"


async def _request(path: str, params: dict[str, Any] | None = None, retries: int = 3) -> Any:
    url = f"{BASE_URL}{path}"
    backoff = 1
    client = get_client()
    for attempt in range(retries):
        try:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(backoff)
            backoff *= 2


async def simple_price(ids: list[str], vs_currencies: list[str]) -> dict[str, Any]:
    params = {"ids": ",".join(ids), "vs_currencies": ",".join(vs_currencies)}
    return await _request("/simple/price", params)
