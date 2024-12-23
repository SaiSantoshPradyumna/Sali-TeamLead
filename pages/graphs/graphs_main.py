# pages/graphs/graphs_main.py

import streamlit as st
from . import environmental_factors
from . import hive_metrics
from . import resource_analysis
from . import flower_availability

def app():
    st.title("Graphs")
    # Subcategories as selectbox
    graph_subcategories = ["Environmental Factors", "Hive Metrics", "Resource Analysis", "Flower Availability"]
    sub_selection = st.selectbox("Select Graph Category", graph_subcategories)

    if sub_selection == "Environmental Factors":
        environmental_factors.app()
    elif sub_selection == "Hive Metrics":
        hive_metrics.app()
    elif sub_selection == "Resource Analysis":
        resource_analysis.app()
    elif sub_selection == "Flower Availability":
        flower_availability.app()