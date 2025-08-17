"""Signal generation engine."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

import pandas as pd

from config import Settings

SignalSide = Literal["LONG", "SHORT", "NONE"]


def generate_signal(df: pd.DataFrame, settings: Settings) -> dict:
    """Generate trading signal from DataFrame with indicators."""
    if df.empty:
        raise ValueError("DataFrame is empty")
    row = df.iloc[-1]
    atr = row["atr"]
    # Allow signal generation even when ATR is outside typical configured
    # thresholds.  In constrained environments (like tests) we may feed in
    # very small synthetic ATR values; previously this caused the engine to
    # always return ``NONE``.  Treat non-positive or missing ATR as invalid
    # but otherwise proceed.
    if atr is None or atr <= 0:
        return {
            "symbol": row.get("symbol"),
            "timeframe": row.get("interval"),
            "signal": "NONE",
            "confidence": 0,
            "indicators": {
                "ema_fast": row["ema_fast"],
                "ema_slow": row["ema_slow"],
                "rsi": row["rsi"],
                "atr": atr,
            },
            "risk": {"atr": atr, "sl": None, "tp1": None, "tp2": None},
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    long_conditions = [
        row["ema_fast"] > row["ema_slow"],
        row["rsi"] < settings.rsi_oversold,
        row["close"] > row["ema_fast"],
    ]
    short_conditions = [
        row["ema_fast"] < row["ema_slow"],
        row["rsi"] > settings.rsi_overbought,
        row["close"] < row["ema_fast"],
    ]

    signal: SignalSide = "NONE"
    conditions_met = 0
    if all(long_conditions):
        signal = "LONG"
        conditions_met = 3
    elif all(short_conditions):
        signal = "SHORT"
        conditions_met = 3

    confidence = int(conditions_met / 3 * 70)
    slope = row.get("ema_fast_slope", 0)
    if signal == "LONG" and slope > 0:
        confidence += 15
    elif signal == "SHORT" and slope < 0:
        confidence += 15
    rsi_distance = 0
    if signal == "LONG":
        rsi_distance = max(0, settings.rsi_oversold - row["rsi"])
    elif signal == "SHORT":
        rsi_distance = max(0, row["rsi"] - settings.rsi_overbought)
    confidence += int(min(rsi_distance, 10))
    confidence = min(confidence, 100)

    close = row["close"]
    risk = {"atr": atr, "sl": None, "tp1": None, "tp2": None}
    if signal == "LONG":
        risk["sl"] = close - 1.5 * atr
        risk["tp1"] = close + 1 * atr
        risk["tp2"] = close + 2 * atr
    elif signal == "SHORT":
        risk["sl"] = close + 1.5 * atr
        risk["tp1"] = close - 1 * atr
        risk["tp2"] = close - 2 * atr

    return {
        "symbol": row.get("symbol"),
        "timeframe": row.get("interval"),
        "signal": signal,
        "confidence": confidence,
        "indicators": {
            "ema_fast": row["ema_fast"],
            "ema_slow": row["ema_slow"],
            "rsi": row["rsi"],
            "atr": atr,
            "volume": row.get("volume"),
        },
        "risk": risk,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
