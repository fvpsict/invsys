import streamlit as st
import pandas as pd

# Load Excel file from GitHub
EXCEL_URL = "invsys/data.xlsx"

@st.cache_data
def load_data():
    try:
        df = pd.read_excel(EXCEL_URL, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

st.set_page_config(page_title="FVPS Inventory System", layout="wide")

st.title("📋 FVPS Inventory System")
st.markdown("Live data loaded from GitHub Excel file.")

df = pd.read_excel("data.xlsx")

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data to display.")
