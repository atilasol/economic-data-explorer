import pandas as pd
import requests
import streamlit as st

BASE_URL = "http://api.worldbank.org/v2/"

# Predefined readable names (optional)
INDICATORS = {
    'NY.GDP.MKTP.CD': 'GDP',
    'NY.GDP.PCAP.CD': 'GDP per capita',
    'SP.POP.TOTL': 'Population',
    'FP.CPI.TOTL.ZG': 'Inflation (CPI)',
    'NE.EXP.GNFS.CD': 'Exports',
    'NE.IMP.GNFS.CD': 'Imports',
    'SL.UEM.TOTL.ZS': 'Unemployment rate'
}

@st.cache_data
def get_country_list():
    """Fetch a dictionary of country codes and names from World Bank API."""
    url = f"{BASE_URL}country?format=json&per_page=1000"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to fetch country list from World Bank API.")
        return {}

    data = response.json()
    if data and len(data) > 1:
        return {c['id']: c['name'] for c in data[1]}
    return {}

@st.cache_data
def get_world_bank_data(selected_countries, selected_indicators, start_year, end_year):
    """Fetch World Bank data for selected countries, indicators, and years."""
    if not selected_countries or not selected_indicators:
        return pd.DataFrame()

    country_str = ";".join(selected_countries)
    indicator_str = ";".join(selected_indicators)
    date_range = f"{start_year}:{end_year}"

    url = f"{BASE_URL}country/{country_str}/indicator/{indicator_str}?format=json&date={date_range}&per_page=10000"
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        return pd.DataFrame()

    data = response.json()
    if not data or len(data) < 2 or not data[1]:
        return pd.DataFrame()

    # Normalize JSON into flat table
    df = pd.json_normalize(data[1])
    df = df.rename(columns={
        'country.value': 'Country',
        'indicator.value': 'Indicator',
        'value': 'Value',
        'date': 'Year'
    })

    # Pivot so indicators are columns
    df_pivot = df.pivot_table(
        index=['Country', 'Year'],
        columns='Indicator',
        values='Value',
        aggfunc='first'
    ).reset_index()

    df_pivot.columns.name = None

    df_pivot["Year"] = df_pivot["Year"].astype(int)

    # Optionally rename columns using INDICATORS if available
    df_pivot = df_pivot.rename(columns={v: INDICATORS[k] for k, v in zip(selected_indicators, df['Indicator'].unique()) if k in INDICATORS})

    return df_pivot


