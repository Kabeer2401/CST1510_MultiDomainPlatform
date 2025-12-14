import streamlit as st
from db_manager import DatabaseManager
import plotly.express as px

st.set_page_config(page_title="IT Ops Desk", page_icon="🛠️", layout="wide")
db = DatabaseManager()

st.title("🛠️ IT Operations & Ticket Desk")

# 1. TICKET LOGGING
with st.form("ticket_form"):
    st.subheader("Log New Support Ticket")
    col1, col2 = st.columns(2)
    with col1:
        issue = st.text_input("Issue Description")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    with col2:
        agent = st.selectbox("Assign to Agent", ["Alice", "Bob", "Charlie", "System"])

    if st.form_submit_button("Create Ticket"):
        db.create_it_ticket(issue, priority, agent)
        st.success("Ticket Assigned!")
        st.rerun()

# 2. PERFORMANCE VISUALIZATION
st.divider()
tickets = db.get_it_tickets()

if not tickets.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Agent Workload")
        # Bar chart: Who has the most tickets? (Solves 'Staff Performance' problem)
        workload = tickets['ticket_id'].value_counts()  # ticket_id column holds Agent Name
        st.bar_chart(workload)

    with col2:
        st.subheader("Ticket Queue")
        st.dataframe(tickets)
else:
    st.info("Queue is empty.")
