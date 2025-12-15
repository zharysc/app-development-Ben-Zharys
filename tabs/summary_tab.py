import streamlit as st
from chart_renders import chart_renderers, all_charts

## =======================================================================================================================================
## Summary Tab
"""
Tab for generating summaries of selected charts. 
"""
#TODO: Integrate with LLM data analysis for real summaries
## =======================================================================================================================================


def render_summary_tab():

    st.subheader("Choose the charts to summarize")

    # == Multi-select for choosing graphs ==
    chosen_charts = st.multiselect(
        "Choose up to 4 charts to display",
        all_charts,
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
                chart_renderers[chart_name]()

            with col2:
                st.markdown(f"**{chart_name} Summary:**")
                st.write(f"This is a placeholder summary for the {chart_name}. Detailed insights will be generated here based on actual data analysis.")

if __name__ == "__main__":
    render_summary_tab()
