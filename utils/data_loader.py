from pathlib import Path
import polars as pl
import streamlit as st


DATA_FILE = Path("data/processed/ev_data.parquet")


@st.cache_data
def load_data():
    return pl.read_parquet(DATA_FILE)