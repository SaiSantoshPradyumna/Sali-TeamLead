# pages/settings.py

import streamlit as st
from PIL import Image
import os
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def app(users_collection):
    st.title("Settings")
    st.subheader("User Settings")

    # Show current username and allow changing it
    st.write(f"**Current Username:** {st.session_state.username}")
    change_username = st.checkbox("Change Username")
    if change_username:
        new_username = st.text_input("New Username")
        if st.button("Update Username"):
            if users_collection.find_one({"username": new_username}):
                st.error("Username already exists!")
            else:
                # Update the username in the database
                users_collection.update_one({"username": st.session_state.username},
                                            {"$set": {"username": new_username}})
                st.success("Username updated successfully!")
                st.session_state.username = new_username
                st.experimental_rerun()

    # Allow changing password
    st.write("**Change Password**")
    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_new_password = st.text_input("Confirm New Password", type="password")
    if st.button("Update Password"):
        # Authenticate current password
        user = users_collection.find_one({"username": st.session_state.username})
        if user and user["password"] == hash_password(current_password):
            if new_password == confirm_new_password:
                hashed_password = hash_password(new_password)
                users_collection.update_one({"username": st.session_state.username},
                                            {"$set": {"password": hashed_password}})
                st.success("Password updated successfully!")
            else:
                st.error("New passwords do not match!")
        else:
            st.error("Current password is incorrect!")

    # Allow uploading profile picture
    st.write("**Profile Picture**")
    profile_pic = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])
    if profile_pic:
        # Save the profile picture to a directory
        if not os.path.exists("profile_pics"):
            os.makedirs("profile_pics")
        img = Image.open(profile_pic)
        img = img.convert("RGB")
        profile_pic_path = f"profile_pics/{st.session_state.username}.jpg"
        img.save(profile_pic_path)
        st.success("Profile picture updated!")
        st.image(img, caption="Profile Picture")