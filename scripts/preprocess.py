from pathlib import Path
import polars as pl


INPUT_FILE = "data/raw/ev_data.csv"
OUTPUT_FILE = "data/processed/ev_data.parquet"


def extract_longitude(location):

    try:
        if location is None:
            return None

        value = (
            str(location)
            .replace("POINT (", "")
            .replace(")", "")
        )

        parts = value.split()

        return float(parts[0])

    except:
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

        parts = value.split()

        return float(parts[1])

    except:
        return None


def main():

    print("Loading CSV...")

    df = pl.read_csv(
        INPUT_FILE,
        infer_schema_length=10000
    )

    print(f"Rows: {len(df):,}")

    df = df.with_columns([
        pl.col("Vehicle Location")
        .map_elements(
            extract_latitude,
            return_dtype=pl.Float64
        )
        .alias("Latitude"),

        pl.col("Vehicle Location")
        .map_elements(
            extract_longitude,
            return_dtype=pl.Float64
        )
        .alias("Longitude")
    ])

    df.write_parquet(OUTPUT_FILE)

    print("Saved:")
    print(OUTPUT_FILE)

    print("")
    print("Columns added:")
    print("Latitude")
    print("Longitude")


if __name__ == "__main__":
    main()