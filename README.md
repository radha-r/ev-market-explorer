# EV Market Explorer

EV Market Explorer is an interactive Streamlit application for exploring electric vehicle registration activity, transaction data, pricing trends, vehicle adoption, and geographic distribution using publicly available datasets.

The project transforms raw public datasets into an optimized parquet dataset that powers analytics, search, and map-based visualizations.

---

# Features

- EV market intelligence dashboards
- Manufacturer and model analysis
- New vs Used vehicle analysis
- Transaction trend analysis
- Price distribution and pricing insights
- Geographic analysis by city, county, ZIP, and legislative district
- Interactive search
- Geographic mapping using ZIP-based latitude and longitude enrichment
- Data profiling and validation pipeline

---

# Repository Structure

```text
ev-market-explorer/
│
├── app.py
├── config.py
│
├── pipeline/
│   └── preprocess.py
│
├── pages/
│   ├── 1_Insights.py
│   ├── 2_Search.py
│   ├── 3_Map.py
│   └── 9_Feedback.py
│
├── utils/
│   ├── data.py
│   ├── filters.py
│   ├── charts.py
│   └── footer.py
│
├── data/
│   ├── raw/
│   └── processed/
│
└── README.md
```

---

# Requirements

- Python 3.13+
- Streamlit
- Polars
- Plotly

Recommended:

- uv

---

# Clone Repository

```bash
git clone https://github.com/<your-account>/ev-market-explorer.git

cd ev-market-explorer
```

---

# Create Virtual Environment

Using uv:

```bash
uv venv

.venv\Scripts\activate
```

Install dependencies:

```bash
uv sync
```

or:

```bash
pip install -r requirements.txt
```

---

# Data Sources

## Data Source 1 - Washington State Electric Vehicle Activity

Dataset:

https://data.wa.gov/Transportation/Electric-Vehicle-Title-and-Registration-Activity/rpr4-cgyd

The dataset contains electric vehicle title and registration activity information including:

```text
Clean Alternative Fuel Vehicle Type
VIN (1-10)
DOL Vehicle ID
Model Year
Make
Model
Primary Use
Electric Range
Odometer Reading
Odometer Reading Description
New or Used Vehicle
Sale Price
Sale Date
Transaction Type
Transaction Date
Year
County
City
State
Postal Code
2020 GEOID
Legislative District
Electric Utility
```

---

## Data Source 2 - US Census ZIP Latitude / Longitude Lookup

Source:

https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html

Download:

https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2026_Gazetteer/2026_Gaz_zcta_national.zip

Required Columns:

```text
GEOID
INTPTLAT
INTPTLONG
```

Definitions:

```text
GEOID     = ZIP Code
INTPTLAT  = Latitude
INTPTLONG = Longitude
```

The ZIP lookup is used to enrich the dataset with latitude and longitude information for map visualizations.

---

# Download the Data

## Step 1 - Download EV Activity Dataset

Navigate to:

https://data.wa.gov/Transportation/Electric-Vehicle-Title-and-Registration-Activity/rpr4-cgyd/about_data

Export the dataset as CSV.

Save the file as:

```text
data/raw/ev_data.csv
```

---

## Step 2 - Download ZIP Latitude / Longitude Dataset

Download:

https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2026_Gazetteer/2026_Gaz_zcta_national.zip

Extract:

```text
2026_Gaz_zcta_national.txt
```

Rename it to:

```text
zip_lat_long.tsv
```

Copy it to:

```text
data/raw/zip_lat_long.tsv
```

---

# Build the Parquet Dataset

Generate the optimized dataset:

```bash
uv run python pipeline/preprocess.py ^
    -i ev_data.csv ^
    -g zip_lat_long.tsv
```

Output:

```text
data/processed/ev_data.parquet
```

---

# Generate Dataset Profile Report

To generate profiling and validation statistics:

```bash
uv run python pipeline/preprocess.py ^
    -i ev_data.csv ^
    -g zip_lat_long.tsv ^
    --report
```

The report includes:

- Row count
- Column count
- Column data types
- Null counts
- Numeric minimums
- Numeric maximums
- Numeric averages
- Latitude coverage
- Longitude coverage
- Output file size

This is useful when validating a newly downloaded dataset.

---

# Running the Application

Start Streamlit:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# Updating Data

When a newer EV Activity dataset becomes available:

1. Download the latest CSV
2. Replace:

```text
data/raw/ev_data.csv
```

3. Regenerate the parquet dataset:

```bash
uv run python pipeline/preprocess.py ^
    -i ev_data.csv ^
    -g zip_lat_long.tsv
```

4. Restart Streamlit

---

# Development Notes

The application reads data exclusively from:

```text
data/processed/ev_data.parquet
```

Source CSV files are never read directly by the application and are only used by the preprocessing pipeline.

The preprocessing pipeline:

- Filters supported transaction types
- Cleans and converts numeric fields
- Parses dates
- Generates time-based analytics fields
- Enriches records with latitude and longitude
- Writes an optimized parquet file for application consumption

---

# Disclaimer

This project uses publicly available datasets provided by third-party organizations.

Data may contain:

- Missing values
- Incomplete records
- Duplicate records
- Geographic inaccuracies
- Delayed updates
- Processing anomalies
- Source data errors

All information, visualizations, metrics, analytics, and derived insights are provided strictly for informational and educational purposes.

No warranty is provided regarding accuracy, completeness, reliability, suitability, or fitness for any purpose.

Use this project and any derived information entirely at your own risk.

---

# Feedback

Feature requests, bug reports, and data quality concerns are welcome through the Feedback page included in the application.

---

# License

Choose a license before publishing.

Recommended:

```text
MIT License
```

for maximum usability and community contributions.
