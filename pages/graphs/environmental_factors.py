# pages/graphs/environmental_factors.py

import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.subheader("Environmental Factors")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Temperature & Humidity")
        if "temp_humidity_df" not in st.session_state:
            st.session_state.temp_humidity_df = pd.DataFrame(columns=["Time", "Temperature", "Humidity"])
        temp_humidity_df = st.data_editor(st.session_state.temp_humidity_df, num_rows="dynamic")
        st.session_state.temp_humidity_df = temp_humidity_df

        try:
            temp_humidity_df["Time"] = pd.to_datetime(temp_humidity_df["Time"])
            fig1 = px.line(temp_humidity_df, x="Time", y=["Temperature", "Humidity"],
                           labels={"value": "Measurements", "variable": "Type"},
                           title="Temperature and Humidity Over Time")
            st.plotly_chart(fig1)
        except Exception as e:
            st.error(f"Error plotting graph: {e}")

    with col2:
        st.write("### Seasonal Correlation")
        if "season_df" not in st.session_state:
            st.session_state.season_df = pd.DataFrame(columns=["Temperature", "Rainfall", "Hive Health"])
        season_df = st.data_editor(st.session_state.season_df, num_rows="dynamic")
        st.session_state.season_df = season_df

        try:
            fig2 = px.scatter(season_df, x="Temperature", y="Hive Health", color="Rainfall",
                              title="Seasonal Correlation: Environmental Factors vs Hive Health")
            st.plotly_chart(fig2)
        except Exception as e:
            st.error(f"Error plotting graph: {e}")