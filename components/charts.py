import streamlit as st
import altair as alt
import pandas as pd

def render_chart(df, selected_indicator, selected_countries):
    # Filter for selected countries
    df_filtered = df[df['Country'].isin(selected_countries)]

    st.subheader(f"{selected_indicator} ({df['Year'].min()}-{df['Year'].max()})")

    chart = alt.Chart(df_filtered).mark_line().encode(
        x='Year:O',
        y=alt.Y(f'{selected_indicator}:Q', title=selected_indicator),
        color='Country:N',
        tooltip=['Country', 'Year', selected_indicator]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    
def render_mv_charts(df, selected_indicator):
    
    st.subheader(f"{selected_indicator} SMA ({df["Year"][0]}-{df["Year"][len(df)-1]})")

    st.line_chart(
        data=df,
        x="Year",
        y="SMA_5",
        x_label="Year",
        y_label=f"{selected_indicator} (Moving Avg)",
        color="Country"
    )
    
    st.subheader(f"{selected_indicator} EMA ({df["Year"][0]}-{df["Year"][len(df)-1]})")

    st.line_chart(
        data=df,
        x="Year",
        y="EMA_5",
        x_label="Year",
        y_label=f"{selected_indicator} (Moving Avg)",
        color="Country"
    )


    # --- Download Chart Option ---
    # --- TO BE IMPLEMENTED ---
