import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date

## copy and run this line in your terminal --> streamlit run frontend.py
## Ctrl+c to stop the server

## =======================================================================================
## Placeholder chart generation functions
"""
When we have real data, these functions will be replaced with actual data processing and visualization logic.
For now, they generate random data to simulate the charts.
"""
#TODO: Replace with real data processing and visualization

## =======================================================================================

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


st.title("UK Crime Data Explorer")

st.set_page_config(
    page_title="UK Crime Data Explorer",
    page_icon=":police_car:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# == List of Graphs to choose from ==
all_charts = [
    "Crime Hotspots Map",
    "Crime Over Time",
    "Secondary Time Series",
    "Crime Type Pie",
    "Extra Line Chart",
    "Extra Metric Chart"
]


graph_tabs,summary_tab=st.tabs(["Graph View","Summary View"])



## ================================================================================================================================================
## Graphs Tab
"""
Main graph viewing tab with filters and chart display.
"""
## ===============================================================================================================================================

with graph_tabs:

    st.subheader("Filters (confirm before viewing charts)")

    with st.form("filter_form"):

        # == Multi-select for choosing graphs ==
        chosen_charts = st.multiselect(
            "Choose up to 4 charts to display",
            all_charts,
            default=all_charts[:4],  # Default picks first 4
        )

        # Limiting to 4 selections
        if len(chosen_charts) > 4:
            st.error("Please select up to 4 charts only.")
            st.stop()
            chosen_charts = chosen_charts[:4]


        st.subheader("Filters")
        # Police force selection
        police_force = st.selectbox("Select Police Force", ["Metropolitan", "Greater Manchester", "West Yorkshire"])

        # Date range slider
        start = date(2023, 9, 1)
        end = date.today()

        time_period = st.slider(
            "Select time period:",
            min_value=start,
            max_value=end,
            value=(start, end),
            format="YYYY-MM-DD"
    )
        # Submit button
        submitted = st.form_submit_button("Apply Filters")

    # If form is submitted, display charts
    if submitted:
        st.success("Filters applied! Displaying charts below.")

        # == Chart layout ==
        col1, col2, col3 = st.columns([2, 2, 1])

        # == KPI and Filters Column ==
        with col3:
            st.metric("Total Crimes", "1,234,567", "5.4%")
            st.metric("Solved Cases", "123,456", "-2.1%")
            st.metric("Active Investigations", "12,345", "0.5%")

        
        
        # == Charts columns ==
        chart_columns = [col1, col2]
        i = 0

        # == Display chosen charts ==
        for chart in chosen_charts:
            with chart_columns[i % 2]:
                renderer = chart_renderers.get(chart)
                if renderer:
                    renderer()
                else:
                    st.error(f"Chart renderer for {chart} not found.")
            # Increment column index        
            i += 1


## =======================================================================================================================================
## Summary Tab
"""
Tab for generating summaries of selected charts. 
"""
#TODO: Integrate with LLM data analysis for real summaries
## =======================================================================================================================================


with summary_tab:

    st.subheader("Choose the charts to summarize")

    # == Multi-select for choosing graphs ==
    chosen_charts = st.multiselect(
        "Choose up to 4 charts to display",
        all_charts,
        default=all_charts[:4],  # Default picks first 4
        )
    
    # Button to generate summary
    generate_summary = st.button("Generate Summary")

    if generate_summary and chosen_charts:
        st.success("Generating summary for selected charts...")

        for chart_name in chosen_charts:
            col1, col2 = st.columns([3, 2])

            # == Display chosen charts and summaries ==

            with col1:
                chart_renderers[chart_name]()

            with col2:
                st.markdown(f"**{chart_name} Summary:**")
                st.write(f"This is a placeholder summary for the {chart_name}. Detailed insights will be generated here based on actual data analysis.")






    
    
    


    
        
