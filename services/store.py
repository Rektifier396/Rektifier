"""In-memory datastore for klines and signals."""
from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd


class DataStore:
    def __init__(self) -> None:
        self.klines: Dict[Tuple[str, str], pd.DataFrame] = {}
        self.signals: Dict[Tuple[str, str], dict] = {}

    def set_klines(self, symbol: str, timeframe: str, df: pd.DataFrame) -> None:
        self.klines[(symbol, timeframe)] = df

    def get_klines(self, symbol: str, timeframe: str) -> pd.DataFrame | None:
        return self.klines.get((symbol, timeframe))

    def set_signal(self, symbol: str, timeframe: str, sig: dict) -> None:
        self.signals[(symbol, timeframe)] = sig

    def get_signal(self, symbol: str, timeframe: str) -> dict | None:
        return self.signals.get((symbol, timeframe))

    def all_signals(self) -> list[dict]:
        return list(self.signals.values())
