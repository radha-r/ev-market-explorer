import streamlit as st


def apply_filters(df):

    st.sidebar.header("Filters")

    # ---------------------------------
    # YEAR
    # ---------------------------------

    years = sorted(
        df["Model Year"]
        .drop_nulls()
        .unique()
        .to_list(),
        reverse=True
    )

    year = st.sidebar.multiselect(
        "Year",
        options=years,
        key="year_filter"
    )

    # ---------------------------------
    # STATE
    # ---------------------------------

    states = sorted(
        df["State"]
        .drop_nulls()
        .unique()
        .to_list()
    )

    state = st.sidebar.multiselect(
        "State",
        options=states,
        key="state_filter"
    )

    # ---------------------------------
    # MAKE
    # ---------------------------------

    makes = sorted(
        df["Make"]
        .drop_nulls()
        .unique()
        .to_list()
    )

    make = st.sidebar.multiselect(
        "Make",
        options=makes,
        key="make_filter"
    )

    # ---------------------------------
    # MODEL (CASCADING)
    # ---------------------------------

    model_df = df

    if make:
        model_df = model_df.filter(
            model_df["Make"].is_in(make)
        )

    models = sorted(
        model_df["Model"]
        .drop_nulls()
        .unique()
        .to_list()
    )

    model = st.sidebar.multiselect(
        "Model",
        options=models,
        key="model_filter"
    )

    # ---------------------------------
    # APPLY FILTERS
    # ---------------------------------

    if year:
        df = df.filter(
            df["Model Year"].is_in(year)
        )

    if state:
        df = df.filter(
            df["State"].is_in(state)
        )

    if make:
        df = df.filter(
            df["Make"].is_in(make)
        )

    if model:
        df = df.filter(
            df["Model"].is_in(model)
        )

    return df