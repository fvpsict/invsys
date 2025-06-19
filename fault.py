import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="FVPS Fault Report", layout="wide")

st.title("📋 FVPS Fault Report System")

# Load or initialize fault data
if "fault_data" not in st.session_state:
    st.session_state.fault_data = pd.DataFrame(columns=[
        "Equipment Type", "Equipment", "Asset No", "Serial Number", "Fault Description", "Status", "Date Reported", "Venue"
    ])

# --- Form Input ---
with st.form("fault_form"):
    st.subheader("Add New Fault Report")
    col1, col2, col3 = st.columns(3)

    with col1:
        equipment_type = st.selectbox("Equipment Type", [
            "Projector", "Visualiser", "Projector Screen", "Desktop", "Laptop", "iPad", "Mobile Cart", "SSOE"
        ])
        asset_no = st.text_input("Asset No")
        venue = st.text_input("Venue")

    with col2:
        equipment = st.selectbox("Equipment", ["", "Desktop", "Laptop", "iPad", "Mobile Cart"])
        serial_no = st.text_input("Serial Number")
        fault_desc = st.text_area("Fault Description")

    with col3:
        status = st.selectbox("Status", [
            "Open", "In Progress", "Resolved", "Closed", "Pending action by vendor", "Faulty"
        ])
        date_reported = st.date_input("Date Reported", value=date.today())

    submitted = st.form_submit_button("Submit Fault")

    if submitted:
        new_entry = {
            "Equipment Type": equipment_type,
            "Equipment": equipment,
            "Asset No": asset_no,
            "Serial Number": serial_no,
            "Fault Description": fault_desc,
            "Status": status,
            "Date Reported": date_reported.strftime("%d %B %Y"),
            "Venue": venue,
        }
        st.session_state.fault_data = pd.concat(
            [st.session_state.fault_data, pd.DataFrame([new_entry])],
            ignore_index=True
        )
        st.success("✅ Fault report submitted!")

# --- Display Table ---
st.subheader("🗂 Current Fault Reports")
st.dataframe(st.session_state.fault_data, use_container_width=True)

