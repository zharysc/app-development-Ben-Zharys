import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date

## copy and run this line in your terminal --> streamlit run frontend.py
## Ctrl+c to stop the server


st.title("UK Crime Data Explorer")

st.set_page_config(
    page_title="UK Crime Data Explorer",
    page_icon=":police_car:",
    layout="wide",
    initial_sidebar_state="expanded",
)

graph_tabs,summary_tab=st.tabs(["Graph View","Summary View"])

with graph_tabs:

    col1, col2, col3 = st.columns([2,2,1])
    
    with col1:
        # == Graph 1: UK Crime Hotspots Map ==
        st.subheader("UK Crime Hotspots")
        # Create random markers within UK bounds
        uk_data = pd.DataFrame(
            np.random.randn(50, 2) * 3 + [54, -3],
            columns=['lat', 'lon']
        )
        st.map(uk_data)
        st.subheader("Graph 3")
        st.line_chart(np.random.randn(10, 2), use_container_width=True)

        # == Graph 3: Crime Type Breakdown ==
        # Placeholder data for pie chart
        

    with col2:
        # == Graph 2: Crime Over Time ==
    
        st.subheader("UK Crime Data over time")
        st.line_chart(np.random.randn(10, 2), use_container_width=True)

        # == Graph 4: Crime type distribution ==
        df = pd.DataFrame({
        "Crime type": ["Violence and sexual offences", "Robbery", "Burglary", "Vehicle crime"],
        "Percentage": [40, 30, 20, 10]
})
        st.subheader("Pie Chart of Crime Types")
        fig = px.pie(df, values='Percentage', names='Crime type', title='Crime Type Breakdown')
        st.plotly_chart(fig, use_container_width=True)

        
    
    with col3:
        st.metric("Total Crimes", "1,234,567", "5.4%")
        st.metric("Solved Cases", "123,456", "-2.1%")
        st.metric("Active Investigations", "12,345", "0.5%")

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


    
        
