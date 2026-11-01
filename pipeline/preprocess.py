"""
Preprocess EV transaction data.

Examples
--------

Default output:

    uv run python pipeline/preprocess.py -i 20261030_ev_data.csv -g zip_lat_long.tsv
        
Creates:

    data/processed/ev_data.parquet


Custom output:

    uv run python pipeline/preprocess.py \
        -i 20261030_ev_data.csv \
        -g zip_lat_long.tsv \
        -o ev_data_test.parquet
        --report

Creates:

    data/processed/ev_data_test.parquet
"""

import sys
import json
from datetime import datetime 
from argparse import ArgumentParser
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import polars as pl

from config import (
    RAW_DIR,
    PROCESSED_DIR,
    DEFAULT_PARQUET_FILE,
)

VALID_TRANSACTION_TYPES = [
    "Original Title",
    "Registration at time of Transfer",
]

KEEP_COLUMNS = [
    "VIN (1-10)",
    "DOL Vehicle ID",
    "Model Year",
    "Make",
    "Model",
    "Primary Use",
    "Electric Range",
    "Odometer Reading",
    "Odometer Reading Description",
    "New or Used Vehicle",
    "Sale Price",
    "Sale Date",
    "Transaction Type",
    "Transaction Date",
    "Year",
    "County",
    "City",
    "State",
    "Postal Code",
    "Legislative District",
    "Electric Utility",
    "Clean Alternative Fuel Vehicle Type",
]


def parse_args():

    parser = ArgumentParser(
        description="Generate EV Market Explorer parquet dataset"
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input CSV located in data/raw"
    )

    parser.add_argument(
        "-g",
        "--geo",
        required=True,
        help="GEO lookup file located in data/raw"
    )

    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_PARQUET_FILE,
        help=(
            "Output parquet filename. "
            "Stored automatically in data/processed."
        )
    )
    
    parser.add_argument(
        "--report",
        action="store_true",
        help="Display dataset profiling report"
    )

    return parser.parse_args()


def validate_columns(
    df: pl.DataFrame,
    required_columns: list[str],
    source_name: str,
):

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"{source_name} is missing columns:\n"
            f"  - " + "\n  - ".join(missing)
        )

def print_dataset_report(df: pl.DataFrame):

    print()
    print("=" * 100)
    print("DATASET PROFILE")
    print("=" * 100)

    print(
        f"Rows    : {len(df):,}"
    )

    print(
        f"Columns : {len(df.columns):,}"
    )

    print()

    headers = [
        "Column",
        "Type",
        "Nulls",
        "Min",
        "Max",
        "Mean",
    ]

    print(
        f"{headers[0]:30}"
        f"{headers[1]:15}"
        f"{headers[2]:>12}"
        f"{headers[3]:>15}"
        f"{headers[4]:>15}"
        f"{headers[5]:>15}"
    )

    print("-" * 102)

    numeric_types = {
        pl.Int8,
        pl.Int16,
        pl.Int32,
        pl.Int64,
        pl.UInt8,
        pl.UInt16,
        pl.UInt32,
        pl.UInt64,
        pl.Float32,
        pl.Float64,
    }

    for column, dtype in df.schema.items():

        nulls = (
            df[column]
            .is_null()
            .sum()
        )

        min_value = ""
        max_value = ""
        mean_value = ""

        if dtype in numeric_types:

            try:

                min_value = (
                    df[column]
                    .min()
                )

                max_value = (
                    df[column]
                    .max()
                )

                mean_value = round(
                    df[column]
                    .mean(),
                    2
                )

            except Exception:
                pass

        print(
            f"{column[:29]:30}"
            f"{str(dtype):15}"
            f"{nulls:12,}"
            f"{str(min_value):>15}"
            f"{str(max_value):>15}"
            f"{str(mean_value):>15}"
        )

    print("=" * 100)

