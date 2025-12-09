import streamlit as st
import pandas as pd
from db_manager import DatabaseManager

st.set_page_config(page_title="Cyber Dashboard", page_icon="📊", layout="wide")

# --- SECURITY CHECK (From Lecture Part 2) ---
# "First thing we do: check if the user is logged in"
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

# Initialize DB
db = DatabaseManager()

# --- SIDEBAR FILTERS (From Lecture "Layout Demo") ---
with st.sidebar:
    st.header(f"User: {st.session_state.username}")
    st.divider()
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")

# --- MAIN CONTENT ---
st.title("📊 Cybersecurity Incident Dashboard")

# 1. INPUT FORM (Widgets Demo)
with st.expander("➕ Report New Incident"):
    with st.form("incident_form"):
        col1, col2 = st.columns(2)
        with col1:
            i_type = st.selectbox("Incident Type", ["Phishing", "Malware", "DDoS", "Policy Violation"])
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        with col2:
            status = st.selectbox("Status", ["Open", "Investigating", "Resolved"])

        submitted = st.form_submit_button("Submit Report")
        if submitted:
            db.create_cyber_incident(i_type, severity, status)
            st.success("Incident logged!")
            st.rerun()  # Refresh page to show new data

# 2. DATA DISPLAY (Mini Dashboard Concept)
incidents = db.read_cyber_incidents()

if incidents:
    # Convert DB data to DataFrame
    df = pd.DataFrame(incidents, columns=["ID", "Type", "Severity", "Status", "Time"])

    st.divider()

    # Layout Columns
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Incident Counts by Type")
        # Using built-in Streamlit charts as per Lecture Part 3
        type_counts = df["Type"].value_counts()
        st.bar_chart(type_counts)

    with col_right:
        st.subheader("Severity Distribution")
        # Using Area chart as per Lecture "Mini Dashboard" example
        sev_counts = df["Severity"].value_counts()
        st.area_chart(sev_counts)

    with st.expander("See raw data (Database View)"):
        st.dataframe(df)

else:
    st.info("No incidents found. Add one above!")
