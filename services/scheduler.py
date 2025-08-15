"""Scheduler for updating market data and signals."""
from __future__ import annotations

from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Settings
from core.datasources import binance
from core.indicators.ta import add_indicators
from core.signals.engine import generate_signal
from services.store import DataStore


async def update_once(settings: Settings, store: DataStore) -> None:
    for symbol in settings.watchlist:
        for tf in settings.timeframes:
            df = await binance.get_klines(symbol, tf)
            df["symbol"] = symbol
            df["interval"] = tf
            df = add_indicators(df, settings)
            store.set_klines(symbol, tf, df)
            sig = generate_signal(df, settings)
            store.set_signal(symbol, tf, sig)
            Path(settings.data_dir).mkdir(parents=True, exist_ok=True)
            df.to_parquet(Path(settings.data_dir) / f"{symbol}_{tf}.parquet", index=False)


def start_scheduler(settings: Settings, store: DataStore) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_once, "interval", seconds=settings.sched_interval_sec, args=[settings, store])
    scheduler.start()
    return scheduler
