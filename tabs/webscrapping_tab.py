
import streamlit as st
import os
import sys

# Adjust path to import scrapper module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scrapper import crime_index_countries

## =======================================================================================================================================
## Webscrapping Tab

# Top 10 countries by crime index
# Recent news articles on crime

#TODO: Integrate with LLM data analysis for real summaries
## =======================================================================================================================================

# == Renders
def render_top_countries_crime_index():
    """
    Renders a table of the top 10 countries by Crime Index."""
    st.subheader("Top 10 Countries by Crime Index")

    # User inputs
    num_countries = st.slider("Number of countries to display:", min_value=1, max_value=50, value=10)

    sort_order = st.selectbox("Sort by Crime Index:", ["Highest", "Lowest"])
    ascending = True if sort_order == "Lowest" else False

    continents = ["All", "Europe", "Asia", "Africa", "North America", "South America", "Oceania"]
    selected_continent = st.selectbox("Select Continent:", continents)
    continent = None if selected_continent == "All" else selected_continent

    df = crime_index_countries(continent,num_countries, ascending)

    # Display table
    st.subheader(f"Top {num_countries} Countries by Crime Index")
    st.table(df[["City", "Crime Index"]])

if __name__ == "__main__":
    render_top_countries_crime_index()