"""Binance public API client."""
from __future__ import annotations

import asyncio
from typing import Any

import httpx
import pandas as pd

BASE_URL = "https://api.binance.com/api/v3"


async def _request(url: str, params: dict[str, Any] | None = None, retries: int = 3) -> Any:
    """Perform HTTP GET with basic retry/backoff."""
    backoff = 1
    async with httpx.AsyncClient(timeout=10) as client:
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


async def get_klines(symbol: str, interval: str, limit: int = 1000) -> pd.DataFrame:
    """Fetch kline data and return as DataFrame."""
    url = f"{BASE_URL}/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    data = await _request(url, params)
    df = pd.DataFrame(
        data,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "trades",
            "taker_base_volume",
            "taker_quote_volume",
            "ignore",
        ],
    )
    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    return df


async def get_24h_ticker(symbol: str) -> dict[str, Any]:
    url = f"{BASE_URL}/ticker/24hr"
    params = {"symbol": symbol}
    return await _request(url, params)


async def get_price(symbol: str) -> float:
    url = f"{BASE_URL}/ticker/price"
    params = {"symbol": symbol}
    data = await _request(url, params)
    return float(data["price"])
