# app/main.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data, plot_boxplot, plot_time_series, plot_wind_rose, get_summary_table

# Page config
st.set_page_config(page_title="Solar Energy Dashboard", layout="wide")

# Load data
@st.cache_data
def load_datasets():
    return load_data()

try:
    df_benin, df_sierra_leone, df_togo, full_df = load_datasets()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

# Sidebar
st.sidebar.title("🌍 Select Region")
countries = ['Benin', 'Sierra Leone', 'Togo']
selected_countries = st.sidebar.multiselect(
    "Choose Countries",
    options=countries,
    default=countries
)

st.sidebar.subheader("🔍 Visualizations")
viz_type = st.sidebar.radio(
    "Select Visualization Type",
    options=["Boxplot", "Time Series", "Wind Rose", "Bubble Chart"]
)

# Header
st.title("☀️ Solar Energy Dashboard for West Africa")
st.markdown("""
This dashboard provides insights into solar irradiance and weather patterns across three regions:
- Benin Malanville
- Sierra Leone Bumbuna
- Togo Dapaong QC

Use the sidebar to filter regions and select visualizations.
""")

# Show Summary Table
if st.checkbox("Show Summary Table"):
    st.subheader("📊 Summary Statistics")
    summary = get_summary_table(full_df)
    st.dataframe(summary)

# Plot based on user input
st.subheader(f"📈 {viz_type} of Solar Data")

if viz_type == "Boxplot":
    fig = plot_boxplot(full_df, selected_countries)
elif viz_type == "Time Series":
    fig = plot_time_series(full_df, selected_countries)
elif viz_type == "Wind Rose":
    fig = plot_wind_rose(full_df, selected_countries)
elif viz_type == "Bubble Chart":
    fig = plot_bubble_chart(full_df, selected_countries)

st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("📊 Powered by MoonLight Energy Solutions | 🌍 Built with Streamlit")