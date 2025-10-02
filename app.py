import streamlit as st
from components.header import render_header
from components.sidebar import render_sidebar
from components.charts import render_chart, render_mv_charts
from services.world_bank import *
from services.analytics import *
from services.downloads import download_csv, download_excel

def main():
    # --- Header ---
    render_header()

    # --- Load countries and indicators ---
    country_dict = get_country_list()
    country_names = list(country_dict.values())
    indicator_names = list(INDICATORS.values())

    # --- Sidebar ---
    selected_countries, selected_indicator, start_year, end_year = render_sidebar(country_names, indicator_names)

    # --- Map names to codes ---
    selected_country_codes = [k for k, v in country_dict.items() if v in selected_countries]
    selected_indicator_codes = {k: v for k, v in INDICATORS.items() if v in selected_indicator}

    tab1, tab2, tab3 = st.tabs(["Chart", "Data", "Analytics"])

    
    with tab2:
        if selected_country_codes and selected_indicator_codes:
            df = get_world_bank_data(selected_country_codes, selected_indicator_codes, start_year, end_year)
            st.dataframe(df)
        else:
            st.warning("Please select at least one country and one indicator.")

        download_csv(df)
        download_excel(df)

    with tab1:
        render_chart(df, selected_indicator, selected_countries)
        render_mv_charts(calculate_moving_averages(df, selected_indicator), selected_indicator)
        
    with tab3:
        st.header(f"Selected Indicator: {selected_indicator}")
        
        st.subheader("Compound Annual Growth Rate (%)")
        cagr = calculate_cagr(df, selected_countries, selected_indicator, start_year, end_year)
        st.dataframe(cagr)

        st.subheader("Data Summary")
        st.dataframe(describe_data(df, selected_countries, selected_indicator))

if __name__ == "__main__":
    main()
