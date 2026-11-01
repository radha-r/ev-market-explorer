import polars as pl
import plotly.express as px
import streamlit as st
from core.data import dataset_metadata, load_data, show_metadata
from core.filters import apply_filters
from core.footer import show_footer

# ==================================================
# LOAD
# ==================================================

st.title("⚡ EV Market Intelligence")
show_metadata()

df = load_data()
df = apply_filters(df)

if len(df) == 0:
    st.warning("No records match filters.")
    st.stop()

# ==================================================
# KPI CALCULATIONS
# ==================================================

total_vehicles = len(df)

unique_makes = df["Make"].n_unique()
unique_models = df["Model"].n_unique()
unique_cities = df["City"].n_unique()

price_df = df.filter(
    pl.col("Sale Price") > 0
)

avg_price = (
    round(price_df["Sale Price"].mean(), 0)
    if len(price_df) > 0
    else 0
)

median_price = (
    round(price_df["Sale Price"].median(), 0)
    if len(price_df) > 0
    else 0
)

top_make = (
    df.group_by("Make")
    .len()
    .sort("len", descending=True)
    .row(0)[0]
)

top_model = (
    df.group_by("Model")
    .len()
    .sort("len", descending=True)
    .row(0)[0]
)

# ==================================================
# KPI ROW 1
# ==================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Vehicles",
    f"{total_vehicles:,}"
)

c2.metric(
    "Manufacturers",
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

# ==================================================
# KPI ROW 2
# ==================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Median Price",
    f"${median_price:,.0f}"
)

c2.metric(
    "Average Price",
    f"${avg_price:,.0f}"
)

c3.metric(
    "Top Make",
    top_make
)

c4.metric(
    "Top Model",
    top_model
)

st.divider()

# ==================================================
# TOP MAKES
# ==================================================

top_makes = (
    df.group_by("Make")
    .len()
    .rename({"len": "Vehicles"})
    .sort("Vehicles", descending=True)
    .head(15)
)

# ==================================================
# TOP MODELS
# ==================================================

top_models = (
    df.group_by("Model")
    .len()
    .rename({"len": "Vehicles"})
    .sort("Vehicles", descending=True)
    .head(15)
)

left, right = st.columns(2)

