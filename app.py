import streamlit as st
from core.footer import show_footer

st.set_page_config(
    page_title="EV Market Explorer",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ EV Market Explorer")

st.markdown("""
## Explore Electric Vehicle Trends, Transactions, and Market Intelligence

EV Market Explorer is an interactive analytics platform designed to help users explore electric vehicle registrations, sales activity, pricing trends, geographic distribution, and market adoption patterns.

Using publicly available vehicle registration and transaction records, the platform provides insights into:

- EV adoption trends across cities, counties, and legislative districts
- Manufacturer and model market share
- New versus used vehicle activity
- Vehicle transaction seasonality
- Sale price distributions and pricing trends
- Utility service territory participation
- Geographic concentrations of electric vehicles
- Emerging vehicle launches and adoption patterns

The goal of this project is to transform large public datasets into meaningful, easy-to-understand visualizations and insights that can be explored by consumers, researchers, policymakers, journalists, industry analysts, and EV enthusiasts.

---

## Data Sources

The information presented in this application is derived from publicly available datasets published by government agencies and other public data providers.

Data may be periodically updated, revised, corrected, or withdrawn by the original source providers.

Additional geographic reference data may be combined with source datasets to support mapping and spatial analysis.

---

## Important Disclaimer

This application is provided for informational and educational purposes only.

While efforts have been made to process, transform, and present the data accurately, the information displayed within this application may contain errors, omissions, inaccuracies, delays, duplicate records, missing records, geolocation inaccuracies, processing errors, or other inconsistencies.

The creators and maintainers of this application:

- Make no guarantees regarding data accuracy, completeness, reliability, timeliness, or suitability.
- Do not warrant that any analysis, visualization, statistic, calculation, ranking, or insight is correct.
- Are not responsible for any decisions, actions, losses, damages, or consequences resulting from the use of this application.
- Are not liable for errors contained in source data or introduced during processing.

Users are solely responsible for independently validating any information before relying on it for business, financial, legal, governmental, commercial, operational, academic, or personal purposes.

---

## Use At Your Own Risk

All information, visualizations, charts, maps, metrics, and derived analytics are provided **"as is"** and **without warranty of any kind**.

By using this application, you acknowledge that:

- Data may be incomplete or inaccurate.
- Results may not reflect current real-world conditions.
- Information should not be treated as authoritative.
- Any reliance on information provided by this application is entirely at your own risk.
""")

show_footer()