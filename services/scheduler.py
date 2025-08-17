"""Scheduler for updating market data and signals."""
from __future__ import annotations

from pathlib import Path
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Settings
from core.datasources import binance
from core.indicators.ta import add_indicators
from core.signals.engine import generate_signal
from services.store import DataStore


logger = logging.getLogger(__name__)


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
            try:
                df.to_parquet(Path(settings.data_dir) / f"{symbol}_{tf}.parquet", index=False)
            except ImportError:
                logger.warning(
                    "pyarrow or fastparquet is not installed; saving %s %s data as CSV",
                    symbol,
                    tf,
                )
                df.to_csv(Path(settings.data_dir) / f"{symbol}_{tf}.csv", index=False)


def create_scheduler(settings: Settings, store: DataStore) -> AsyncIOScheduler:
    """Configure the AsyncIO scheduler for periodic updates."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        update_once,
        "interval",
        seconds=settings.sched_interval_sec,
        args=[settings, store],
        max_instances=1,
        coalesce=True,
        misfire_grace_time=settings.sched_interval_sec,
    )
    return scheduler
