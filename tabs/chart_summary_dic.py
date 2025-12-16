## =======================================================================================
# chart_summary_dic.py

# This module defines a dictionary mapping chart names to their rendering and summary functions.
# Imports necessary functions from chart_renders and other modules.
# Assign them to a dictionary for easy access.
## =======================================================================================

# Imports
# Import summary functions ===============
# Pie chart
from pie_top_3 import get_crime_types_summary
# Import chart rendering functions
from chart_renders import (
    render_crime_hotspots_map,
    render_crime_over_time,
    render_secondary_time_series,
    render_crime_type_pie,
    render_extra_line_chart,
    render_extra_metric_chart
)
chart_renderers = {
    "Crime Hotspots Map": {
        "render": render_crime_hotspots_map,
        "summary": None,  # or the corresponding summary function if exists
    },
    "Crime Over Time": {
        "render": render_crime_over_time,
        "summary": None,
    },
    "Secondary Time Series": {
        "render": render_secondary_time_series,
        "summary": None,
    },
    "Crime Type Pie": {
        "render": render_crime_type_pie,
        "summary": get_crime_types_summary,  # from pie_top_3
    },
    "Extra Line Chart": {
        "render": render_extra_line_chart,
        "summary": None,
    },
    "Extra Metric Chart": {
        "render": render_extra_metric_chart,
        "summary": None,
    },
}
