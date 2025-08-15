from datetime import datetime

import pandas as pd

from config import Settings
from core.signals.engine import generate_signal


def _df_from_row(row: dict) -> pd.DataFrame:
    return pd.DataFrame([row])


def test_long_signal():
    settings = Settings()
    row = {
        "open_time": datetime.utcnow(),
        "open": 1,
        "high": 1.2,
        "low": 0.8,
        "close": 1.1,
        "volume": 100,
        "ema_fast": 1.05,
        "ema_slow": 1.0,
        "rsi": 30,
        "atr": 0.1,
        "ema_fast_slope": 0.01,
        "symbol": "TEST",
        "interval": "1m",
    }
    df = _df_from_row(row)
    sig = generate_signal(df, settings)
    assert sig["signal"] == "LONG"


def test_short_signal():
    settings = Settings()
    row = {
        "open_time": datetime.utcnow(),
        "open": 1,
        "high": 1.2,
        "low": 0.8,
        "close": 0.9,
        "volume": 100,
        "ema_fast": 0.95,
        "ema_slow": 1.0,
        "rsi": 70,
        "atr": 0.1,
        "ema_fast_slope": -0.01,
        "symbol": "TEST",
        "interval": "1m",
    }
    df = _df_from_row(row)
    sig = generate_signal(df, settings)
    assert sig["signal"] == "SHORT"
