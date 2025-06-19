import streamlit as st
import pandas as pd

# Link to raw Excel file on GitHub
EXCEL_URL = "https://raw.githubusercontent.com/fvpsict/invsys/main/data.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_URL)

st.title("📋 FVPS Inventory Viewer")
st.write("Data loaded live from GitHub:")

df = load_data()
st.dataframe(df)

