## ================================================================================================================================================
## Graphs Tab
"""
Main graph viewing tab with filters and chart display.
"""
## ===============================================================================================================================================

import streamlit as st
from datetime import date
import pandas as pd
import numpy as np
from frontend_files.chart_renders import chart_renderers, all_charts



## ===== KPI Functions
# When we have real data, these functions will be replaced with actual data processing and visualization logic.
# For now, they generate random data to simulate the charts.

#TODO: Replace with real data processing and visualization

## =======================================================================================


#
#
#
#
#
#






## ===== Main dashboard rendering function =======================================================

def render_dashboard_tab():
    # st.title("Dashboard Tab")

    st.subheader("Choose the charts to display")
    # == Multi-select for choosing graphs ==
    chosen_charts = st.multiselect(
        "Choose up to 4 charts to display",
        all_charts,
        default=all_charts[:4], # Default picks first 4
        key = "dashboard_charts",  
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
    

    # == Chart layout ==
    col1, col2, col3 = st.columns([2, 2, 1])

    # == KPI and Filters Column ==
    with col3:
        st.subheader("Key Performance Indicators (KPIs)")

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

if __name__ == "__main__":
    render_dashboard_tab()