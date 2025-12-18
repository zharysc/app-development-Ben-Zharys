import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
from backend_files.scrapper import crime_index_countries 
from frontend_files.tabs.dashboard_tab import render_dashboard_tab
from frontend_files.tabs.summary_tab import render_summary_tab
from frontend_files.tabs.webscrapping_tab import render_top_countries_crime_index


## copy and run this line in your terminal --> streamlit run frontend.py
## Ctrl+c to stop the server


st.set_page_config(
    page_title="My App",    # Optional
    layout="wide",          # <-- This makes your app use full width
    initial_sidebar_state="expanded"  # Optional
)

st.title("Crime Data Dashboard")

# Define tabs
tab1, tab2, tab3 = st.tabs(["Dashboard", "Summary", "Other countries Crime Index"])

with tab1:
    render_dashboard_tab()

with tab2:
    render_summary_tab()

with tab3:
    render_top_countries_crime_index()



    
    
    


    
        
