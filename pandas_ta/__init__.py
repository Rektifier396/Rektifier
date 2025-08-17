"""Minimal subset of pandas_ta used for tests.

This lightweight module implements only the indicators required by the
project's unit tests: ``ema``, ``rsi`` and ``atr``.  The real
``pandas_ta`` package provides many more indicators, but pulling in the
full dependency (which in turn depends on ``talib``) is unnecessary for
our purposes and problematic in restricted environments.

The implementations below rely solely on ``pandas`` so they work with
small DataFrames and do not require any optional native extensions.
"""
from __future__ import annotations

import pandas as pd


def ema(close: pd.Series, length: int | None = None, **kwargs) -> pd.Series:
    """Exponential moving average using pandas ``ewm``.

    This mirrors the API of :func:`pandas_ta.ema` but always returns a
    ``Series`` even when ``length`` is greater than the input length,
    which is convenient for small test datasets.
    """
    length = int(length) if length and length > 0 else 10
    adjust = kwargs.get("adjust", False)
    return close.ewm(span=length, adjust=adjust).mean()


def rsi(close: pd.Series, length: int = 14, **kwargs) -> pd.Series:
    """Relative Strength Index implementation."""
    length = int(length) if length and length > 0 else 14
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / length, min_periods=1, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / length, min_periods=1, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int = 14, **kwargs) -> pd.Series:
    """Average True Range implementation."""
    length = int(length) if length and length > 0 else 14
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    atr = tr.ewm(alpha=1 / length, min_periods=1, adjust=False).mean()
    return atr

__all__ = ["ema", "rsi", "atr"]
