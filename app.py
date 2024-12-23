import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pymongo import MongoClient
import hashlib
import os

# MongoDB Atlas configuration

client = MongoClient(os.getenv('MONGO_URI'))
db = client["streamlit_auth"]
users_collection = db["users"]

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return user
    return None

def create_user(username, password):
    hashed_password = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_password})

# Pages
def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

    if "page" not in st.session_state:
        st.session_state.page = "Sign In"

    if st.session_state.page == "Sign In":
        signin_page()
    elif st.session_state.page == "Sign Up":
        signup_page()
    elif st.session_state.page == "Home":
        home_page()

def signin_page():
    st.title("🐝 Bee Keeper's Portal")
    
    with st.container():
        st.markdown("""
        ### Welcome to the Honey Bee Management System
        Please login to access your hive management dashboard.
        """)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sign In"):
                user = authenticate(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.page = "Home"
                else:
                    st.error("Invalid username or password.")
        with col2:
            if st.button("Go to Sign Up"):
                st.session_state.page = "Sign Up"

def signup_page():
    st.title("Sign Up")
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    
    if st.button("Sign Up"):
        if users_collection.find_one({"username": new_username}):
            st.error("Username already exists!")
        else:
            create_user(new_username, new_password)
            st.success("Sign up successful! Redirecting to Sign In page...")
            st.session_state.page = "Sign In"

    if st.button("Go to Sign In"):
        st.session_state.page = "Sign In"

def home_page():
    st.title("Home")
    if st.session_state.authenticated:
        st.success(f"Welcome, {st.session_state.username}!")
    
        # Streamlit layout
        st.title("Hive Data Analysis Dashboard")

        # Tabs for categorized visualization
        tab1, tab2, tab3, tab4 = st.tabs(["Environmental Factors", "Hive Metrics", "Resource Analysis", "Flower Availability"])

        # Environmental Factors
        with tab1:
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

        # Hive Metrics
        with tab2:
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

        # Resource Analysis
        with tab3:
            st.subheader("Resource Analysis")
            st.write("### Foraging Resources")
            if "foraging_df" not in st.session_state:
                st.session_state.foraging_df = pd.DataFrame(columns=["Days", "Pollen", "Nectar", "Other Resources"])
            foraging_df = st.data_editor(st.session_state.foraging_df, num_rows="dynamic")
            st.session_state.foraging_df = foraging_df

            try:
                foraging_df["Days"] = pd.to_datetime(foraging_df["Days"])
                fig7 = px.bar(foraging_df, x="Days", y=["Pollen", "Nectar", "Other Resources"],
                            labels={"value": "Quantity", "variable": "Resource Type"},
                            title="Foraging Resources Over Time", barmode="stack")
                st.plotly_chart(fig7)
            except Exception as e:
                st.error(f"Error plotting graph: {e}")

        # Flower Availability
        with tab4:
            st.subheader("Flower Availability")
            if "flower_df" not in st.session_state:
                st.session_state.flower_df = pd.DataFrame(columns=["Weeks", "Nectar-rich Flowers", 
                                        "Pollen-rich Flowers", "Other Flowers"])
            flower_df = st.data_editor(st.session_state.flower_df, num_rows="dynamic")
            st.session_state.flower_df = flower_df

            try:
                flower_df["Weeks"] = pd.to_datetime(flower_df["Weeks"])
                fig8 = px.bar(flower_df, x="Weeks", y=["Nectar-rich Flowers", "Pollen-rich Flowers", "Other Flowers"],
                            labels={"value": "Number of Flowers", "variable": "Flower Type"},
                            title="Flower Availability by Type Over Time", barmode="stack")
                st.plotly_chart(fig8)
            except Exception as e:
                st.error(f"Error plotting graph: {e}")

        if st.button("Sign Out"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.page = "Sign In"
    else:
        st.error("Unauthorized access. Redirecting to Sign In...")
        st.session_state.page = "Sign In"

if __name__ == "__main__":
    main()