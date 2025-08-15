"""Reusable Streamlit components for the dashboard."""
from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

SIGNAL_COLORS = {"LONG": "#16a34a", "SHORT": "#dc2626", "FLAT": "#6b7280"}


def signal_badge(signal: str) -> None:
    """Render a colored badge for the given signal."""
    color = SIGNAL_COLORS.get(signal.upper(), SIGNAL_COLORS["FLAT"])
    st.markdown(
        f"<span style='background-color:{color}; padding:2px 8px; border-radius:4px; color:white;'>{signal}</span>",
        unsafe_allow_html=True,
    )


def confidence_bar(value: int) -> None:
    """Render a progress bar representing confidence."""
    st.progress(int(value), text=f"{value}%")


def kpi_card(title: str, value: str, delta: Optional[str] = None, help: Optional[str] = None) -> None:
    """Display a KPI card using :func:`st.metric`."""
    st.metric(title, value, delta, help=help)


def donut_chart(data: dict) -> None:
    """Render a donut chart from a mapping of labels to values."""
    labels, values = zip(*data.items()) if data else ([], [])
    fig = px.pie(names=labels, values=values, hole=0.6)
    st.plotly_chart(fig, use_container_width=True)


def sparkline(series: Iterable[float]) -> None:
    """Render a small line chart without markers."""
    if not series:
        st.empty()
        return
    df = pd.DataFrame({"y": list(series)})
    fig = px.line(df, y="y")
    fig.update_layout(showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False), margin=dict(t=0,l=0,b=0,r=0))
    st.plotly_chart(fig, use_container_width=True)
