import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
## =======================================================================================

## ===== Placeholder chart generation functions

#TODO: Replace with real data processing and visualization

all_charts = [
    "Crime Hotspots Map",
    "Crime Over Time",
    "Secondary Time Series",
    "Crime Type Pie",
    "Extra Line Chart",
    "Extra Metric Chart"
]

def render_crime_hotspots_map():
    st.subheader("UK Crime Hotspots")
    uk_data = pd.DataFrame(
        np.random.randn(50, 2) * 3 + [54, -3],
        columns=["lat", "lon"]
    )
    st.map(uk_data)

def render_crime_over_time():
    st.subheader("UK Crime Data over time")
    st.line_chart(np.random.randn(10, 2), use_container_width=True)

def render_secondary_time_series():
    st.subheader("Secondary Time Series")
    st.line_chart(np.random.randn(10, 1), use_container_width=True)

def render_crime_type_pie():
    df = pd.DataFrame({
        "Crime type": [
            "Violence and sexual offences",
            "Robbery",
            "Burglary",
            "Vehicle crime",
        ],
        "Percentage": [40, 30, 20, 10],
    })
    st.subheader("Pie Chart of Crime Types")
    fig = px.pie(df, values="Percentage", names="Crime type", title="Crime Type Breakdown")
    st.plotly_chart(fig, use_container_width=True)

def render_extra_line_chart():
    st.subheader("Extra Line Chart")
    st.line_chart(np.random.randn(10, 2), use_container_width=True)

def render_extra_metric_chart():
    st.subheader("Extra Metric Chart")
    st.bar_chart(np.random.randn(10, 2), use_container_width=True)

chart_renderers = {
    "Crime Hotspots Map": render_crime_hotspots_map,
    "Crime Over Time": render_crime_over_time,
    "Secondary Time Series": render_secondary_time_series,
    "Crime Type Pie": render_crime_type_pie,
    "Extra Line Chart": render_extra_line_chart,
    "Extra Metric Chart": render_extra_metric_chart,
}
## =======================================================================================