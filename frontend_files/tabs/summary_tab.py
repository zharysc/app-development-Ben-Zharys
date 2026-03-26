import streamlit as st
from datetime import date
import pandas as pd
import numpy as np
from .chart_summary_dic import chart_renderers
from backend_files.prompt_function import generate_chart_analysis_summary
from backend_files.population_functions import get_population_summary
from backend_files.crime_density import crime_density_heatmap_info

## =======================================================================================================================================
## Summary Tab
"""
Tab for generating summaries of selected charts. 
"""
## =======================================================================================================================================


def render_summary_tab():

    st.subheader("Choose the charts to summarize")

    # == Multi-select for choosing graphs ==
    chosen_charts = st.multiselect(
        "Choose up to 4 charts to display",
        list(chart_renderers.keys()),
        # default=all_charts[:2], # Default picks first 4
        key = "summary_charts"  
        )
    
    # Button to generate summary
    generate_summary = st.button("Generate Summary")

    if generate_summary and chosen_charts:
        st.success("Generating summary for selected charts...")

        for chart_name in chosen_charts:
            col1, col2 = st.columns([3, 2])

            # == Display chosen charts and summaries ==

            with col1:
                chart_renderers[chart_name]["render"]()


            # == Display chart summary ==
            with col2:
                st.markdown(f"**{chart_name} Summary:**")
                # Special case for Population data
                if chart_name == "Population":
                    summary = generate_chart_analysis_summary(
                                # Wrap the population summary fetcher so it's called later
                                get_population_summary,
                                id=None,
                                csv_data="backend_files/data/cleaned_population.csv",
                                word_limit=50,
                                prompt_template=None
                            )

                    st.write(summary)

                else:
                    summary_func = chart_renderers[chart_name]["summary"]
                    
                    if summary_func:
                        # Call the summary function (you can pass arguments if needed)
                        summary = generate_chart_analysis_summary(summary_func)
                        st.write(summary)
                    else:
                        st.write(f"This is a placeholder summary for the {chart_name}. Detailed insights will be generated here based on actual data analysis.")

if __name__ == "__main__":
    render_summary_tab()
