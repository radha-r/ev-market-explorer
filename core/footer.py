import streamlit as st


def show_footer():
    st.divider()
    st.caption(
        "Insights are derived from public vehicle registration and transaction data and may not reflect current market conditions. "
        "Please validate information with official sources before making purchasing, financial, or business decisions."
        )

    st.write("Please feel free send your feedback about EV Market Explorer. Thanks.")
    st.page_link("https://forms.gle/f3EzwVXi5CyeGqe78", label="Send Feedback", icon="🌎")
