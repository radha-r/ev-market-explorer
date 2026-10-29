import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

st.title("Analytics")

df = load_data()

top_makes = (
    df.group_by("Make")
      .len()
      .sort("len", descending=True)
      .head(10)
)

fig = px.bar(
    top_makes.to_pandas(),
    x="Make",
    y="len",
    title="Top EV Makes"
)

st.plotly_chart(
    fig,
    use_container_width=True
)