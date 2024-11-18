import streamlit as st
from voice_training import show_voice_training_page
from voice_cloning import show_voice_cloning_page
from tts_generation import show_tts_generation_page

# Function to handle login
def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username == "your_username" and password == "your_password":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")
    
    # Check if session state is set before rendering
    if "logged_in" in st.session_state and st.session_state.logged_in:
        st.experimental_rerun()  # Force a rerun to reflect the change in session state

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully!")

# Check if the user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.title("Login Page")
    login()
else:
    # If the user is logged in, show the app
    st.title(f"Welcome {st.session_state.username}")
    
    # Sidebar for page navigation
    st.sidebar.title("Voice Changer App")
    page = st.sidebar.radio("Choose a page", ["Voice Training", "Voice Cloning", "TTS Generation", "Logout"])

    # Route to selected page
    if page == "Voice Training":
        show_voice_training_page()
    elif page == "Voice Cloning":
        show_voice_cloning_page()
    elif page == "TTS Generation":
        show_tts_generation_page()
    elif page == "Logout":
        logout()
