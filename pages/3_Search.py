import streamlit as st
import pandas as pd

from utils.data_loader import load_data

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Vehicle Search",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Vehicle Search")

# ==================================================
# LOAD DATA
# ==================================================

df = load_data()

# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("Filters")

# -----------------------------
# MAKE
# -----------------------------

makes = sorted(
    df["Make"]
    .drop_nulls()
    .unique()
    .to_list()
)

selected_make = st.sidebar.selectbox(
    "Make",
    ["All"] + makes
)

# -----------------------------
# MODEL
# -----------------------------

if selected_make == "All":

    model_source = df

else:

    model_source = df.filter(
        df["Make"] == selected_make
    )

models = sorted(
    model_source["Model"]
    .drop_nulls()
    .unique()
    .to_list()
)

selected_model = st.sidebar.selectbox(
    "Model",
    ["All"] + models
)

# -----------------------------
# YEAR
# -----------------------------

years = sorted(
    [
        int(y)
        for y in df["Model Year"]
        .drop_nulls()
        .unique()
        .to_list()
    ],
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Model Year",
    ["All"] + years
)

# -----------------------------
# COUNTY
# -----------------------------

counties = sorted(
    df["County"]
    .drop_nulls()
    .unique()
    .to_list()
)

selected_county = st.sidebar.selectbox(
    "County",
    ["All"] + counties
)

# -----------------------------
# CITY
# -----------------------------

cities = sorted(
    df["City"]
    .drop_nulls()
    .unique()
    .to_list()
)

selected_city = st.sidebar.selectbox(
    "City",
    ["All"] + cities
)

# -----------------------------
# EV TYPE
# -----------------------------

ev_types = sorted(
    df["Electric Vehicle Type"]
    .drop_nulls()
    .unique()
    .to_list()
)

selected_ev_type = st.sidebar.selectbox(
    "Vehicle Type",
    ["All"] + ev_types
)

# ==================================================
# APPLY FILTERS
# ==================================================

filtered = df

if selected_make != "All":
    filtered = filtered.filter(
        filtered["Make"] == selected_make
    )

if selected_model != "All":
    filtered = filtered.filter(
        filtered["Model"] == selected_model
    )

if selected_year != "All":
    filtered = filtered.filter(
        filtered["Model Year"] == selected_year
    )

if selected_county != "All":
    filtered = filtered.filter(
        filtered["County"] == selected_county
    )

if selected_city != "All":
    filtered = filtered.filter(
        filtered["City"] == selected_city
    )

if selected_ev_type != "All":
    filtered = filtered.filter(
        filtered["Electric Vehicle Type"]
        == selected_ev_type
    )

# ==================================================
# KPI SECTION
# ==================================================

total_records = len(filtered)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Matching Vehicles",
        f"{total_records:,}"
    )

with col2:
    st.metric(
        "Makes",
        filtered["Make"].n_unique()
    )

with col3:
    st.metric(
        "Models",
        filtered["Model"].n_unique()
    )

with col4:
    st.metric(
        "Cities",
        filtered["City"].n_unique()
    )

# ==================================================
# DISPLAY DATA
# ==================================================

display_df = filtered.select([
    "Model Year",
    "Make",
    "Model",
    "Electric Vehicle Type",
    "Electric Range",
    "City",
    "County",
    "State",
    "Postal Code"
])

full_download_df = display_df.to_pandas()

# ==================================================
# DOWNLOAD BUTTON
# ==================================================

download_csv = full_download_df.to_csv(index=False)

download_col, empty_col = st.columns([1, 5])

with download_col:
    st.download_button(
        "📥 Download CSV",
        download_csv,
        file_name="vehicle_search_results.csv",
        mime="text/csv"
    )

# ==================================================
# SUMMARY
# ==================================================

if total_records > 0:

    top_city = (
        filtered
        .group_by("City")
        .len()
        .sort("len", descending=True)
        .row(0)[0]
    )

    st.info(
        f"""
        Found **{total_records:,}** matching vehicles.

        Most represented city: **{top_city}**
        """
    )

# ==================================================
# RESULTS TABLE
# ==================================================

MAX_ROWS = 1000

table_df = (
    display_df
    .head(MAX_ROWS)
    .to_pandas()
)

st.subheader("Search Results")

st.caption(
    f"Showing first {min(MAX_ROWS, total_records):,} rows "
    f"of {total_records:,} matching records."
)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
    height=750
)

# ==================================================
# NO RESULTS
# ==================================================

if total_records == 0:
    st.warning(
        "No records found for the selected filters."
    )