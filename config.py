from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"

PROCESSED_DIR = DATA_DIR / "processed"

DEFAULT_PARQUET_FILE = "ev_data.parquet"

PARQUET_PATH = (
    PROCESSED_DIR /
    DEFAULT_PARQUET_FILE
)