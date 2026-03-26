import streamlit as st


hex_colour = st.color_picker('Pick a base colour', '#4A90E2')

st.write('The current color is', hex_colour)

## === Sending hex code to LLM backend to generate themes === ##
prompt = f"""
You are a theme generator for a web application.
Given the base colour {hex_colour}, generate a color palette for:
1. Primary Color
2. Secondary Color
3. Background Color
4. Text Color
5. Accent Color
Return JSON only with hex values
"""
