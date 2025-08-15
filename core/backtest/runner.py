"""Basic vectorized backtesting."""
from __future__ import annotations

from pathlib import Path
from typing import List, Dict

import pandas as pd

from config import Settings
from core.signals.engine import generate_signal


class BacktestResult(pd.DataFrame):
    pass


def run_backtest(df: pd.DataFrame, settings: Settings) -> Dict:
    """Run simple backtest on DataFrame."""
    trades: List[Dict] = []
    position = None
    entry_price = sl = tp = 0.0
    equity = 0.0
    max_equity = 0.0
    max_drawdown = 0.0

    for i in range(len(df)):
        sub_df = df.iloc[: i + 1]
        signal = generate_signal(sub_df, settings)["signal"]
        row = df.iloc[i]
        if position is None and signal in {"LONG", "SHORT"}:
            position = signal
            entry_price = row["close"]
            atr = row["atr"]
            if position == "LONG":
                sl = entry_price - 1.5 * atr
                tp = entry_price + atr
            else:
                sl = entry_price + 1.5 * atr
                tp = entry_price - atr
            entry_time = row["open_time"]
        elif position:
            exit_price = None
            exit_time = row["open_time"]
            if position == "LONG":
                if row["low"] <= sl:
                    exit_price = sl
                elif row["high"] >= tp:
                    exit_price = tp
            else:
                if row["high"] >= sl:
                    exit_price = sl
                elif row["low"] <= tp:
                    exit_price = tp
            if exit_price is not None:
                pnl = exit_price - entry_price if position == "LONG" else entry_price - exit_price
                equity += pnl
                max_equity = max(max_equity, equity)
                drawdown = max_equity - equity
                max_drawdown = max(max_drawdown, drawdown)
                trades.append({
                    "entry_time": entry_time,
                    "exit_time": exit_time,
                    "side": position,
                    "entry": entry_price,
                    "exit": exit_price,
                    "pnl": pnl,
                })
                position = None
    wins = sum(1 for t in trades if t["pnl"] > 0)
    losses = sum(1 for t in trades if t["pnl"] <= 0)
    total_trades = len(trades)
    win_rate = wins / total_trades * 100 if total_trades else 0
    avg_win = sum(t["pnl"] for t in trades if t["pnl"] > 0) / wins if wins else 0
    avg_loss = sum(t["pnl"] for t in trades if t["pnl"] <= 0) / losses if losses else 0
    expectancy = win_rate / 100 * avg_win + (1 - win_rate / 100) * avg_loss

    return {
        "trades": trades,
        "total_trades": total_trades,
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "expectancy": expectancy,
        "max_drawdown": max_drawdown,
        "pnl": equity,
    }


def save_backtest(trades: List[Dict], symbol: str, timeframe: str, data_dir: str) -> Path:
    df = pd.DataFrame(trades)
    path = Path(data_dir) / f"backtest_{symbol}_{timeframe}.csv"
    df.to_csv(path, index=False)
    return path
