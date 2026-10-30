import streamlit as st

from utils.data_loader import load_data

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="EV Map",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ EV Registration Map")

# ==================================================
# LOAD DATA
# ==================================================

df = load_data()

# ==================================================
# VERIFY REQUIRED COLUMNS
# ==================================================

required_columns = [
    "Latitude",
    "Longitude"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"""
        Missing columns:
        {', '.join(missing_columns)}

        Re-run:

        uv run python scripts/preprocess.py
        """
    )

    st.stop()

# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("Map Filters")

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

# ==================================================
# APPLY FILTERS
# ==================================================

filtered = df

if selected_make != "All":
    filtered = filtered.filter(
        filtered["Make"] == selected_make
    )

if selected_county != "All":
    filtered = filtered.filter(
        filtered["County"] == selected_county
    )

if selected_city != "All":
    filtered = filtered.filter(
        filtered["City"] == selected_city
    )

# ==================================================
# REMOVE BAD COORDINATES
# ==================================================

filtered = filtered.filter(
    filtered["Latitude"].is_not_null()
)

filtered = filtered.filter(
    filtered["Longitude"].is_not_null()
)

# ==================================================
# KPI ROW
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Vehicles",
        f"{len(filtered):,}"
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
# MAP DATA
# ==================================================

MAX_POINTS = 50000

if len(filtered) > MAX_POINTS:

    map_df = filtered.sample(
        n=MAX_POINTS,
        seed=42
    )

else:

    map_df = filtered

map_pd = map_df.select([
    "Latitude",
    "Longitude"
]).to_pandas()

# Streamlit expects lat/lon names

map_pd.columns = [
    "lat",
    "lon"
]

# ==================================================
# MAP
# ==================================================

st.subheader("Vehicle Locations")

st.info(
    f"Displaying {len(map_pd):,} vehicle locations."
)

st.write(
    f"Filtered records: {len(filtered):,}"
)
st.map(map_pd)

# ==================================================
# TOP CITIES
# ==================================================

st.subheader("🏙️ Top Cities")

top_cities = (
    filtered
    .group_by("City")
    .len()
    .sort("len", descending=True)
    .head(25)
    .to_pandas()
)

st.dataframe(
    top_cities,
    use_container_width=True,
    hide_index=True,
    height=400
)

# ==================================================
# TOP MAKES
# ==================================================

st.subheader("🚗 Top Makes")

top_makes = (
    filtered
    .group_by("Make")
    .len()
    .sort("len", descending=True)
    .head(20)
    .to_pandas()
)

st.dataframe(
    top_makes,
    use_container_width=True,
    hide_index=True,
    height=300
)