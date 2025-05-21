import streamlit as st
import matplotlib.pyplot as plt
import os
import pandas as pd
import utils  # Make sure utils.py exists in the same folder

# Set page config
st.set_page_config(page_title="Solar Energy Dashboard", layout="wide")

# Load CSS for styling (comment out if not needed)
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# local_css("style.css")  # Optional - comment/uncomment as needed

# Load data
@st.cache_data
def load_data():
    benin, sierra, togo = utils.load_data()
    all_data = pd.concat([benin, sierra, togo], ignore_index=True)
    return benin, sierra, togo, all_data

try:
    benin_df, sl_df, togo_df, full_df = load_data()
except Exception as e:
    st.error("Error loading data. Make sure the clean CSV files exist in the data/ folder.")
    st.stop()

# Sidebar
st.sidebar.title("🌍 Select Region")
countries = ['Benin', 'Sierra Leone', 'Togo']
selected_countries = st.sidebar.multiselect("Choose Countries", options=countries, default=countries)

st.sidebar.subheader("🔍 Visualizations")
viz_type = st.sidebar.radio("Select Visualization Type", 
                            options=["Boxplot", "Time Series", "Wind Rose", "Bubble Chart"])

# Header
st.title("☀️ Solar Energy Dashboard for West Africa")
st.markdown("""
This dashboard provides insights into solar irradiance and weather patterns across three regions:
- Benin Malanville
- Sierra Leone Bumbuna
- Togo Dapaong QC

Use the sidebar to filter regions and select visualizations.
""")

# Show summary table
if st.checkbox("Show Summary Table"):
    st.subheader("📊 Summary Statistics")
    summary = utils.get_summary_table(full_df, selected_countries)
    st.dataframe(summary)