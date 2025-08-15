"""Application configuration using pydantic-settings."""
from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "crypto-signal-bot"
    port: int = 8000
    watchlist: list[str] = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
    timeframes: list[str] = ["1m", "15m"]
    sched_interval_sec: int = 60
    ema_fast: int = 9
    ema_slow: int = 21
    rsi_len: int = 14
    rsi_overbought: int = 65
    rsi_oversold: int = 35
    atr_len: int = 14
    atr_min: float = 5
    atr_max: float = 10000
    data_dir: str = "./data"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
