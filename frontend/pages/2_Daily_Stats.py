"""Daily statistics and market overview."""
from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

from utils.api_client import get_client
from utils.components import donut_chart, kpi_card
from utils.theme import inject_theme, build_sidebar

load_dotenv()
if "theme" not in st.session_state:
    st.session_state["theme"] = "Dark"

inject_theme()
client = get_client()
build_sidebar(client)

st.title("Daily Stats")

@st.cache_data(ttl=30)
def fetch_stats(day: str):
    return client.get_stats_daily(day)

stats = fetch_stats(date.today().isoformat())

cols = st.columns(4)
with cols[0]:
    top = (stats.get("top_movers") or [{}])[0]
    kpi_card("Top Mover", top.get("symbol", "-"), delta=f"{top.get('change', 0)}%")
with cols[1]:
    kpi_card("Avg % Change", f"{stats.get('avg_change', 0):.2f}%")
with cols[2]:
    kpi_card("24h Volume", f"{stats.get('volume_sum', 0):,.0f}")
with cols[3]:
    kpi_card("Signals Today", str(stats.get('signals_today', 0)))

st.subheader("Long / Short Ratio")
donut_chart({"Long": stats.get("long_signals", 0), "Short": stats.get("short_signals", 0)})

st.subheader("Fear & Greed Index")
fg = stats.get("fear_greed", {}).get("value")
if fg is not None:
    fig = go.Figure(go.Indicator(mode="gauge+number", value=float(fg), title={"text": "FGI"}, gauge={"axis": {"range": [0, 100]}}))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Fear & Greed data unavailable")

st.subheader("Top Movers")
movers = pd.DataFrame(stats.get("top_movers", []))
st.dataframe(movers, use_container_width=True)
