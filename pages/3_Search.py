import streamlit as st

from utils.data_loader import load_data

st.title("Vehicle Search")

df = load_data()

make = st.selectbox(
    "Make",
    sorted(df["Make"].drop_nulls().unique().to_list())
)

filtered = df.filter(
    df["Make"] == make
)

st.write(
    f"Vehicles Found: {len(filtered):,}"
)

st.dataframe(
    filtered.head(100).to_pandas()
)