import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
from backend_files.pie_top_3 import get_crime_types_summary
import matplotlib.pyplot as plt
import seaborn as sns
import uuid

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

    df = get_crime_types_summary(id=None, csv_data='backend_files/street_data/leicestershire_street.csv')


    palette = sns.color_palette("Set2", n_colors=len(df))  # Set2 is a popular Seaborn palette
    palette = [f'rgb({int(r*255)},{int(g*255)},{int(b*255)})' for r, g, b in palette]

    # Create interactive pie chart with Plotly
    fig = px.pie(
        df,
        names='category',
        values='percentage',
        title='Crime Type Distribution',
        color='category',         # assign colors by category
        color_discrete_sequence=palette  # use Seaborn palette
    )
    random_key = str(uuid.uuid4())

    st.plotly_chart(fig, use_container_width=True,key=random_key)


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