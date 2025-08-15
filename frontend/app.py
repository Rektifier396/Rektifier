"""Streamlit entrypoint for the crypto signal dashboard."""
from __future__ import annotations

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

st.title("Crypto Signal Dashboard")
st.write("Use the sidebar to navigate between pages.")
