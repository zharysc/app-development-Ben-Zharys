import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
from backend_files.pie_top_3 import get_crime_types_summary
from backend_files.lollipop_functions import get_columns_for_crime_rate_by_region
from backend_files.population_functions import get_population_summary
from backend_files.crime_types_force import get_columns_for_heatmap_table
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import plotly.graph_objects as go


## =======================================================================================

## ===== Placeholder chart generation functions

#TODO: Replace with real data processing and visualization

# all_charts = [
#     "Crime Hotspots Map",
#     "Crime Over Time",
#     "Secondary Time Series",
#     "Crime Type Pie",
#     "Extra Line Chart",
#     "Extra Metric Chart"
# ]

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

def crime_rate_by_region_graph(df = None, theme = ["whitegrid", "viridis"]):

    """

    A function to create a lollipop chart of crime rate by region.

    Input: Dataframe with crime rate by region.

    Output: Lollipop chart.

    """

    # If no df is passed, fetch it
    if df is None:
        df = get_columns_for_crime_rate_by_region()

    # Sort for consistent ordering
    df = df.sort_values("crime_rate_per_1000", ascending=True)

    # Build the figure
    fig = go.Figure()

    # Add stems (lines from 0 to value)
    fig.add_trace(
        go.Scatter(
            x=df["crime_rate_per_1000"],
            y=df["police_force_name"],
            mode="lines",
            line=dict(color="lightgray", width=2),
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Add bubble points
    fig.add_trace(
        go.Scatter(
            x=df["crime_rate_per_1000"],
            y=df["police_force_name"],
            mode="markers",
            marker=dict(
                size=df["population"] / df["population"].max() * 500,  # scale size
                color=df["crime_rate_per_1000"],
                colorscale="Viridis",
                showscale=True,
                sizemode="area"
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Crime rate: %{x:.2f} per 1,000<br>"
            ),
            showlegend=False,
        )
    )

    # Layout tuning
    fig.update_layout(
        title="Crime Rate by Police Force",
        xaxis_title="Crime Rate per 1,000 People",
        yaxis_title="Police Force",
        yaxis=dict(autorange="reversed"),  # flip so highest rate at top
        template="plotly_white",
        margin=dict(l=120, r=20, t=50, b=50),
    )

    random_key = str(uuid.uuid4())

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True,key=random_key)


def render_crime_type_pie():

    df = get_crime_types_summary(id=None, csv_data='backend_files/street_data/test_crime_data.csv')


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


def render_population_bar_chart():
    """
    Function to render a bar chart of the Population
    each Police Force serves
    """
    df = get_population_summary(csv_data='backend_files/data/cleaned_population.csv')
    
    df = df.sort_values("population", ascending=False)

    # Build the figure
    fig = go.Figure()

    # Add a single Bar trace
    fig.add_trace(
        go.Bar(
            x=df["police_force_id"],
            y=df["population"],
            marker=dict(
                color=df["population"],
                colorscale="Viridis",
                showscale=True  # showscale is valid here if you want a color bar
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Population: %{y:,.0f}<extra></extra>"
            ),
            showlegend=False  # legend visibility goes here
        )
    )

    fig.update_layout(
        title="Population Served by Police Force",
        xaxis_title="Police Force",
        yaxis_title="Population",
        template="plotly_white",
        margin=dict(l=40, r=20, t=50, b=40)
    )

    # Streamlit key to avoid component reuse
    random_key = str(uuid.uuid4())
    st.plotly_chart(fig, use_container_width=True, key=random_key)

def crime_density_heatmap_graph():

    """

    A function to create a heatmap of crime on a geographical map.

    Input: Dataframe with crime locationdata.

    Output: Heatmap.

    """
    df = pd.read_csv('backend_files/street_data/test_crime_data.csv')

    categories = sorted(df["category"].dropna().unique())

    fig = go.Figure()

    # Add one density trace per category
    for cat in categories:
        df_cat = df[df["category"] == cat]

        fig.add_trace(
            go.Densitymapbox(
                lat=df_cat["latitude"],
                lon=df_cat["longitude"],
                radius=15,
                name=cat,
                visible=True
            )
        )

    # Build tick-list buttons
    buttons = []

    for i, cat in enumerate(categories):
        visibility = [False] * len(categories)
        visibility[i] = True

        buttons.append(
            dict(
                label=cat,
                method="update",
                args=[{"visible": visibility}]
            )
        )

    # Add "All" option
    buttons.insert(
        0,
        dict(
            label="All",
            method="update",
            args=[{"visible": [True] * len(categories)}]
        )
    )

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            zoom=5,
            center=dict(
                lat=df["latitude"].mean(),
                lon=df["longitude"].mean()
            )
        ),
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                showactive=True,
                x=0.02,
                y=0.98,
                xanchor="left",
                yanchor="top"
            )
        ],
        title="Spatial Density of Recorded Crimes",
        margin=dict(r=0, l=0, t=50, b=0)
    )

    # Display the figure in Streamlit
    random_key = str(uuid.uuid4())
    st.plotly_chart(fig, use_container_width=True, key=random_key)


def type_against_region_heatmap_graph():

    """

    A function to create a heatmap of crime categories by police force.

    Input: Dataframe with crime categories by police force.

    Output: Heatmap.

    """

    df = get_columns_for_heatmap_table(df_crimes = pd.read_csv("backend_files/street_data/test_crime_data.csv"),
                                          df_population = pd.read_csv("backend_files/data/cleaned_population.csv") ,
                                            df_forces = pd.read_csv("backend_files/data/forces.csv"))
    

    print(df.columns.tolist())
    theme = ["whitegrid", "viridis"]

    # Use pivot_table to avoid duplicate issues
    heatmap_data = df.pivot_table(
        index="category",
        columns="police_force_name",
        values="crime_count",
        aggfunc="sum",
        fill_value=0
    )

    fig = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="YlGnBu",
        labels=dict(
            x="Police Force",
            y="Crime Category",
            color="Number of Crimes"
        ),
        title="Crime Categories by Police Force"
    )

    fig.update_layout(
        xaxis_tickangle=45,
        height=600
    )

    # Streamlit key to avoid component reuse
    random_key = str(uuid.uuid4())
    st.plotly_chart(fig, use_container_width=True, key=random_key)



def render_extra_metric_chart():
    st.subheader("Extra Metric Chart")
    st.bar_chart(np.random.randn(10, 2), use_container_width=True)

## ==============================================================================================
## KPI Renders
## ==============================================================================================