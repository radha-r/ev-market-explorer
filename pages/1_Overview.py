import streamlit as st

from utils.data_loader import load_data

st.title("Overview")

df = load_data()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Vehicles",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Makes",
        df["Make"].n_unique()
    )

with col3:
    st.metric(
        "Models",
        df["Model"].n_unique()
    )