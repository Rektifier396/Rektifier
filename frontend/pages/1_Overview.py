"""Overview page showing latest trading signals."""
from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

from utils.api_client import get_client
from utils.components import confidence_bar, signal_badge, sparkline
from utils.theme import inject_theme, build_sidebar

load_dotenv()
if "theme" not in st.session_state:
    st.session_state["theme"] = "Dark"

inject_theme()
client = get_client()
build_sidebar(client)

st.title("Overview")
st.write("Monitoring day-trading metrics such as volume and RSI for selected pairs.")
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=st.session_state.get("refresh_sec", 60) * 1000, key="auto")
except Exception:
    pass


@st.cache_data(ttl=15)
def fetch_signals():
    return client.get_signals_batch()

signals = fetch_signals()
selected_symbols = set(st.session_state.get("watchlist", []))
timeframe = st.session_state.get("timeframe")

for sig in signals:
    if sig.get("symbol") not in selected_symbols or sig.get("timeframe") != timeframe:
        continue
    with st.container():
        cols = st.columns([2, 2, 2, 2])
        with cols[0]:
            st.subheader(sig.get("symbol", ""))
            signal_badge(sig.get("signal", "FLAT"))
            confidence_bar(int(sig.get("confidence", 0)))
        with cols[1]:
            risk = sig.get("risk", {})
            st.write(f"SL: {risk.get('sl')}")
            st.write(f"TP1: {risk.get('tp1')}")
            st.write(f"TP2: {risk.get('tp2')}")
            raw_ts = sig.get("generated_at")
            try:
                dt = datetime.fromisoformat(raw_ts)
                tz = timezone(timedelta(hours=7))
                formatted = dt.astimezone(tz).strftime("%Hh%M %d-%m-%Y")
            except Exception:
                formatted = raw_ts
            st.caption(f"Updated: {formatted}")
        with cols[2]:
            ind = sig.get("indicators", {})
            vol = ind.get("volume")
            rsi = ind.get("rsi")
            if vol is not None:
                st.write(f"Volume: {vol:,.0f}")
            if rsi is not None:
                st.write(f"RSI: {rsi:.2f}")
        with cols[3]:
            sparkline(sig.get("history", []))
        with st.expander("Indicators"):
            st.json(sig.get("indicators", {}))
