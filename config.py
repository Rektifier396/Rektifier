"""Application configuration using pydantic-settings."""
from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "crypto-signal-bot"
    port: int = 8000
    watchlist: list[str] = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
    timeframes: list[str] = ["1m", "15m"]
    allowed_origins: list[str] = ["*"]
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

    @field_validator("watchlist")
    @classmethod
    def dedup_watchlist(cls, v: list[str]) -> list[str]:
        """Ensure watchlist has unique symbols preserving order."""
        return list(dict.fromkeys(v))

    @field_validator("allowed_origins")
    @classmethod
    def dedup_origins(cls, v: list[str]) -> list[str]:
        """Ensure CORS origin list is unique while preserving order."""
        return list(dict.fromkeys(v))

    @field_validator("port", mode="before")
    @staticmethod
    def validate_port(value: int | str | None) -> int:
        """Ensure the port is a valid integer.

        Environments sometimes provide the port as a non-numeric placeholder
        (e.g. ``"${PORT}"``), which causes ``uvicorn`` to error. Fallback to
        the default ``8000`` when the value can't be converted to ``int``.
        """
        try:
            return int(value)
        except (TypeError, ValueError):
            return 8000

    class Config:
        env_file = ".env"


settings = Settings()
