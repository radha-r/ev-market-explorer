import streamlit as st

st.set_page_config(
    page_title="EV Market Explorer",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ EV Market Explorer")

st.info(
    """
    Data Source: "Electric Vehicle Population data" from State of Washington. 
    
    This dataset shows the Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) that are currently registered through Washington State Department of Licensing (DOL).

    Use the navigation menu on the left.

    👉 Insights

    👉 Search

    👉 Map
    """
)