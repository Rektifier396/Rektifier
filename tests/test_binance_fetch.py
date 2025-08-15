import asyncio

import pandas as pd

from core.datasources import binance


def test_binance_kline_fetch():
    df = asyncio.run(binance.get_klines("BTCUSDT", "1m", limit=5))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert {"open", "high", "low", "close", "volume"}.issubset(df.columns)
