import streamlit as st
import pandas as pd
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="FVPS Fault Report", layout="wide")
st.title("📋 FVPS Fault Report System")

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key(st.secrets["gcp_service_account"]["sheet_id"])
worksheet = sheet.sheet1

# Load sheet data into DataFrame
@st.cache_data(ttl=60)
def load_fault_data():
    records = worksheet.get_all_records()
    return pd.DataFrame(records)

if "fault_data" not in st.session_state:
    st.session_state.fault_data = load_fault_data()

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

def reset_form_state():
    keys = [
        "equipment_type", "equipment", "asset_no", "serial_no",
        "fault_desc", "status", "date_reported", "venue"
    ]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]

# --- Fault Form ---
with st.form("fault_form"):
    st.subheader("Add New Fault Report" if st.session_state.edit_index is None else "Edit Fault Report")
    col1, col2, col3 = st.columns(3)

    equipment_types = [
        "Projector", "Visualiser", "Projector Screen", "Desktop", "Laptop", "iPad", "Mobile Cart", "SSOE"
    ]
    equipment_options = ["", "Desktop", "Laptop", "iPad", "Mobile Cart"]
    statuses = [
        "Open", "In Progress", "Resolved", "Closed", "Pending action by vendor", "Faulty"
    ]

    with col1:
        equipment_type = st.selectbox("Equipment Type", equipment_types, key="equipment_type")
        asset_no = st.text_input("Asset No", key="asset_no")
        venue = st.text_input("Venue", key="venue")

    with col2:
        equipment = st.selectbox("Equipment", equipment_options, key="equipment")
        serial_no = st.text_input("Serial Number", key="serial_no")
        fault_desc = st.text_area("Fault Description", key="fault_desc")

    with col3:
        status = st.selectbox("Status", statuses, key="status")
        date_reported = st.date_input("Date Reported", value=date.today(), key="date_reported")

    submitted = st.form_submit_button("Update Fault" if st.session_state.edit_index is not None else "Submit Fault")

    if submitted:
        new_entry = {
            "Equipment Type": st.session_state.equipment_type,
            "Equipment": st.session_state.equipment,
            "Asset No": st.session_state.asset_no,
            "Serial Number": st.session_state.serial_no,
            "Fault Description": st.session_state.fault_desc,
            "Status": st.session_state.status,
            "Date Reported": st.session_state.date_reported.strftime("%d %B %Y"),
            "Venue": st.session_state.venue,
        }

        if st.session_state.edit_index is None:
            worksheet.append_row(list(new_entry.values()))
            st.session_state.fault_data = pd.concat(
                [st.session_state.fault_data, pd.DataFrame([new_entry])],
                ignore_index=True
            )
            st.success("✅ Fault report submitted!")
        else:
            row_num = st.session_state.edit_index + 2  # account for header row
            worksheet.update(f"A{row_num}:H{row_num}", [list(new_entry.values())])
            for k, v in new_entry.items():
                st.session_state.fault_data.at[st.session_state.edit_index, k] = v
            st.success("✅ Fault report updated!")
            st.session_state.edit_index = None

        reset_form_state()
        st.experimental_rerun()

# --- Display Table with Edit/Delete ---
st.subheader("🗂 Current Fault Reports")

fields = [
    "Equipment Type", "Equipment", "Asset No", "Serial Number",
    "Fault Description", "Status", "Date Reported", "Venue"
]

for i, row in st.session_state.fault_data.iterrows():
    with st.expander(f"{row['Asset No']} - {row['Equipment']} ({row['Status']})"):
        cols = st.columns([1, 1, 1, 1, 2, 1, 1, 1])
        for idx, col in enumerate(fields):
            cols[idx].markdown(f"**{col}**: {row[col]}")

        colA, colB = st.columns([1, 1])
        if colA.button("✏️ Edit", key=f"edit_{i}"):
            st.session_state.edit_index = i
            for field in fields:
                st.session_state[field.replace(" ", "_").lower()] = row[field]
            st.experimental_rerun()

        if colB.button("🗑️ Delete", key=f"delete_{i}"):
            worksheet.delete_rows(i + 2)  # +2 for header offset (1-based + header)
            st.session_state.fault_data = st.session_state.fault_data.drop(index=i).reset_index(drop=True)
            st.success("🗑️ Fault report deleted!")
            st.experimental_rerun()
