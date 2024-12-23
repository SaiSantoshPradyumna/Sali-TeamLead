import streamlit as st
from streamlit_option_menu import option_menu
from pymongo import MongoClient
import hashlib
import os
from PIL import Image

# Import page modules
from pages import dashboard
from pages import predictive_analysis
from pages import report_download
from pages import weather
from pages import settings
from pages import support
from pages.graphs import graphs_main
MONGO_URI = "mongodb+srv://saisantoshpradyumna:Vid3Ohz1gdVkA6IL@cluster0.r6xfa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
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

# Main function
def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

    if "page" not in st.session_state:
        st.session_state.page = "Sign In"

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

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
                    st.session_state.current_page = "Dashboard"
                    st.experimental_rerun()
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
            st.experimental_rerun()

    if st.button("Go to Sign In"):
        st.session_state.page = "Sign In"

def home_page():
    if st.session_state.authenticated:
        # Sidebar navigation
        with st.sidebar:
            st.title("Navigation")
            menu_options = ["Dashboard", "Predictive Analysis", "Report Download", "Weather", "Graphs", "Settings", "Support"]
            selection = option_menu(
                menu_title="Main Menu",
                options=menu_options,
                icons=["grid", "graph-up", "download", "cloud-sun", "bar-chart", "gear", "envelope"],
                menu_icon="cast",
                default_index=menu_options.index(st.session_state.current_page),
            )
            st.session_state.current_page = selection

        # Top bar with username and sign out button
        with st.container():
            col1, col2, col3 = st.columns([0.5, 8, 1])
            with col1:
                # Display profile picture if exists
                profile_pic_path = f"profile_pics/{st.session_state.username}.jpg"
                if os.path.exists(profile_pic_path):
                    st.image(profile_pic_path, width=40)
                else:
                    st.image("default_profile_pic.jpg", width=40)
            with col2:
                pass  # Empty
            with col3:
                st.write(f"**{st.session_state.username}**")
                if st.button("Sign Out"):
                    st.session_state.authenticated = False
                    st.session_state.username = None
                    st.session_state.page = "Sign In"
                    st.session_state.current_page = None
                    st.experimental_rerun()

        # Display the selected page
        if st.session_state.current_page == "Dashboard":
            dashboard.app()
        elif st.session_state.current_page == "Predictive Analysis":
            predictive_analysis.app()
        elif st.session_state.current_page == "Report Download":
            report_download.app()
        elif st.session_state.current_page == "Weather":
            weather.app()
        elif st.session_state.current_page == "Graphs":
            graphs_main.app()
        elif st.session_state.current_page == "Settings":
            settings.app(users_collection)
        elif st.session_state.current_page == "Support":
            support.app()

    else:
        st.error("Unauthorized access. Redirecting to Sign In...")
        st.session_state.page = "Sign In"

if __name__ == "__main__":
    main()