import streamlit as st
import pandas as pd
import os

FILE_NAME = "patients.csv"

st.set_page_config(
    page_title="Clinic Tracker",
    layout="wide"
)

# ---------- CSS DESIGN ----------
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
.stApp {
    background-color: #f8fafc;
    color: #1f2937;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
}

section[data-testid="stSidebar"] * {
    color: #1f2937 !important;
}

/* ---------- HEADER ---------- */
.title-box {
    background: linear-gradient(90deg, #60a5fa, #3b82f6);
    padding: 25px;
    border-radius: 15px;
    color: white !important;
    text-align: center;
    margin-bottom: 25px;
}

.title-box h1,
.title-box p {
    color: white !important;
}

/* ---------- CARDS ---------- */
.card {
    background-color: #ffffff;
    color: #1f2937 !important;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* ---------- METRIC CARDS ---------- */
.metric-card {
    background-color: #ffffff;
    color: #1f2937 !important;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
}

/* ---------- TEXT ---------- */
h1, h2, h3, p, label, span, div {
    color: #1f2937 !important;
}

/* ---------- INPUT FIELDS ---------- */
input, textarea {
    background-color: #ffffff !important;
    color: #1f2937 !important;
    border: 1px solid #d1d5db !important;
}

/* Placeholder */
input::placeholder {
    color: #9ca3af !important;
}

/* ---------- SELECT BOX ---------- */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #1f2937 !important;
    border: 1px solid #d1d5db !important;
}

/* Selected value */
div[data-baseweb="select"] span {
    color: #1f2937 !important;
}

/* Dropdown menu */
ul {
    background-color: #ffffff !important;
}

/* Dropdown items */
ul li {
    color: #1f2937 !important;
}

/* Hover */
ul li:hover {
    background-color: #f3f4f6 !important;
}

/* ---------- BUTTON ---------- */
button {
    background-color: #3b82f6 !important;
    color: white !important;
    border-radius: 8px !important;
}

/* ---------- TABLE ---------- */
thead tr th {
    background-color: #e5e7eb !important;
    color: #111827 !important;
}

tbody tr {
    background-color: #ffffff !important;
    color: #1f2937 !important;
}

tbody tr:nth-child(even) {
    background-color: #f9fafb !important;
}

/* ---------- TOOLBAR ---------- */
div[data-testid="stDataFrameToolbar"] {
    background-color: #f3f4f6 !important;
}

div[data-testid="stDataFrameToolbar"] button svg {
    color: #1f2937 !important;
    fill: #1f2937 !important;
}

/* ---------- REMOVE DARK OVERLAY ---------- */
[data-testid="stAppViewContainer"] {
    background-color: #f8fafc !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- FILE CREATION ----------
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Customer ID", "Name", "Mobile", "Service", "Status"])
    df.to_csv(FILE_NAME, index=False)

def load_data():
    return pd.read_csv(FILE_NAME)

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

def generate_customer_id(df):
    if len(df) == 0:
        return "CLN1001"
    return "CLN" + str(1001 + len(df))

df = load_data()

# ---------- HEADER ----------
st.markdown("""
<div class="title-box">
    <h1> Clinic Appointment Tracker</h1>
    <p>Manage patients, services, and appointment status easily</p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("Clinic Menu")
menu = st.sidebar.radio(
    "Choose an option",
    ["Dashboard", "Add Patient", "Search Patient", "Active Patients"]
)

# ---------- DASHBOARD ----------
if menu == "Dashboard":
    total_patients = len(df)
    active_count = len(df[df["Status"] == "Active"])
    completed_count = len(df[df["Status"] == "Completed"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Patients</h3>
            <h1>{total_patients}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Active Patients</h3>
            <h1>{active_count}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Completed</h3>
            <h1>{completed_count}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Recent Patient Records")
    st.dataframe(df.tail(10), use_container_width=True)

# ---------- ADD PATIENT ----------
elif menu == "Add Patient":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("➕ Add New Patient")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Patient Name")
        mobile = st.text_input("Mobile Number")

    with col2:
        service = st.selectbox("Select Service", ["Consultation", "Blood Test", "Injection"])
        status = st.selectbox("Service Status", ["Active", "Completed"])

    if st.button("Add Patient", use_container_width=True):
        if name.strip() == "":
            st.error("Please enter patient name.")

        elif not mobile.isdigit() or len(mobile) != 10:
            st.error("Mobile number must be exactly 10 digits.")

        elif mobile in df["Mobile"].astype(str).values:
            st.error("This mobile number already exists.")

        else:
            customer_id = generate_customer_id(df)

            new_patient = {
                "Customer ID": customer_id,
                "Name": name,
                "Mobile": mobile,
                "Service": service,
                "Status": status
            }

            df = pd.concat([df, pd.DataFrame([new_patient])], ignore_index=True)
            save_data(df)

            st.success("Patient added successfully!")
            st.info(f"Generated Customer ID: {customer_id}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- SEARCH PATIENT ----------
elif menu == "Search Patient":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🔍 Search Patient")

    search_value = st.text_input("Enter Customer ID or Mobile Number")

    if st.button("Search", use_container_width=True):
        result = df[
            (df["Customer ID"].astype(str).str.lower() == search_value.lower()) |
            (df["Mobile"].astype(str) == search_value)
        ]

        if result.empty:
            st.error("No patient found.")

        else:
            patient = result.iloc[0]

            badge = (
                '<span class="active-badge">Active</span>'
                if patient["Status"] == "Active"
                else '<span class="completed-badge">Completed</span>'
            )

            st.markdown(f"""
            <div class="patient-detail">
                <p><b>Customer ID:</b> {patient['Customer ID']}</p>
                <p><b>Name:</b> {patient['Name']}</p>
                <p><b>Mobile:</b> {patient['Mobile']}</p>
                <p><b>Service:</b> {patient['Service']}</p>
                <p><b>Status:</b> {badge}</p>
            </div>
            """, unsafe_allow_html=True)

            if patient["Status"] == "Active":
                if st.button("Mark as Completed"):
                    df.loc[df["Customer ID"] == patient["Customer ID"], "Status"] = "Completed"
                    save_data(df)
                    st.success("Patient marked as completed.")
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ACTIVE PATIENTS ----------
elif menu == "Active Patients":
    st.header("🟡 Active Patients Dashboard")

    active_patients = df[df["Status"] == "Active"]

    if active_patients.empty:
        st.info("No active patients available.")

    else:
        st.dataframe(active_patients, use_container_width=True)

        selected_id = st.selectbox(
            "Select Customer ID to mark as completed",
            active_patients["Customer ID"]
        )

        if st.button("Mark Selected Patient as Completed", use_container_width=True):
            df.loc[df["Customer ID"] == selected_id, "Status"] = "Completed"
            save_data(df)
            st.success("Selected patient marked as completed.")
            st.rerun()