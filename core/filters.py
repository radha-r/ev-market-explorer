import polars as pl
import streamlit as st
from core.logger import log_filter_change

def apply_filters(df):

    st.sidebar.header("Filters")
    # =================================
    # YEAR
    # =================================

    years = sorted(
        df["Model Year"]
        .drop_nulls()
        .unique()
        .to_list(),
        reverse=True
    )

    selected_years = st.sidebar.multiselect(
        "Year",
        options=years
    )

    # =================================
    # STATE
    # =================================

    states = sorted(
        df["State"]
        .drop_nulls()
        .unique()
        .to_list()
    )

    selected_states = st.sidebar.multiselect(
        "State",
        options=states
    )

    # =================================
    # COUNTY
    # =================================

    counties = sorted(
        df["County"]
        .drop_nulls()
        .unique()
        .to_list()
    )

    selected_counties = st.sidebar.multiselect(
        "County",
        options=counties
    )

    # =================================
    # CITY (ONLY CASCADE FROM COUNTY)
    # =================================

    city_df = df

    if selected_counties:

        city_df = city_df.filter(
            pl.col("County").is_in(
                selected_counties
            )
        )

    cities = sorted(
        city_df["City"]
        .drop_nulls()
        .unique()
        .to_list()
    )

    selected_cities = st.sidebar.multiselect(
        "City",
        options=cities
    )

    # =================================
    # MAKE
    # =================================

    makes = sorted(
        df["Make"]
        .drop_nulls()
        .unique()
        .to_list()
    )

    selected_makes = st.sidebar.multiselect(
        "Make",
        options=makes
    )

    # =================================
    # MODEL (ONLY CASCADE FROM MAKE)
    # =================================

    model_df = df

    if selected_makes:

        model_df = model_df.filter(
            pl.col("Make").is_in(
                selected_makes
            )
        )

    models = sorted(
        model_df["Model"]
        .drop_nulls()
        .unique()
        .to_list()
    )

    selected_models = st.sidebar.multiselect(
        "Model",
        options=models
    )

    # =================================
    # APPLY FILTERS
    # =================================

    if selected_years:

        df = df.filter(
            pl.col("Model Year")
            .is_in(selected_years)
        )

    if selected_states:

        df = df.filter(
            pl.col("State")
            .is_in(selected_states)
        )

    if selected_counties:

        df = df.filter(
            pl.col("County")
            .is_in(selected_counties)
        )

    if selected_cities:

        df = df.filter(
            pl.col("City")
            .is_in(selected_cities)
        )

    if selected_makes:

        df = df.filter(
            pl.col("Make")
            .is_in(selected_makes)
        )

    if selected_models:

        df = df.filter(
            pl.col("Model")
            .is_in(selected_models)
        )

    # =================================
    # STATUS
    # =================================

    st.sidebar.divider()

    st.sidebar.caption(
        f"{len(df):,} matching vehicles"
    )

    log_filter_change(
    {
        "year": selected_years,
        "state": selected_states,
        "county": selected_counties,
        "city": selected_cities,
        "make": selected_makes,
        "model": selected_models,
    }
    )
    return df