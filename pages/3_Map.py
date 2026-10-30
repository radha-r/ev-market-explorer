import streamlit as st

from utils.data_loader import load_data
from utils.filters import apply_filters

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
# APPLY SHARED FILTERS
# ==================================================

df = apply_filters(df)

# ==================================================
# VERIFY COORDINATES
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

        Run:

        uv run python scripts/preprocess.py
        """
    )

    st.stop()

# ==================================================
# REMOVE NULL COORDINATES
# ==================================================

df = df.filter(
    df["Latitude"].is_not_null()
)

df = df.filter(
    df["Longitude"].is_not_null()
)

# ==================================================
# KPIs
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Vehicles",
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

with col4:
    st.metric(
        "Cities",
        df["City"].n_unique()
    )

# ==================================================
# MAP DATA
# ==================================================

MAX_POINTS = 50000

if len(df) > MAX_POINTS:

    map_df = df.sample(
        n=MAX_POINTS,
        seed=42
    )

else:

    map_df = df

map_pd = map_df.select([
    "Latitude",
    "Longitude"
]).to_pandas()

# Streamlit requires lat/lon

map_pd.columns = [
    "lat",
    "lon"
]

# ==================================================
# MAP
# ==================================================

st.subheader("Vehicle Locations")

st.info(
    f"""
    Showing {len(map_pd):,} map points
    from {len(df):,} filtered vehicles.
    """
)

st.map(map_pd)

# ==================================================
# LOWER SECTION
# ==================================================

left, right = st.columns(2)

# ==================================================
# TOP CITIES
# ==================================================

with left:

    st.subheader("🏙️ Top Cities")

    top_cities = (
        df
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
        height=450
    )

# ==================================================
# TOP MAKES
# ==================================================

with right:

    st.subheader("🚗 Top Makes")

    top_makes = (
        df
        .group_by("Make")
        .len()
        .sort("len", descending=True)
        .head(25)
        .to_pandas()
    )

    st.dataframe(
        top_makes,
        use_container_width=True,
        hide_index=True,
        height=450
    )