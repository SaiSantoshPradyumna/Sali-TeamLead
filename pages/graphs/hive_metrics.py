# pages/graphs/hive_metrics.py

import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.subheader("Hive Metrics")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Ventilation: Bee Fanning")
        if "bee_fanning_df" not in st.session_state:
            st.session_state.bee_fanning_df = pd.DataFrame(columns=["Time", "Bee Fanning Intensity"])
        bee_fanning_df = st.data_editor(st.session_state.bee_fanning_df, num_rows="dynamic")
        st.session_state.bee_fanning_df = bee_fanning_df

        try:
            bee_fanning_df["Time"] = pd.to_datetime(bee_fanning_df["Time"])
            fig3 = px.bar(bee_fanning_df, x="Time", y="Bee Fanning Intensity", title="Bee Fanning Intensity Over Time")
            st.plotly_chart(fig3)
        except Exception as e:
            st.error(f"Error plotting graph: {e}")

        st.write("### Hive Placement")
        if "hive_df" not in st.session_state:
            st.session_state.hive_df = pd.DataFrame(columns=["Hive Location", "Honey Yield (kg)", "Colony Health"])
        hive_df = st.data_editor(st.session_state.hive_df, num_rows="dynamic")
        st.session_state.hive_df = hive_df

        try:
            fig4 = px.scatter(hive_df, x="Hive Location", y="Honey Yield (kg)", size="Colony Health",
                              title="Hive Placement and Productivity", labels={"size": "Health Score"})
            st.plotly_chart(fig4)
        except Exception as e:
            st.error(f"Error plotting graph: {e}")

    with col2:
        st.write("### Hive Weight")
        if "weight_df" not in st.session_state:
            st.session_state.weight_df = pd.DataFrame(columns=["Time", "Hive Weight (kg)"])
        weight_df = st.data_editor(st.session_state.weight_df, num_rows="dynamic")
        st.session_state.weight_df = weight_df

        try:
            weight_df["Time"] = pd.to_datetime(weight_df["Time"])
            fig5 = px.line(weight_df, x="Time", y="Hive Weight (kg)", title="Hive Weight Over Time")
            st.plotly_chart(fig5)
        except Exception as e:
            st.error(f"Error plotting graph: {e}")

        st.write("### Brood Development")
        if "brood_df" not in st.session_state:
            st.session_state.brood_df = pd.DataFrame(columns=["Time", "Eggs", "Larvae", "Pupae"])
        brood_df = st.data_editor(st.session_state.brood_df, num_rows="dynamic")
        st.session_state.brood_df = brood_df

        try:
            brood_df["Time"] = pd.to_datetime(brood_df["Time"])
            fig6 = px.area(brood_df, x="Time", y=["Eggs", "Larvae", "Pupae"],
                           labels={"value": "Count", "variable": "Brood Type"},
                           title="Brood Development Trends")
            st.plotly_chart(fig6)
        except Exception as e:
            st.error(f"Error plotting graph: {e}")