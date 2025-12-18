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
from frontend_files.tabs.chart_summary_dic import chart_renderers
from backend_files.lollipop_functions import get_columns_for_crime_rate_by_region




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
    all_charts = list(chart_renderers.keys())
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

    # ## TODO: Integrate these filters
    # st.subheader("Filters")
    # # Police force selection
    # police_force = st.selectbox("Select Police Force", ["Metropolitan", "Greater Manchester", "West Yorkshire"])

    # # Date range slider
    # start = date(2023, 9, 1)
    # end = date.today()


    

    # == Chart layout ==
    col1, col2, col3 = st.columns([2, 2, 1])

    # == KPI and Filters Column ==
    with col3:
        # Get the DataFrame first
        df = get_columns_for_crime_rate_by_region()

        # Select police force
        selected_force = st.selectbox(
            "Select a police force",
            df['police_force_name'].unique()
        )

        # Filter the DataFrame for the selected force and round to 2 dp
        crime_rate = round(
            df.loc[df['police_force_name'] == selected_force, 'crime_rate_per_1000'].values[0],
            2
        )
        crime_count  = round(df.loc[df['police_force_name'] == selected_force, 'crime_count'].values[0],
            2
        )

        # Display the KPI
        st.markdown(f"### {selected_force}")
        st.markdown(f"Crime rate: **{crime_rate}** per 1,000 people")
        st.markdown(f"Crime count: **{crime_count}**")

        # st.metric(label=f"", value=crime_rate)



    # == Charts columns ==
    chart_columns = [col1, col2]
    i = 0

    # == Display chosen charts ==
    for chart in chosen_charts:
        with chart_columns[i % 2]:
            render_fn = chart_renderers.get(chart, {}).get("render")
            if render_fn:
                render_fn()
            else:
                st.error(f"Chart renderer for {chart} not found.")
        # Increment column index        
        i += 1

if __name__ == "__main__":
    render_dashboard_tab()