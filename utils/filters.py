import streamlit as st


def apply_filters(df):

    states = sorted(
        df["State"].drop_nulls().unique().to_list()
    )

    state = st.sidebar.multiselect(
        "State",
        states
    )

    makes = sorted(
        df["Make"].drop_nulls().unique().to_list()
    )

    make = st.sidebar.multiselect(
        "Make",
        makes
    )

    if state:
        df = df.filter(df["State"].is_in(state))

    if make:
        df = df.filter(df["Make"].is_in(make))

    return df