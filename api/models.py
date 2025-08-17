from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class Metric(BaseModel):
    symbol: str
    price: float
    change_24h: float
    volume_24h: float
    rsi: float
    ma50: float
    ma200: float
    recent_high: float
    recent_low: float
    signals: dict[str, str]


class SummaryResponse(BaseModel):
    interval: str
    as_of: datetime
    data: list[Metric]
