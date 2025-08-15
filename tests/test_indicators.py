import pytest
import pandas as pd
import pandas_ta as ta

from config import Settings
from core.indicators.ta import add_indicators


def test_indicators_match():
    data = {
        "open": [1, 2, 3, 4, 5, 6, 7],
        "high": [1, 2, 3, 4, 5, 6, 7],
        "low": [1, 2, 3, 4, 5, 6, 7],
        "close": [1, 2, 3, 4, 5, 6, 7],
        "volume": [1, 1, 1, 1, 1, 1, 1],
    }
    df = pd.DataFrame(data)
    settings = Settings()
    res = add_indicators(df, settings)
    ema_fast = ta.ema(df["close"], length=settings.ema_fast)
    assert res["ema_fast"].iloc[-1] == pytest.approx(ema_fast.iloc[-1])
    rsi = ta.rsi(df["close"], length=settings.rsi_len)
    assert res["rsi"].iloc[-1] == pytest.approx(rsi.iloc[-1])
