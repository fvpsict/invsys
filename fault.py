import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="FVPS Fault Report", layout="wide")
st.title("📋 FVPS Fault Report System")

# Initialize session state
if "fault_data" not in st.session_state:
    st.session_state.fault_data = pd.DataFrame(columns=[
        "Equipment Type", "Equipment", "Asset No", "Serial Number",
        "Fault Description", "Status", "Date Reported", "Venue"
    ])
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Clear input fields
def reset_form_state():
    for key in [
        "equipment_type", "equipment", "asset_no", "serial_no",
        "fault_desc", "status", "date_reported", "venue"
    ]:
        if key in st.session_state:
            del st.session_state[key]

# --- Fault Form ---
with st.form("fault_form"):
    st.subheader("Add New Fault Report" if st.session_state.edit_index is None else "Edit Fault Report")

    col1, col2, col3 = st.columns(3)

    options_equipment_type = [
        "Projector", "Visualiser", "Projector Screen", "Desktop", "Laptop", "iPad", "Mobile Cart", "SSOE"
    ]
    options_equipment = ["", "Desktop", "Laptop", "iPad", "Mobile Cart"]
    options_status = [
        "Open", "In Progress", "Resolved", "Closed", "Pending action by vendor", "Faulty"
    ]

    with col1:
        equipment_type = st.selectbox(
            "Equipment Type", options_equipment_type,
            index=0 if st.session_state.edit_index is None else
            options_equipment_type.index(st.session_state.fault_data.loc[st.session_state.edit_index]["Equipment Type"]),
            key="equipment_type"
        )
        asset_no = st.text_input(
            "Asset No", "" if st.session_state.edit_index is None else
            st.session_state.fault_data.loc[st.session_state.edit_index]["Asset No"],
            key="asset_no"
        )
        venue = st.text_input(
            "Venue", "" if st.session_state.edit_index is None else
            st.session_state.fault_data.loc[st.session_state.edit_index]["Venue"],
            key="venue"
        )

    with col2:
        equipment = st.selectbox(
            "Equipment", options_equipment,
            index=0 if st.session_state.edit_index is None else
            options_equipment.index(st.session_state.fault_data.loc[st.session_state.edit_index]["Equipment"]),
            key="equipment"
        )
        serial_no = st.text_input(
            "Serial Number", "" if st.session_state.edit_index is None else
            st.session_state.fault_data.loc[st.session_state.edit_index]["Serial Number"],
            key="serial_no"
        )
        fault_desc = st.text_area(
            "Fault Description", "" if st.session_state.edit_index is None else
            st.session_state.fault_data.loc[st.session_state.edit_index]["Fault Description"],
            key="fault_desc"
        )

    with col3:
        status = st.selectbox(
            "Status", options_status,
            index=0 if st.session_state.edit_index is None else
            options_status.index(st.session_state.fault_data.loc[st.session_state.edit_index]["Status"]),
            key="status"
        )
        date_reported = st.date_input(
            "Date Reported",
            value=date.today() if st.session_state.edit_index is None else
            pd.to_datetime(st.session_state.fault_data.loc[st.session_state.edit_index]["Date Reported"]),
            key="date_reported"
        )

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
            st.session_state.fault_data = pd.concat(
                [st.session_state.fault_data, pd.DataFrame([new_entry])],
                ignore_index=True
            )
            st.success("✅ Fault report submitted!")
        else:
            for key, value in new_entry.items():
                st.session_state.fault_data.at[st.session_state.edit_index, key] = value
            st.success("✅ Fault report updated!")
            st.session_state.edit_index = None

        reset_form_state()
        st.experimental_rerun()

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
