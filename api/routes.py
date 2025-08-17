"""FastAPI routes."""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from config import Settings, settings
from core.backtest.runner import run_backtest, save_backtest
from core.datasources import binance, coingecko, fng
from services.scheduler import update_once
from services.store import DataStore

router = APIRouter()


def get_store() -> DataStore:
    from main import store  # lazy import to avoid circular
    return store


def get_settings() -> Settings:
    return settings


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@router.get("/symbols")
async def get_symbols(settings: Settings = Depends(get_settings)) -> list[str]:
    """Return supported trading symbols."""
    return settings.watchlist


@router.get("/config")
async def get_config(settings: Settings = Depends(get_settings)) -> dict:
    return settings.model_dump()


@router.post("/config")
async def update_config(new: dict, settings: Settings = Depends(get_settings)) -> dict:
    for k, v in new.items():
        if hasattr(settings, k):
            setattr(settings, k, v)
    return settings.model_dump()


@router.get("/signals")
async def get_signal(symbol: str, timeframe: str, store: DataStore = Depends(get_store), settings: Settings = Depends(get_settings)) -> dict:
    sig = store.get_signal(symbol, timeframe)
    if not sig:
        await update_once(settings, store)
        sig = store.get_signal(symbol, timeframe)
    if not sig:
        raise HTTPException(404, "signal not found")
    return sig


@router.get("/signals/batch")
async def get_all_signals(store: DataStore = Depends(get_store), settings: Settings = Depends(get_settings)) -> list:
    sigs = store.all_signals()
    if not sigs:
        await update_once(settings, store)
        sigs = store.all_signals()
    return sigs


@router.get("/stats/daily")
async def stats_daily(query_date: Optional[date] = None, store: DataStore = Depends(get_store), settings: Settings = Depends(get_settings)) -> dict:
    tickers = {}
    for sym in settings.watchlist:
        tickers[sym] = await binance.get_24h_ticker(sym)
    ids = ["bitcoin", "ethereum", "binancecoin", "solana"]
    prices = await coingecko.simple_price(ids, ["usd"])
    index = await fng.get_index()
    signal_counts = len(store.all_signals())
    long_short = {
        "long": sum(1 for s in store.all_signals() if s["signal"] == "LONG"),
        "short": sum(1 for s in store.all_signals() if s["signal"] == "SHORT"),
    }
    return {
        "date": str(query_date or date.today()),
        "tickers": tickers,
        "coingecko": prices,
        "fear_greed": index,
        "signal_count": signal_counts,
        "long_short_ratio": long_short,
    }


@router.get("/backtest")
async def backtest(symbol: str, timeframe: str, days: int = 30, store: DataStore = Depends(get_store), settings: Settings = Depends(get_settings)) -> dict:
    df = store.get_klines(symbol, timeframe)
    if df is None:
        df = await binance.get_klines(symbol, timeframe)
        df["symbol"] = symbol
        df["interval"] = timeframe
        from core.indicators.ta import add_indicators

        df = add_indicators(df, settings)
    result = run_backtest(df, settings)
    path = save_backtest(result["trades"], symbol, timeframe, settings.data_dir)
    summary = result.copy()
    summary["csv"] = str(path)
    return summary
