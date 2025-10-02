import streamlit as st
from datetime import datetime

def render_sidebar(country_names, indicator_names):
    st.sidebar.title("Filter Data")
    st.sidebar.divider()

    selected_countries = st.sidebar.multiselect(
        "Select countries:",
        options=sorted(country_names),
        default=["Italy"]
    )

    selected_indicators = st.sidebar.selectbox(
        "Select indicators:",
        options=sorted(indicator_names),
    )

    start_year, end_year = st.sidebar.slider(
        "Select year range:", 1960, datetime.now().year, (2000, datetime.now().year)
    )

    st.sidebar.divider()
    st.sidebar.write("Source: https://data.worldbank.org")

    return selected_countries, selected_indicators, start_year, end_year
