import streamlit as st
from core.footer import show_footer

st.title("💬 Feedback")

st.markdown("""
## Help Improve EV Market Explorer

Thank you for taking the time to provide feedback.

Your suggestions help improve:

- Dashboard insights
- Search capabilities
- Mapping features
- Data quality
- New analytics and visualizations

Please use the feedback form below.
""")

url = "https://forms.gle/f3EzwVXi5CyeGqe78"
st.markdown(f"""
<a href="{url}" target="_blank">
<button style="background-color:GreenYellow; padding:10px; border:none; border-radius:5px; cursor:pointer;">
Send Feedback
</button>
</a>
""", unsafe_allow_html=True)


st.divider()

st.markdown("""
### Examples of Useful Feedback

#### Feature Requests
- Add county-level comparisons
- Add charger location overlays
- Support additional states
- Add vehicle depreciation analysis

#### Data Quality
- Incorrect city mappings
- Unexpected counts
- Missing vehicle models

#### General Suggestions
- Visual improvements
- New dashboard ideas
- Performance improvements
""")

show_footer()