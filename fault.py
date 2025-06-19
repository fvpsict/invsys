import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="FVPS Fault Report", layout="wide")
st.title("📋 FVPS Fault Report System")

# Initialize data
if "fault_data" not in st.session_state:
    st.session_state.fault_data = pd.DataFrame(columns=[
        "Equipment Type", "Equipment", "Asset No", "Serial Number",
        "Fault Description", "Status", "Date Reported", "Venue"
    ])
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# --- Fault Form ---
with st.form("fault_form"):
    st.subheader("Add New Fault Report" if st.session_state.edit_index is None else "Edit Fault Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        equipment_type = st.selectbox("Equipment Type", [
            "Projector", "Visualiser", "Projector Screen", "Desktop", "Laptop", "iPad", "Mobile Cart", "SSOE"
        ], index=0 if st.session_state.edit_index is None else
           ["Projector", "Visualiser", "Projector Screen", "Desktop", "Laptop", "iPad", "Mobile Cart", "SSOE"].index(
               st.session_state.fault_data.loc[st.session_state.edit_index]["Equipment Type"]
           ))
        asset_no = st.text_input("Asset No", "" if st.session_state.edit_index is None else
                                 st.session_state.fault_data.loc[st.session_state.edit_index]["Asset No"])
        venue = st.text_input("Venue", "" if st.session_state.edit_index is None else
                              st.session_state.fault_data.loc[st.session_state.edit_index]["Venue"])

    with col2:
        equipment = st.selectbox("Equipment", ["", "Desktop", "Laptop", "iPad", "Mobile Cart"],
                                 index=0 if st.session_state.edit_index is None else
                                 ["", "Desktop", "Laptop", "iPad", "Mobile Cart"].index(
                                     st.session_state.fault_data.loc[st.session_state.edit_index]["Equipment"]
                                 ))
        serial_no = st.text_input("Serial Number", "" if st.session_state.edit_index is None else
                                  st.session_state.fault_data.loc[st.session_state.edit_index]["Serial Number"])
        fault_desc = st.text_area("Fault Description", "" if st.session_state.edit_index is None else
                                  st.session_state.fault_data.loc[st.session_state.edit_index]["Fault Description"])

    with col3:
        status = st.selectbox("Status", [
            "Open", "In Progress", "Resolved", "Closed", "Pending action by vendor", "Faulty"
        ], index=0 if st.session_state.edit_index is None else
           ["Open", "In Progress", "Resolved", "Closed", "Pending action by vendor", "Faulty"].index(
               st.session_state.fault_data.loc[st.session_state.edit_index]["Status"]
           ))
        date_reported = st.date_input("Date Reported", value=date.today() if st.session_state.edit_index is None else
                                      pd.to_datetime(st.session_state.fault_data.loc[st.session_state.edit_index]["Date Reported"]))

    submitted = st.form_submit_button("Update Fault" if st.session_state.edit_index is not None else "Submit Fault")

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

        if st.session_state.edit_index is None:
            # Add new entry
            st.session_state.fault_data = pd.concat(
                [st.session_state.fault_data, pd.DataFrame([new_entry])],
                ignore_index=True
            )
            st.success("✅ Fault report submitted!")
        else:
            # Update existing entry
            for key, value in new_entry.items():
                st.session_state.fault_data.at[st.session_state.edit_index, key] = value
            st.success("✅ Fault report updated!")
            st.session_state.edit_index = None

# --- Display Table with Edit/Delete ---
st.subheader("🗂 Current Fault Reports")

for i, row in st.session_state.fault_data.iterrows():
    with st.expander(f"{row['Asset No']} - {row['Equipment']} ({row['Status']})"):
        cols = st.columns([1, 1, 1, 1, 2, 1, 1, 1])
        for idx, col in enumerate(["Equipment Type", "Equipment", "Asset No", "Serial Number",
                                   "Fault Description", "Status", "Date Reported", "Venue"]):
            cols[idx].markdown(f"**{col}**: {row[col]}")

        colA, colB = st.columns([1, 1])
        if colA.button("✏️ Edit", key=f"edit_{i}"):
            st.session_state.edit_index = i
            st.experimental_rerun()

        if colB.button("🗑️ Delete", key=f"delete_{i}"):
            st.session_state.fault_data = st.session_state.fault_data.drop(index=i).reset_index(drop=True)
            st.success("🗑️ Fault report deleted!")
            st.experimental_rerun()
