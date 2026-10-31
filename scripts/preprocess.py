from pathlib import Path

import polars as pl

INPUT_FILE = "data/raw/20261030_ev_data.csv"
ZIP_LOOKUP_FILE = "data/raw/zip_lat_long.tsv"
OUTPUT_FILE = "data/processed/ev_data.parquet"

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
    "Vehicle Location",
]


def clean_price(value):

    try:

        if value is None:
            return None

        value = (
            str(value)
            .replace("$", "")
            .replace(",", "")
            .strip()
        )

        if value == "":
            return None

        return float(value)

    except Exception:
        return None


def extract_longitude(location):

    try:

        if location is None:
            return None

        value = (
            str(location)
            .replace("POINT (", "")
            .replace(")", "")
        )

        return float(value.split()[0])

    except Exception:
        return None


def extract_latitude(location):

    try:

        if location is None:
            return None

        value = (
            str(location)
            .replace("POINT (", "")
            .replace(")", "")
        )

        return float(value.split()[1])

    except Exception:
        return None


def main():

    print("Loading CSV...")

    df = pl.read_csv(
        INPUT_FILE,
        infer_schema_length=50000,
        ignore_errors=True,
    )

    print(f"Rows Loaded: {len(df):,}")

    print("Loading ZIP mapping...")

    zip_df = pl.read_csv(
        ZIP_LOOKUP_FILE,
        separator='|'
    )

    print(f"Rows Loaded: {len(zip_df):,}")

    columns_to_keep = [
        col
        for col in KEEP_COLUMNS
        if col in df.columns
    ]

    df = df.select(columns_to_keep)

    print(f"Columns Retained: {len(df.columns)}")

    # ------------------------------------------------
    # TRANSACTION FILTER
    # ------------------------------------------------

    if "Transaction Type" in df.columns:

        df = df.filter(
            pl.col("Transaction Type")
            .is_in(VALID_TRANSACTION_TYPES)
        )

        print(
            f"Rows After Transaction Filter: {len(df):,}"
        )

    # ------------------------------------------------
    # SALE PRICE
    # ------------------------------------------------

    if "Sale Price" in df.columns:

        df = df.with_columns(
            pl.col("Sale Price")
            .map_elements(
                clean_price,
                return_dtype=pl.Float64
            )
            .alias("Sale Price")
        )

    # ------------------------------------------------
    # ODOMETER
    # ------------------------------------------------

    if "Odometer Reading" in df.columns:

        df = df.with_columns(
            pl.col("Odometer Reading")
            .cast(
                pl.Int64,
                strict=False
            )
        )

    # ------------------------------------------------
    # DATES
    # ------------------------------------------------

    if "Sale Date" in df.columns:

        df = df.with_columns(
            pl.col("Sale Date")
            .str.strptime(
                pl.Date,
                "%B %d, %Y",
                strict=False
            )
        )

    if "Transaction Date" in df.columns:

        df = df.with_columns(
            pl.col("Transaction Date")
            .str.strptime(
                pl.Date,
                "%B %d, %Y",
                strict=False
            )
        )

# ------------------------------------------------
# DATE DERIVATIVES
# ------------------------------------------------

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
            .alias("Transaction Month Name")
        ])

    # ------------------------------------------------
    # GEO
    # ------------------------------------------------

# ----------------------------------------
# GEO LOOKUP
# ----------------------------------------

    zip_df = zip_df.with_columns(

        pl.col("GEOID")
        .cast(pl.Int64, strict=False),

        pl.col("INTPTLAT")
        .cast(pl.Float64, strict=False),

        pl.col("INTPTLONG")
        .cast(pl.Float64, strict=False)

    )

    df = df.with_columns(
        pl.col("Postal Code")
        .cast(pl.Int64, strict=False)

    )

    df = df.join(

        zip_df.select([
            "GEOID",
            "INTPTLAT",
            "INTPTLONG"
        ]),

        left_on="Postal Code",
        right_on="GEOID",
        how="left"

    )

    df = df.rename({

        "INTPTLAT": "Latitude",
        "INTPTLONG": "Longitude"

    })

    # ------------------------------------------------
    # WRITE
    # ------------------------------------------------

    print()
    print("Schema:")

    for column, dtype in df.schema.items():
        print(f"{column}: {dtype}")

    print()
    print(f"Final Rows: {len(df):,}")

    print()
    print("Writing parquet...")

    df.write_parquet(
        OUTPUT_FILE,
        compression="zstd"
    )

    size_mb = (
        Path(OUTPUT_FILE).stat().st_size
        / 1024
        / 1024
    )

    print()
    print(f"Saved: {OUTPUT_FILE}")
    print(f"Size : {size_mb:.1f} MB")
    print("Done")


if __name__ == "__main__":
    main()