import streamlit as st
import pandas as pd
from io import BytesIO

def download_csv(df):
    csv = df.to_csv().encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="data.csv",
        mime="text/csv",
        icon=":material/download:"
    )

def download_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    excel_data = output.getvalue()

    st.download_button(
        label="Download Excel",
        data=excel_data,
        file_name="data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        icon=":material/download:"
    )