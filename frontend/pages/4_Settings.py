"""Settings page to update backend configuration."""
from __future__ import annotations

import time

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

st.title("Settings")

config = client.get_config()

with st.form("config"):
    watchlist = st.text_input("Watchlist (comma separated)", ",".join(config.get("watchlist", [])))
    timeframes = st.text_input("Timeframes (comma separated)", ",".join(config.get("timeframes", [])))
    rsi_overbought = st.number_input("RSI Overbought", value=config.get("rsi_overbought", 65))
    rsi_oversold = st.number_input("RSI Oversold", value=config.get("rsi_oversold", 35))
    submitted = st.form_submit_button("Save")

if submitted:
    payload = {
        "watchlist": list(dict.fromkeys(s.strip().upper() for s in watchlist.split(",") if s.strip())),
        "timeframes": [s.strip() for s in timeframes.split(",") if s.strip()],
        "rsi_overbought": rsi_overbought,
        "rsi_oversold": rsi_oversold,
    }
    try:
        client.update_config(payload)
        st.success("Configuration updated")
    except Exception as exc:
        st.error(f"Failed to update: {exc}")

if st.button("Reset Watchlist"):
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)
    try:
        client.update_config({"watchlist": []})
        st.success("Watchlist reset")
    except Exception as exc:
        st.error(f"Failed to reset: {exc}")
