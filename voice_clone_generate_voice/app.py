import streamlit as st
from voice_training import show_voice_training_page
from voice_cloning import show_voice_cloning_page
from tts_generation import show_tts_generation_page

# Sidebar for page navigation
st.sidebar.title("Voice Changer App")
page = st.sidebar.radio("Choose a page", ["Voice Training", "Voice Cloning", "TTS Generation"])

# Route to selected page
if page == "Voice Training":
    show_voice_training_page()
elif page == "Voice Cloning":
    show_voice_cloning_page()
elif page == "TTS Generation":
    show_tts_generation_page()
s
