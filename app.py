import streamlit as st

st.set_page_config(
    page_title="IND320 Reservoir Dashboard",
    page_icon="⚡",
    layout="wide"
)

st.title("Welcome to IND320 Project - Norwegian Reservoirs")
st.markdown("""
This interactive web application was developed to analyze historical data on energy reservoirs.

### How to navigate the app:
- Use the **left sidebar** to switch between the different sections:
    - **Interactive Table**: To explore and filter the complete dataset.
    - **Reservoir Plot**: To visualize the fill rate trend.
    - **Extra**: Additional section for customized analysis.
""")

st.info("Use the sidebar menu to start exploring the data.")