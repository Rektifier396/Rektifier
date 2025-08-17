"""Utility functions for computing and caching market metrics."""
from __future__ import annotations

import pandas_ta as ta
from cachetools import TTLCache

from config import settings
from core.datasources import binance
from api.models import Metric

# Caches for OHLCV data and computed metrics
_ohlcv_cache: TTLCache = TTLCache(maxsize=100, ttl=settings.cache_ttl_seconds)
_metric_cache: TTLCache = TTLCache(maxsize=100, ttl=settings.cache_ttl_seconds)


async def fetch_ohlcv(symbol: str, interval: str, limit: int = 500):
    """Return OHLCV data for a symbol with caching."""
    key = (symbol, interval, limit)
    df = _ohlcv_cache.get(key)
    if df is None:
        df = await binance.get_klines(symbol, interval, limit=limit)
        _ohlcv_cache[key] = df
    return df


async def _compute_metric(symbol: str, interval: str) -> Metric:
    df = await fetch_ohlcv(symbol, interval, limit=500)
    df["rsi"] = ta.rsi(df["close"], length=14)
    df["ma50"] = df["close"].rolling(50).mean()
    df["ma200"] = df["close"].rolling(200).mean()
    df.fillna(0, inplace=True)

    price = float(df["close"].iloc[-1])
    rsi = float(df["rsi"].iloc[-1])
    ma50 = float(df["ma50"].iloc[-1])
    ma200 = float(df["ma200"].iloc[-1])
    recent_high = float(df["high"].tail(60).max())
    recent_low = float(df["low"].tail(60).min())

    ticker = await binance.get_24h_ticker(symbol)
    change_24h = float(ticker.get("priceChangePercent", 0))
    volume_24h = float(ticker.get("volume", 0))

    signals = {
        "rsi": "overbought" if rsi > 70 else "oversold" if rsi < 30 else "neutral",
        "ma_cross": "golden" if ma50 > ma200 else "death" if ma50 < ma200 else "none",
    }

    return Metric(
        symbol=symbol,
        price=price,
        change_24h=change_24h,
        volume_24h=volume_24h,
        rsi=rsi,
        ma50=ma50,
        ma200=ma200,
        recent_high=recent_high,
        recent_low=recent_low,
        signals=signals,
    )


async def get_metric(symbol: str, interval: str) -> Metric:
    """Retrieve metric for a symbol/interval with caching."""
    key = (symbol, interval)
    metric = _metric_cache.get(key)
    if metric is None:
        metric = await _compute_metric(symbol, interval)
        _metric_cache[key] = metric
    return metric
