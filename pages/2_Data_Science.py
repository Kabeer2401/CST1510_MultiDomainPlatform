import streamlit as st
from db_manager import DatabaseManager
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Science Hub", page_icon="📈", layout="wide")
db = DatabaseManager()

st.title("💾 Data Governance Dashboard")

# 1. FILE UPLOADER
uploaded_file = st.file_uploader("Upload CSV Dataset for Analysis", type=["csv"])

if uploaded_file is not None:
    # Analyze the file
    df = pd.read_csv(uploaded_file)
    rows = len(df)
    size_mb = uploaded_file.size / (1024 * 1024)

    st.write(f"**Preview:** {uploaded_file.name} ({rows} rows, {size_mb:.2f} MB)")

    if st.button("Save Metadata to Catalog"):
        db.add_dataset_metadata(uploaded_file.name, rows, size_mb)
        st.success("Dataset logged in Governance Database!")

# 2. VISUALIZATION
st.divider()
st.subheader("Dataset Resource Consumption")
data = db.get_datasets()

if not data.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(data)
    with col2:
        # Scatter plot
        fig = px.scatter(data, x="row_count", y="file_size_mb",
                         size="file_size_mb", hover_name="dataset_name",
                         title="Storage Impact Analysis")
        st.plotly_chart(fig)
else:
    st.info("No datasets cataloged yet.")
