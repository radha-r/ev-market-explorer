import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.filters import apply_filters

st.set_page_config(layout="wide")

#st.title("📊 EV Market Analytics")
st.markdown("""
<div style="
    background: linear-gradient(90deg,#0f172a,#1e40af);
    padding:30px;
    border-radius:15px;
    color:white;
    margin-bottom:20px;
">
    <h1>⚡ EV Market Explorer</h1>
    <p>
        Explore electric vehicle registrations, market share,
        adoption trends, and geographic insights across the United States.
    </p>
</div>
""", unsafe_allow_html=True)

df = load_data()
df = apply_filters(df)

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_vehicles = len(df)

unique_makes = df["Make"].n_unique()

unique_models = df["Model"].n_unique()

unique_cities = df["City"].n_unique()

avg_range = round(
    df["Electric Range"].fill_null(0).mean(),
    1
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

# --------------------------------------------------
# KPI ROW
# --------------------------------------------------

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "EV Registrations",
    f"{total_vehicles:,}"
)

c2.metric(
    "Makes",
    unique_makes
)

c3.metric(
    "Models",
    unique_models
)

c4.metric(
    "Cities",
    unique_cities
)

c5.metric(
    "Top Make",
    top_make[0]
)

c6.metric(
    "Avg Range",
    f"{avg_range} mi"
)

st.divider()

# --------------------------------------------------
# TOP MAKES
# --------------------------------------------------

top_makes = (
    df.group_by("Make")
    .len()
    .sort("len", descending=True)
    .head(10)
)

# --------------------------------------------------
# TOP MODELS
# --------------------------------------------------

top_models = (
    df.group_by("Model")
    .len()
    .sort("len", descending=True)
    .head(10)
)

# --------------------------------------------------
# TOP CITIES
# --------------------------------------------------

top_cities = (
    df.group_by("City")
    .len()
    .sort("len", descending=True)
    .head(10)
)

# --------------------------------------------------
# TOP COUNTIES
# --------------------------------------------------

top_counties = (
    df.group_by("County")
    .len()
    .sort("len", descending=True)
    .head(10)
)

top_zipcodes = (
    df.group_by("Postal Code")
    .len()
    .sort("len", descending=True)
    .head(15)
)

utility_stats = (
    df.group_by("Electric Utility")
    .len()
    .sort("len", descending=True)
    .head(10)
)

# --------------------------------------------------
# MODEL YEAR TREND
# --------------------------------------------------

year_trend = (
    df.group_by("Model Year")
    .len()
    .sort("Model Year")
)

cafv_stats = (
    df.group_by(
        "Clean Alternative Fuel Vehicle (CAFV) Eligibility"
    )
    .len()
)

# --------------------------------------------------
# EV TYPES
# --------------------------------------------------

ev_types = (
    df.group_by("Electric Vehicle Type")
    .len()
)

# --------------------------------------------------
# ROW 1
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        top_makes.to_pandas(),
        x="Make",
        y="len",
        color="len",
        title="Top 10 EV Manufacturers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.bar(
        top_models.to_pandas(),
        x="Model",
        y="len",
        color="len",
        title="Top 10 EV Models"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# ROW 2
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.line(
        year_trend.to_pandas(),
        x="Model Year",
        y="len",
        markers=True,
        title="Registrations by Model Year"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

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

# --------------------------------------------------
# ROW 3
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

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

with col2:

    fig = px.bar(
        top_cities.to_pandas(),
        x="City",
        y="len",
        color="len",
        title="Top Cities by Registrations"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("🏆 County Rankings")
st.subheader("⚡ Utility Service Territories")

fig = px.bar(
    utility_stats.to_pandas(),
    x="len",
    y="Electric Utility",
    orientation="h",
    title="EV Registrations by Utility"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("✅ CAFV Eligibility")

fig = px.pie(
    cafv_stats.to_pandas(),
    names="Clean Alternative Fuel Vehicle (CAFV) Eligibility",
    values="len",
    title="CAFV Eligibility Breakdown"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

fig = px.bar(
    top_counties.to_pandas(),
    x="County",
    y="len",
    color="len",
    title="Top Counties by EV Registrations"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📮 Top ZIP Codes")

fig = px.bar(
    top_zipcodes.to_pandas(),
    x="Postal Code",
    y="len",
    color="len",
    title="Top EV ZIP Codes"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.subheader("🔍 Quick Insights")

left, right = st.columns(2)

with left:

    st.info(
        f"""
        **Market Leader:** {top_make[0]}

        Most common EV model:
        **{top_model[0]}**
        """
    )

with right:

    st.success(
        f"""
        Dataset contains
        **{total_vehicles:,} EV registrations**
        spanning
        **{unique_cities} cities**.
        """
    )