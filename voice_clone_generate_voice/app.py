import streamlit as st

# Dummy credentials for demonstration
USERNAME = "apprikart"
PASSWORD = "123"

# Initialize session states for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Login"

# Function to display the login page
def show_login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["authenticated"] = True
            st.session_state["active_page"] = "Main"
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Function to display the logout button
def show_logout_button():
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["active_page"] = "Login"
        st.experimental_rerun()

# Import pages (dummy functions for demonstration)
def show_voice_training_page():
    st.title("Voice Training Page")
    st.write("Content for Voice Training goes here.")

def show_voice_cloning_page():
    st.title("Voice Cloning Page")
    st.write("Content for Voice Cloning goes here.")

def show_tts_generation_page():
    st.title("TTS Generation Page")
    st.write("Content for TTS Generation goes here.")

# Route based on authentication state
if not st.session_state["authenticated"]:
    show_login_page()
else:
    # Sidebar navigation
    st.sidebar.title("Voice Changer App")
    show_logout_button()  # Add logout button to the sidebar
    page = st.sidebar.radio("Choose a page", ["Voice Training", "Voice Cloning", "TTS Generation"])

    # Route to selected page
    if page == "Voice Training":
        show_voice_training_page()
    elif page == "Voice Cloning":
        show_voice_cloning_page()
    elif page == "TTS Generation":
        show_tts_generation_page()
