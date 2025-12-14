import streamlit as st
from db_manager import DatabaseManager
from auth import verify_password, hash_password

# Learned from Streamlit Part 2: Setup page config
st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

# Initialize Database Manager
db = DatabaseManager()

# --- INITIALISE SESSION STATE ---
# Learned from Lecture: "We store data in st.session_state so it persists across reruns"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🛡️ Multi-Domain Intelligence Platform (Web Interface)")

# If already logged in, show success and button to dashboard
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"):
        # Learned from Lecture: Programmatic navigation
        st.switch_page("pages/1_Dashboard.py")
    st.stop()  # Stop rendering the rest of the page

# --- TABS: LOGIN / REGISTER ---
# Learned from Lecture: "We use tabs to toggle between Login and Register"
tab_login, tab_register = st.tabs(["Login", "Register"])

# ----- LOGIN TAB -----
with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_user")
    login_password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Log in", type="primary"):
        # Real Database Check (Upgrading from the lecture's dictionary example)
        user_record = db.find_user(login_username)

        if user_record:
            stored_hash = user_record[2]  # Index 2 is the hash

            if verify_password(login_password, stored_hash):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.success(f"Welcome back, {login_username}! 🎉")
                # Redirect to dashboard
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Invalid password.")
        else:
            st.error("User not found.")

# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username", key="reg_user")
    new_password = st.text_input("Choose a password", type="password", key="reg_pass")
    confirm_password = st.text_input("Confirm password", type="password", key="reg_confirm")

    if st.button("Create account"):
        # Basic validation logic from Lecture
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif db.find_user(new_username):
            st.error("Username already exists.")
        else:
            # Hash and Save to SQLite
            hashed_pw = hash_password(new_password)
            if db.add_user(new_username, hashed_pw):
                st.success("Account created! Go to the Login tab to sign in.")
            else:
                st.error("Database error.")
