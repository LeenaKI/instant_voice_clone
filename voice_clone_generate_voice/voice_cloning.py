import streamlit as st
from pydub import AudioSegment
import os
import requests
import json

# Constants
API_KEY = "sk_54bb120d056452299fd2f6aa61cb6cdd5a115d8e16a02485"  # Add your Eleven Labs API Key here
AUDIO_DIR = "./audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)
stability = 0.2
similarity_boost = 0.1

# List of default voices to hide
default_voices_to_hide = [
    "Charlotte", "Aria", "Roger", "Sarah", "Laura", "Charlie", "George", 
    "Callum", "River", "Liam", "Lily", "Bill", "Alice", "Matilda", "Will", 
    "Jessica", "Eric", "Chris", "Brian", "Daniel"
]

# Function to fetch available voices from Eleven Labs API
def get_available_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": API_KEY}
    response = requests.get(url, headers=headers).json()
    
    if response and "voices" in response:
        voices = response["voices"]
        voice_options = {voice["name"]: voice["voice_id"] for voice in voices}
        return voice_options
    else:
        st.error("Failed to fetch voices from Eleven Labs")
        return {}

# Function to clone voice using Eleven Labs API
def clone_voice(mp3_path, voice_id):
    url = f"https://api.elevenlabs.io/v1/speech-to-speech/{voice_id}/stream"
    headers = {"xi-api-key": API_KEY}
    data = {
        "model_id": "eleven_english_sts_v2",
        "voice_settings": json.dumps({
            "stability": stability,
            "similarity_boost": similarity_boost,
        }),
    }
    with open(mp3_path, 'rb') as f:
        files = {'audio': ('audio.mp3', f, 'audio/mp3')}
        response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code == 200:
        output_path = os.path.join(AUDIO_DIR, "cloned_voice.mp3")
        with open(output_path, 'wb') as out_file:
            out_file.write(response.content)
        return output_path
    else:
        st.error("Failed to clone voice")
        return None

# Streamlit page function
def show_voice_cloning_page():
    st.title("Voice Cloning")
    st.write("Upload an audio file to clone a voice.")

    uploaded_file = st.file_uploader("Upload mp3 file(min. 1-2min)", type=["mp3"])
    if uploaded_file:
        # Save the uploaded file locally
        mp3_path = os.path.join(AUDIO_DIR, "input_audio.mp3")
        with open(mp3_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Display the uploaded audio for playback
        st.write("Uploaded Audio:")
        st.audio(mp3_path, format="audio/mp3")

        # Fetch available voices from Eleven Labs API
        voices_map = get_available_voices()
        
        if voices_map:
            # Filter out the default voices to hide
            filtered_voices = {name: id for name, id in voices_map.items() if name not in default_voices_to_hide}
            
            # Display the voices in a dropdown for selection, excluding the default ones
            if filtered_voices:
                voice_name = st.selectbox("Select voice for cloning(trained voice in previous step)", options=list(filtered_voices.keys()))
                voice_id = filtered_voices[voice_name]

                if st.button("Clone Voice"):
                    cloned_audio_path = clone_voice(mp3_path, voice_id)
                    if cloned_audio_path:
                        st.write("Cloned Audio:")
                        st.audio(cloned_audio_path, format="audio/mp3")
                        st.success("Voice cloned successfully!")
            else:
                st.warning("No valid voices available to choose from.")
        else:
            st.warning("No voices available to choose from.")
