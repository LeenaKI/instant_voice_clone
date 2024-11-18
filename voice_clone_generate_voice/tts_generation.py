import streamlit as st
import requests
from io import BytesIO

API_KEY = "sk_54bb120d056452299fd2f6aa61cb6cdd5a115d8e16a02485"

# List of default voices to hide
default_voices_to_hide = [
    "Charlotte", "Aria", "Roger", "Sarah", "Laura", "Charlie", "George", 
    "Callum", "River", "Liam", "Lily", "Bill", "Alice", "Matilda", "Will", "Ruhaan - Clean Hindi Narration Voice",
    "Jessica", "Eric", "Chris", "Brian", "Daniel", "Daniel", "Ruhaan - Clean narration voice", "Niraj - Hindi Narrator", "Niraj - Hindi Narrator"
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

# Function to generate TTS using the voice ID
def generate_tts(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    headers = {"xi-api-key": API_KEY}
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        st.error("Failed to generate TTS")
        return None

# Streamlit page function
def show_tts_generation_page():
    st.title("Text-to-Speech (TTS) Generation")
    st.write("Enter text to generate speech using the selected voice.")

    # Fetch available voices from Eleven Labs API
    voices_map = get_available_voices()

    if voices_map:
        # Filter out the default voices to hide
        filtered_voices = {name: id for name, id in voices_map.items() if name not in default_voices_to_hide}
        
        # Display the voices in a dropdown for selection, excluding the default ones
        if filtered_voices:
            voice_name = st.selectbox("Select voice for TTS", options=list(filtered_voices.keys()))
            voice_id = filtered_voices[voice_name]

            text = st.text_area("Enter text for TTS:")

            if st.button("Generate TTS"):
                audio_bytes = generate_tts(text, voice_id)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                    st.success("TTS generated successfully!")
        else:
            st.warning("No valid voices available to choose from.")
    else:
        st.warning("No voices available to choose from.")
