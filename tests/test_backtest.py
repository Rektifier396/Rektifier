import pandas as pd

from config import Settings
from core.indicators.ta import add_indicators
from core.backtest.runner import run_backtest


def test_backtest_returns_summary():
    settings = Settings()
    data = {
        "open_time": pd.date_range("2023-01-01", periods=50, freq="T"),
        "open": range(50),
        "high": [x + 1 for x in range(50)],
        "low": [x - 1 for x in range(50)],
        "close": range(50),
        "volume": [100] * 50,
    }
    df = pd.DataFrame(data)
    df = add_indicators(df, settings)
    summary = run_backtest(df, settings)
    assert {"trades", "total_trades", "win_rate", "pnl"}.issubset(summary.keys())
