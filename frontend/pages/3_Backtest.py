"""Backtest page allowing quick simulations."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from utils.api_client import get_client
from utils.theme import inject_theme, build_sidebar

load_dotenv()
if "theme" not in st.session_state:
    st.session_state["theme"] = "Dark"

inject_theme()
client = get_client()
build_sidebar(client)

st.title("Backtest")

symbol_default = (st.session_state.get("watchlist") or ["BTCUSDT"])[0]
timeframe_default = st.session_state.get("timeframe", "1m")

with st.form("backtest"):
    cols = st.columns(3)
    symbol = cols[0].text_input("Symbol", symbol_default)
    timeframe = cols[1].text_input("Timeframe", timeframe_default)
    days = cols[2].number_input("Days", min_value=1, max_value=365, value=30)
    run = st.form_submit_button("Run")

if run:
    @st.cache_data(ttl=30)
    def run_backtest(sym: str, tf: str, d: int):
        return client.backtest(sym, tf, d)

    result = run_backtest(symbol, timeframe, days)
    equity = result.get("equity_curve", [])
    if equity:
        df = pd.DataFrame(equity)
        fig = px.line(df, x=df.columns[0], y=df.columns[1], labels={df.columns[0]:"Time", df.columns[1]:"PnL"})
        st.plotly_chart(fig, use_container_width=True)
    metrics = result.get("metrics", {})
    if metrics:
        st.subheader("Metrics")
        st.table(pd.DataFrame(metrics, index=[0]).T)
    csv = result.get("csv") or result.get("csv_link")
    if csv:
        st.markdown(f"[Download CSV]({csv})")
