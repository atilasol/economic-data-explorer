import pandas as pd
import streamlit as st

def calculate_cagr(df, selected_countries, selected_indicator, start_year, end_year):
    end_year -= 1
    t = end_year - start_year
    cagr_list = []

    for country in selected_countries:
        start_value = df[(df["Country"] == country) & (df["Year"] == start_year)][selected_indicator].iloc[0]
        end_value = df[(df["Country"] == country) & (df["Year"] == end_year)][selected_indicator].iloc[0]

        cagr = (end_value / start_value) ** (1/t) -1
        cagr_list.append(cagr)

    cagr_df = pd.DataFrame({"Country": selected_countries, f"CAGR(%) of {selected_indicator} ({start_year}-{end_year})":cagr_list})
    return cagr_df

def describe_data(df, selected_countries, selected_indicator):
    describe = pd.DataFrame()

    for country in selected_countries:
        stats = df.loc[df["Country"] == country, selected_indicator].describe()
        describe[country] = stats

    return describe

def calculate_moving_averages(df, selected_indicator):
    window_size = 5

    df_mv = df

    df_mv["SMA_5"] = df[selected_indicator].rolling(window=window_size).mean()
    df_mv['EMA_5'] = df[selected_indicator].ewm(span=window_size, adjust=False).mean()

    return df_mv