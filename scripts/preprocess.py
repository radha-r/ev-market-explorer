from pathlib import Path

import polars as pl

INPUT_FILE = "data/raw/ev_data.csv"
OUTPUT_FILE = "data/processed/ev_data.parquet"


def main():

    df = pl.read_csv(
        INPUT_FILE,
        infer_schema_length=10000
    )

    print(f"Rows: {len(df):,}")

    df.write_parquet(OUTPUT_FILE)

    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()