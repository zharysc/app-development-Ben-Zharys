import streamlit as st
from lollipop_functions import get_columns_for_crime_rate_by_region
#TODO: Grab crime rate table via df = get_columns_for_crime_rate_by_region()
#TODO: Generate kpi card for streamlit
#TODO: Add filter to KPI card which lets you pick a single Police force to look at

def render_crime_rate_kpi():
    """
    Render KPIs for crime rate per region with optional police force filter,
    including total crimes in region.
    Returns the filtered DataFrame.
    """

    st.markdown("### Crime Rate Key Performance Indicators")

    # Load the crime rate table
    df_crime_rate = get_columns_for_crime_rate_by_region()

if __name__ == "__main__":
    df_crime_rate = get_columns_for_crime_rate_by_region()
    print(df_crime_rate.dtypes)