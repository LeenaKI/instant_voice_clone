import streamlit as st
from voice_training import show_voice_training_page
from voice_cloning import show_voice_cloning_page
from tts_generation import show_tts_generation_page

# Sidebar for page navigation
st.sidebar.title("Voice Changer App")
page = st.sidebar.radio("Choose a page", ["Voice Training", "Voice Cloning", "TTS Generation"])

USERNAME = "apprikart"
PASSWORD = "123" 

# Initialize session state for authentication and uploaded files
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

# Function to check authentication
def check_authentication(username, password):
    return username == USERNAME and password == PASSWORD

# Login function
def login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_authentication(username, password):
            st.session_state['authenticated'] = True
            st.success("Login successful!please click on login button again")
        else:
            st.error("Invalid username or password")

# Logout function
def logout():
    st.session_state['authenticated'] = False
    st.success("You have been logged out! please click on logout button again.")

# Route to selected page
if page == "Voice Training":
    show_voice_training_page()
elif page == "Voice Cloning":
    show_voice_cloning_page()
elif page == "TTS Generation":
    show_tts_generation_page()

    st.markdown("---")
    if st.button("Logout"):
        logout()

# Authentication flow
if not st.session_state['authenticated']:
    login()
else:
    main_app()
