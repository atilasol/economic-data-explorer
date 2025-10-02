import streamlit as st
from PIL import Image

APP_TITLE = "Economic Data Explorer"

def render_header():
    try:
        favicon = Image.open("./economic.png")
    except:
        favicon = None

    st.set_page_config(page_title=APP_TITLE, layout="wide", page_icon=favicon)
    st.title(APP_TITLE)
