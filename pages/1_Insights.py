import polars as pl
import plotly.express as px
import streamlit as st

from utils.data_loader import load_data
from utils.filters import apply_filters
import polars as pl
import plotly.express as px
import streamlit as st

from utils.data_loader import load_data
from utils.filters import apply_filters

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="EV Market Insights",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ EV Market Insights")

st.markdown("""
Explore EV adoption trends, market share,
vehicle technology, utility distribution,
and geographic intelligence.
""")

# ==================================================
# LOAD DATA
# ==================================================

df = load_data()

df = apply_filters(df)

if len(df) == 0:
    st.warning(
        "No records match the selected filters."
    )
    st.stop()

# ==================================================
# KPI CALCULATIONS
# ==================================================

total_vehicles = len(df)

unique_makes = df["Make"].n_unique()

unique_models = df["Model"].n_unique()

unique_cities = df["City"].n_unique()

unique_counties = df["County"].n_unique()

avg_range_value = (
    df["Electric Range"]
    .fill_null(0)
    .mean()
)

avg_range = (
    round(avg_range_value, 1)
    if avg_range_value is not None
    else 0
)

top_make = (
    df.group_by("Make")
    .len()
    .sort("len", descending=True)
    .row(0)
)

top_model = (
    df.group_by("Model")
    .len()
    .sort("len", descending=True)
    .row(0)
)

bev_count = len(
    df.filter(
        pl.col("Electric Vehicle Type")
        .str.contains("Battery")
    )
)

bev_pct = round(
    (bev_count / total_vehicles) * 100,
    1
)

# ==================================================
# KPI ROW
# ==================================================

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Vehicles",
    f"{total_vehicles:,}"
)

c2.metric(
    "Top Make",
    top_make[0]
)

c3.metric(
    "Top Model",
    top_model[0]
)

c4.metric(
    "Avg Range",
    f"{avg_range}"
)

c5.metric(
    "Cities",
    unique_cities
)

c6.metric(
    "BEV %",
    f"{bev_pct}%"
)

st.divider()

# ==================================================
# TOP MAKES
# ==================================================

top_makes = (
    df.group_by("Make")
    .len()
    .sort("len", descending=True)
    .head(15)
)

# ==================================================
# TOP MODELS
# ==================================================

top_models = (
    df.group_by("Model")
    .len()
    .sort("len", descending=True)
    .head(15)
)

# ==================================================
# TREND
# ==================================================

year_trend = (
    df.group_by("Model Year")
    .len()
    .sort("Model Year")
)

# ==================================================
# CITY HEATMAP DATA
# ==================================================

city_heatmap = (
    df.group_by(["City", "County"])
    .len()
    .sort("len", descending=True)
    .head(50)
)

# ==================================================
# EV TYPES
# ==================================================

ev_types = (
    df.group_by("Electric Vehicle Type")
    .len()
)

# ==================================================
# TOP CITIES
# ==================================================

top_cities = (
    df.group_by("City")
    .len()
    .sort("len", descending=True)
    .head(20)
)

# ==================================================
# TOP COUNTIES
# ==================================================

top_counties = (
    df.group_by("County")
    .len()
    .sort("len", descending=True)
    .head(20)
)

# ==================================================
# TOP ZIPS
# ==================================================

top_zips = (
    df.group_by("Postal Code")
    .len()
    .sort("len", descending=True)
    .head(20)
)

# ==================================================
# UTILITIES
# ==================================================

utility_stats = (
    df.group_by("Electric Utility")
    .len()
    .sort("len", descending=True)
    .head(15)
)

# ==================================================
# CAFV
# ==================================================

cafv_stats = (
    df.group_by(
        "Clean Alternative Fuel Vehicle (CAFV) Eligibility"
    )
    .len()
)

# ==================================================
# RANGE BY MAKE
# ==================================================

range_by_make = (
    df.group_by("Make")
    .agg(
        pl.col("Electric Range")
        .mean()
        .alias("avg_range")
    )
    .sort("avg_range", descending=True)
    .head(15)
)

# ==================================================
# TOP MAKES / MODELS
# ==================================================

left, right = st.columns(2)

with left:

    fig = px.bar(
        top_makes.to_pandas(),
        x="Make",
        y="len",
        color="len",
        title="Top Manufacturers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.bar(
        top_models.to_pandas(),
        x="Model",
        y="len",
        color="len",
        title="Top Models"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# MARKET SHARE / EV TYPES
# ==================================================

left, right = st.columns(2)

with left:

    fig = px.treemap(
        top_makes.to_pandas(),
        path=["Make"],
        values="len",
        title="Market Share Treemap"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.pie(
        ev_types.to_pandas(),
        names="Electric Vehicle Type",
        values="len",
        title="BEV vs PHEV"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# TRENDS
# ==================================================

left, right = st.columns(2)

with left:

    fig = px.line(
        year_trend.to_pandas(),
        x="Model Year",
        y="len",
        markers=True,
        title="Registration Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    city_heatmap_pd = (
        df.group_by(["City", "County"])
        .len()
        .sort("len", descending=True)
        .head(10)
    )

    fig = px.scatter(
        city_heatmap_pd,
        x="len",
        y="City",
        size="len",
        color="len",
        hover_data=["County"],
        title="Top 10 Cities by EV Registrations",
        color_continuous_scale="Viridis",
        size_max=60
    )

    fig.update_layout(
        height=500,
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# ==================================================
# GEOGRAPHY
# ==================================================

st.subheader("🌎 Geographic Intelligence")

c1, c2, c3 = st.columns(3)

with c1:
    st.dataframe(
        top_cities.to_pandas(),
        use_container_width=True,
        hide_index=True,
        height=350
    )

with c2:
    st.dataframe(
        top_counties.to_pandas(),
        use_container_width=True,
        hide_index=True,
        height=350
    )

with c3:
    st.dataframe(
        top_zips.to_pandas(),
        use_container_width=True,
        hide_index=True,
        height=350
    )

# ==================================================
# INFRASTRUCTURE
# ==================================================

left, right = st.columns(2)

with left:

    fig = px.bar(
        utility_stats.to_pandas(),
        x="len",
        y="Electric Utility",
        orientation="h",
        title="Top Utilities"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.pie(
        cafv_stats.to_pandas(),
        values="len",
        names="Clean Alternative Fuel Vehicle (CAFV) Eligibility",
        title="CAFV Eligibility"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# ANALYST COMMENTARY
# ==================================================

top_city = top_cities.row(0)[0]
top_county = top_counties.row(0)[0]

st.subheader("📈 Automated Insights")

st.success(
    f"""
• {top_make[0]} is the leading EV manufacturer.

• {top_model[0]} is the most registered model.

• Battery EVs represent {bev_pct}% of registrations.

• Average vehicle range is {avg_range} miles.

• {top_city} is the leading EV city.

• {top_county} is the leading EV county.

• Data spans {unique_cities} cities and {unique_counties} counties.
"""
)