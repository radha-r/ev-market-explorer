import streamlit as st


def show_footer():

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("EV Market Explorer")

    with col2:
        url = "https://forms.gle/f3EzwVXi5CyeGqe78"
        st.markdown(f"""
        <a href="{url}" target="_blank">
        <button style="background-color:GreenYellow; padding:10px; border:none; border-radius:5px; cursor:pointer;">
        Send Feedback
        </button>
        </a>
        """, unsafe_allow_html=True)

    with col3:
        st.caption("Last Updated: Oct 31,2026")