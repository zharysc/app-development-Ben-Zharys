## =======================================================================================
# chart_summary_dic.py

# This module defines a dictionary mapping chart names to their rendering and summary functions.
# Imports necessary functions from chart_renders and other modules.
# Assign them to a dictionary for easy access.
## =======================================================================================

# Imports
# Import summary functions ===============
# Pie chart
from backend_files.pie_top_3 import get_crime_types_summary
# Crime rates
from backend_files.lollipop_functions import crime_rate_by_region_info
# Population
from backend_files.population_functions import get_population_summary
#Crime density heatmap
from backend_files.crime_density import crime_density_heatmap_info
# Crime types by force
from backend_files.crime_types_force import type_against_region_heatmap_info
# Import chart rendering functions
from frontend_files.chart_renders import (
    crime_density_heatmap_graph,
    render_crime_over_time,
    crime_rate_by_region_graph,
    render_crime_type_pie,
    render_population_bar_chart,
    type_against_region_heatmap_graph
)
chart_renderers = {
    "Crime Hotspots Map (...in progress)": {
        "render": crime_density_heatmap_graph,
        "summary": None,  # or the corresponding summary function if exists
    },
    "Crime Over Time (...in progress)": {
        "render": render_crime_over_time,
        "summary": None,
    },
    "Crime Rate By Region": {
        "render": crime_rate_by_region_graph,
        "summary": crime_rate_by_region_info,
    },
    "Crime Type Pie": {
        "render": render_crime_type_pie,
        "summary": get_crime_types_summary,  # from pie_top_3
    },
    "Population": {
        "render": render_population_bar_chart,
        "summary": get_population_summary,
    },
    "Crime Types and Force Heatmap": {
        "render": type_against_region_heatmap_graph,
        "summary": type_against_region_heatmap_info,
    },
}
