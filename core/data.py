"""
Centralized data access layer.

Provides:

- dataset loading
- schema inspection
- dataset metadata
- validation helpers

All application pages should access data
through this module.
"""

import polars as pl
import streamlit as st

from config import PARQUET_PATH


@st.cache_data(show_spinner=False)
def load_data() -> pl.DataFrame:
    """
    Load the processed EV dataset.
    """

    if not PARQUET_PATH.exists():

        raise FileNotFoundError(
            f"Dataset not found:\n"
            f"{PARQUET_PATH}"
        )

    return pl.read_parquet(PARQUET_PATH)


# ==================================================
# SCHEMA
# ==================================================

def schema(df: pl.DataFrame):

    return df.schema


def columns(df: pl.DataFrame):

    return df.columns


def show_schema(df: pl.DataFrame):

    schema_df = pl.DataFrame({
        "Column": list(df.schema.keys()),
        "Type": [
            str(dtype)
            for dtype in df.schema.values()
        ]
    })

    st.dataframe(
        schema_df.to_pandas(),
        width="stretch",
        hide_index=True
    )


# ==================================================
# VALIDATION
# ==================================================

def column_exists(
    df: pl.DataFrame,
    column_name: str
):

    return column_name in df.columns


def require_columns(
    df: pl.DataFrame,
    *required_columns
):

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            "Missing required columns:\n"
            + "\n".join(missing)
        )


# ==================================================
# DATASET INFO
# ==================================================

def row_count(df: pl.DataFrame):

    return len(df)


def column_count(df: pl.DataFrame):

    return len(df.columns)


def dataset_info(df: pl.DataFrame):

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "schema": df.schema,
    }


def show_dataset_info(df: pl.DataFrame):

    c1, c2 = st.columns(2)

    c1.metric(
        "Rows",
        f"{len(df):,}"
    )

    c2.metric(
        "Columns",
        len(df.columns)
    )


# ==================================================
# VALUES
# ==================================================

def unique_values(
    df: pl.DataFrame,
    column: str,
    limit: int | None = None
):

    values = (
        df[column]
        .drop_nulls()
        .unique()
        .sort()
    )

    if limit is not None:

        values = values.head(limit)

    return values.to_list()