def main():

    args = parse_args()

    input_file = RAW_DIR / args.input
    geo_file = RAW_DIR / args.geo

    output_file = (
        PROCESSED_DIR /
        Path(args.output).name
    )

    if not input_file.exists():

        raise FileNotFoundError(
            f"Input file not found:\n{input_file}"
        )

    if not geo_file.exists():

        raise FileNotFoundError(
            f"GEO lookup file not found:\n{geo_file}"
        )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print("=" * 60)
    print("EV DATA PREPROCESSING")
    print("=" * 60)

    # ==================================================
    # LOAD VEHICLE DATA
    # ==================================================

    print()
    print(f"Loading vehicle data: {input_file}")

    df = pl.read_csv(
        input_file,
        infer_schema_length=50000,
        ignore_errors=True,
    )

    print(f"Rows Loaded: {len(df):,}")

    # ==================================================
    # LOAD GEO LOOKUP
    # ==================================================

    print()
    print(f"Loading GEO lookup: {geo_file}")

    geo_df = pl.read_csv(
        geo_file,
        separator="|",
    )

    print(
        f"GEO Rows Loaded: {len(geo_df):,}"
    )

    # ==================================================
    # KEEP ONLY REQUIRED COLUMNS
    # ==================================================

    columns_to_keep = [
        col
        for col in KEEP_COLUMNS
        if col in df.columns
    ]

    df = df.select(columns_to_keep)

    print(
        f"Columns Retained: {len(df.columns)}"
    )

    # ==================================================
    # FILTER TRANSACTION TYPES
    # ==================================================

    if "Transaction Type" in df.columns:

        df = df.filter(
            pl.col("Transaction Type").is_in(
                VALID_TRANSACTION_TYPES
            )
        )

        print(
            f"Rows After Transaction Filter: "
            f"{len(df):,}"
        )

    # ==================================================
    # SALE PRICE
    # ==================================================

    if "Sale Price" in df.columns:

        df = df.with_columns(
            pl.col("Sale Price")
            .str.replace_all(r"[$,]", "")
            .cast(
                pl.Float64,
                strict=False
            )
        )

    # ==================================================
    # ODOMETER
    # ==================================================

    if "Odometer Reading" in df.columns:

        df = df.with_columns(
            pl.col("Odometer Reading")
            .cast(
                pl.Int64,
                strict=False
            )
        )

    # ==================================================
    # DATE CONVERSION
    # ==================================================

    if "Sale Date" in df.columns:

        df = df.with_columns(
            pl.col("Sale Date")
            .str.strptime(
                pl.Date,
                "%B %d, %Y",
                strict=False,
            )
        )

    if "Transaction Date" in df.columns:

        df = df.with_columns(
            pl.col("Transaction Date")
            .str.strptime(
                pl.Date,
                "%B %d, %Y",
                strict=False,
            )
        )

    # ==================================================
    # DATE DERIVATIVES
    # ==================================================

    if "Transaction Date" in df.columns:

        df = df.with_columns([

            pl.col("Transaction Date")
            .dt.year()
            .alias("Transaction Year"),

            pl.col("Transaction Date")
            .dt.month()
            .alias("Transaction Month"),

            pl.col("Transaction Date")
            .dt.quarter()
            .alias("Transaction Quarter"),

            pl.col("Transaction Date")
            .dt.strftime("%b")
            .alias("Transaction Month Name"),

        ])

    # ==================================================
    # GEO LOOKUP
    # ==================================================

    validate_columns(
        geo_df,
        ["GEOID", "INTPTLAT", "INTPTLONG"],
        geo_file.name,
    )

    geo_df = geo_df.with_columns([

        pl.col("GEOID")
        .cast(pl.Int64, strict=False),

        pl.col("INTPTLAT")
        .cast(pl.Float64, strict=False),

        pl.col("INTPTLONG")
        .cast(pl.Float64, strict=False),

    ])

    if "Postal Code" in df.columns:

        df = df.with_columns(
            pl.col("Postal Code")
            .cast(pl.Int64, strict=False)
        )

        df = df.join(
            geo_df.select([
                "GEOID",
                "INTPTLAT",
                "INTPTLONG",
            ]),
            left_on="Postal Code",
            right_on="GEOID",
            how="left",
        )

        df = df.rename({
            "INTPTLAT": "Latitude",
            "INTPTLONG": "Longitude",
        })

        print()
        print(
            f"Latitude populated : "
            f"{df['Latitude'].is_not_null().sum():,}"
        )

        print(
            f"Longitude populated: "
            f"{df['Longitude'].is_not_null().sum():,}"
        )

    # ==================================================
    # SUMMARY
    # ==================================================

    print()
    print("Schema:")

    for column, dtype in df.schema.items():

        print(
            f"  {column}: {dtype}"
        )

    print()
    print(
        f"Final Rows: {len(df):,}"
    )

    # ==================================================
    # WRITE PARQUET
    # ==================================================

    if args.report:
        print_dataset_report(df)

    print()
    print(f"Writing: {output_file}")

    df.write_parquet(
        output_file,
        compression="zstd"
    )

    size_mb = (
        output_file.stat().st_size
        / 1024
        / 1024
    )

    # ==================================================
    # WRITE META DATA 
    # ==================================================

    metadata = {
        "last_refresh": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "available_data_start": str(
            df["Transaction Date"].min()
        ),
        "available_data_end": str(
            df["Transaction Date"].max()
        ),
        "row_count": len(df),
    }

    metadata_file = (
        PROCESSED_DIR /
        "ev_metadata.json"
    )

    with open(
        metadata_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=2
        )

    print()
    print(f"Saved : {output_file}")
    print(f"Size  : {size_mb:.1f} MB")

    print(f"Saved Metadata: {metadata_file}")

    print("Done")


    if args.report:

        print()

        print("=" * 100)

        print(
            f"Output File : {output_file}"
        )

        print(
            f"Rows        : {len(df):,}"
        )

        print(
            f"Columns     : {len(df.columns):,}"
        )

        print(
            f"Size (MB)   : {size_mb:.1f}"
        )

        print("=" * 100)

if __name__ == "__main__":
    main()