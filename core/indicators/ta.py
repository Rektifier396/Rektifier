"""Indicator calculations using pandas_ta."""
from __future__ import annotations

import pandas as pd
import pandas_ta as ta

from config import Settings


def add_indicators(df: pd.DataFrame, settings: Settings) -> pd.DataFrame:
    """Return DataFrame with technical indicators added."""
    df = df.copy()
    df["ema_fast"] = ta.ema(df["close"], length=settings.ema_fast)
    df["ema_slow"] = ta.ema(df["close"], length=settings.ema_slow)
    df["rsi"] = ta.rsi(df["close"], length=settings.rsi_len)
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=settings.atr_len)
    df["ema_fast_slope"] = df["ema_fast"].diff()
    return df
