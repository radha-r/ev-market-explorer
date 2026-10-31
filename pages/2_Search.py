import streamlit as st
from core.data import load_data
from core.footer import show_footer

st.title("🚗 Vehicle Search")

# ==================================================
# LOAD DATA
# ==================================================

df = load_data()

# ==================================================
# FILTERS
# ==================================================

st.sidebar.header("Search")

# MAKE

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

# MODEL (CASCADE)

model_df = df

if selected_make != "All":

    model_df = model_df.filter(
        model_df["Make"] == selected_make
    )

models = sorted(
    model_df["Model"]
    .drop_nulls()
    .unique()
    .to_list()
)

selected_model = st.sidebar.selectbox(
    "Model",
    ["All"] + models
)

# YEAR

years = sorted(
    df["Model Year"]
    .drop_nulls()
    .unique()
    .to_list(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Model Year",
    ["All"] + years
)

# COUNTY

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

# CITY

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

# VEHICLE TYPE

vehicle_types = sorted(
    df["Clean Alternative Fuel Vehicle Type"]
    .drop_nulls()
    .unique()
    .to_list()
)

selected_type = st.sidebar.selectbox(
    "Vehicle Type",
    ["All"] + vehicle_types
)

# NEW / USED

usage_types = sorted(
    df["New or Used Vehicle"]
    .drop_nulls()
    .unique()
    .to_list()
)

selected_usage = st.sidebar.selectbox(
    "Condition",
    ["All"] + usage_types
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

if selected_type != "All":

    filtered = filtered.filter(
        filtered[
            "Clean Alternative Fuel Vehicle Type"
        ]
        == selected_type
    )

if selected_usage != "All":

    filtered = filtered.filter(
        filtered["New or Used Vehicle"]
        == selected_usage
    )

# ==================================================
# KPI ROW
# ==================================================

total_records = len(filtered)


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Vehicles",
    f"{total_records:,}"
)

col2.metric(
    "Makes",
    filtered["Make"].n_unique()
)

col3.metric(
    "Models",
    filtered["Model"].n_unique()
)

col4.metric(
    "Cities",
    filtered["City"].n_unique()
)


# ==================================================
# DISPLAY DATASET
# ==================================================

display_df = filtered.select([
    "Model Year",
    "Make",
    "Model",
    "New or Used Vehicle",
    "Odometer Reading",
    "Sale Price",
    "Electric Range",
    "City",
    "County",
    "State",
    "Postal Code",
    "Transaction Type",
    "Transaction Date",
])

with col5:
    download_df = display_df.to_pandas()
    csv = download_df.to_csv(index=False)

    st.download_button(
        "📥 Download",
        csv,
        file_name="vehicle_search_results.csv",
        mime="text/csv"
    )

# ==================================================
# SUMMARY
# ==================================================

# if total_records > 0:

#     top_city = (
#         filtered
#         .group_by("City")
#         .len()
#         .sort("len", descending=True)
#         .row(0)[0]
#     )

#     st.info(
#         f"""
#         {top_city} has more vehicles.
#         """
#     )

# ==================================================
# TABLE
# ==================================================

MAX_ROWS = 1000

table_df = (
    display_df
    .head(MAX_ROWS)
    .to_pandas()
)

#st.subheader("Search Results")

st.caption(
    f"Showing first {min(MAX_ROWS, total_records):,} rows "
    f"of {total_records:,} matching vehicles."
)

st.dataframe(
    table_df,
    width="stretch",
    hide_index=True,
    height=800
)

# ==================================================
# NO RESULTS
# ==================================================

if total_records == 0:

    st.warning(
        "No matching records found."
    )


# ==================================================
# FOOTER
# ==================================================

show_footer()