with left:

    fig = px.bar(
        top_makes.to_pandas(),
        x="Make",
        y="Vehicles",
        color="Vehicles",
        text="Vehicles",
        title="Top Manufacturers"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    fig = px.bar(
        top_models.to_pandas(),
        x="Model",
        y="Vehicles",
        color="Vehicles",
        text="Vehicles",
        title="Top Models"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ==================================================
# MARKET SHARE + PRICE HISTOGRAM
# ==================================================

left, right = st.columns(2)

with left:

    fig = px.treemap(
        top_makes.to_pandas(),
        path=["Make"],
        values="Vehicles",
        title="Market Share"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    fig = px.histogram(
        price_df.to_pandas(),
        x="Sale Price",
        nbins=40,
        title="Price Distribution"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ==================================================
# SEASONALITY HEATMAP
# ==================================================

st.subheader(
    "📅 Vehicle Registrations by Month and Year"
)

seasonality = (
    df.group_by(
        [
            "Transaction Month Name",
            "Transaction Year"
        ]
    )
    .len()
    .rename({"len": "Vehicles"})
)

heatmap_pd = (
    seasonality
    .to_pandas()
    .pivot(
        index="Transaction Month Name",
        columns="Transaction Year",
        values="Vehicles"
    )
)

heatmap_pd = heatmap_pd.reindex(
    [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
)

fig = px.imshow(
    heatmap_pd,
    aspect="auto",
    color_continuous_scale="Viridis",
    title="Seasonality Heatmap"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ==================================================
# TRANSACTIONS
# ==================================================

txn_type = (
    df.group_by(
        "Transaction Type"
    )
    .len()
    .rename({"len": "Vehicles"})
)

new_used = (
    df.group_by(
        "New or Used Vehicle"
    )
    .len()
    .rename({"len": "Vehicles"})
)

left, right = st.columns(2)

with left:

    fig = px.pie(
        txn_type.to_pandas(),
        names="Transaction Type",
        values="Vehicles",
        title="Transaction Type"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    fig = px.pie(
        new_used.to_pandas(),
        names="New or Used Vehicle",
        values="Vehicles",
        title="New vs Used"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ==================================================
# PRICE BY MAKE
# ==================================================

price_make = (
    price_df.group_by("Make")
    .agg(
        pl.col("Sale Price")
        .median()
        .alias("Median Price")
    )
    .sort(
        "Median Price",
        descending=True
    )
    .head(15)
)

fig = px.bar(
    price_make.to_pandas(),
    x="Make",
    y="Median Price",
    color="Median Price",
    text="Median Price",
    title="Median Sale Price by Make"
)

fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ==================================================
# TOP CITIES
# ==================================================

city_stats = (
    df.group_by(
        ["City", "County"]
    )
    .len()
    .rename({"len": "Vehicles"})
    .sort(
        "Vehicles",
        descending=True
    )
    .head(10)
)

districts = (
    df.group_by(
        "Legislative District"
    )
    .len()
    .rename({"len": "Vehicles"})
    .sort(
        "Vehicles",
        descending=True
    )
    .head(15)
)

left, right = st.columns(2)

with left:

    fig = px.scatter(
        city_stats.to_pandas(),
        x="Vehicles",
        y="City",
        size="Vehicles",
        color="Vehicles",
        hover_data=["County"],
        title="Top 10 Cities"
    )

    fig.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    fig = px.bar(
        districts.to_pandas(),
        x="Legislative District",
        y="Vehicles",
        color="Vehicles",
        text="Vehicles",
        title="Top Legislative Districts"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ==================================================
# UTILITIES
# ==================================================

utility_stats = (
    df.group_by(
        "Electric Utility"
    )
    .len()
    .rename({"len": "Vehicles"})
    .sort(
        "Vehicles",
        descending=True
    )
    .head(15)
)

fig = px.bar(
    utility_stats.to_pandas(),
    x="Vehicles",
    y="Electric Utility",
    orientation="h",
    text="Vehicles",
    color="Vehicles",
    title="Top Utilities"
)

fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ==================================================
# COUNTIES + ZIPS
# ==================================================

left, right = st.columns(2)

top_counties = (
    df.group_by("County")
    .len()
    .rename({"len": "Vehicles"})
    .sort(
        "Vehicles",
        descending=True
    )
    .head(20)
)

top_zips = (
    df.group_by("Postal Code")
    .len()
    .rename({"len": "Vehicles"})
    .sort(
        "Vehicles",
        descending=True
    )
    .head(20)
)

with left:

    st.subheader(
        "Top Counties"
    )

    st.dataframe(
        top_counties.to_pandas(),
        width="stretch",
        hide_index=True,
        height=400
    )

with right:

    st.subheader(
        "Top ZIP Codes"
    )

    st.dataframe(
        top_zips.to_pandas(),
        width="stretch",
        hide_index=True,
        height=400
    )

# ==================================================
# ODOMETER
# ==================================================

st.subheader(
    "🚘 Odometer Distribution"
)

odometer_df = (
    df.filter(
        pl.col(
            "Odometer Reading"
        ).is_not_null()
    )
)

fig = px.histogram(
    odometer_df.to_pandas(),
    x="Odometer Reading",
    nbins=50,
    title="Mileage Distribution"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ==================================================
# EXECUTIVE SUMMARY
# ==================================================

top_city = (
    df.group_by("City")
    .len()
    .sort(
        "len",
        descending=True
    )
    .row(0)[0]
)

st.subheader(
    "📈 Executive Summary"
)

st.success(
    f"""
• {top_make} is the leading EV manufacturer.

• {top_model} is the most registered model.

• {top_city} is the leading EV market.

• Median transaction price is ${median_price:,.0f}.

• Dataset contains {total_vehicles:,} vehicle transactions.

• Covers {unique_cities:,} cities.

• Includes new and used vehicle registrations and transfer activity.
"""
)

# ==================================================
# FOOTER
# ==================================================

show_footer()