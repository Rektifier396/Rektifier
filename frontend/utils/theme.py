"""Theme utilities and layout helpers for the Streamlit dashboard."""
from __future__ import annotations

import os
from pathlib import Path

import streamlit as st


def inject_theme() -> None:
    """Load CSS and apply light/dark theme based on session state."""
    st.set_page_config(page_title="Crypto Signal Dashboard", layout="wide")
    theme = st.session_state.get("theme", "Dark").lower()
    css_path = Path(__file__).resolve().parent.parent / "assets" / "styles.css"
    base_css = css_path.read_text()
    if theme == "light":
        colors = """
        body {background-color: #ffffff; color: #000000;}
        .card {background-color: #f3f4f6; color: #000000;}
        .badge {background-color: #2563eb;}
        .progress {background-color: #e5e7eb;}
        """
    else:
        colors = """
        body {background-color: #0e1117; color: #ffffff;}
        .card {background-color: #1f2937; color: #ffffff;}
        .badge {background-color: #374151;}
        .progress {background-color: #4b5563;}
        """
    st.markdown(f"<style>{base_css}\n{colors}</style>", unsafe_allow_html=True)


def build_sidebar(client) -> None:
    """Render common sidebar controls and navigation."""
    config = client.get_config()
    watchlist = list(dict.fromkeys(config.get("watchlist", [])))
    timeframes = config.get("timeframes", [])
    st.session_state["theme"] = st.sidebar.selectbox(
        "Theme", ["Dark", "Light"],
        index=0 if st.session_state.get("theme", "Dark") == "Dark" else 1,
    )
    st.sidebar.multiselect("Watchlist", options=watchlist, default=watchlist, key="watchlist")
    st.sidebar.selectbox("Timeframe", options=timeframes, index=0, key="timeframe")
    st.sidebar.number_input(
        "Refresh (sec)", min_value=10, max_value=3600,
        value=int(os.getenv("REFRESH_SEC", "60")), key="refresh_sec",
    )
    if st.sidebar.button("Refresh Now"):
        st.experimental_rerun()

    st.sidebar.page_link("pages/1_Overview.py", label="Overview")
    st.sidebar.page_link("pages/2_Daily_Stats.py", label="Daily Stats")
    st.sidebar.page_link("pages/3_Backtest.py", label="Backtest")
    st.sidebar.page_link("pages/4_Settings.py", label="Settings")

    st.sidebar.markdown(f"[API Docs]({client.base_url}/docs)")

    try:
        healthy = client.health().get("status") == "ok"
    except Exception:
        healthy = False
    st.sidebar.markdown(f"**Health:** {'🟢' if healthy else '🔴'}")
