import streamlit as st
from elevenlabs import ElevenLabs, VoiceSettings
from io import BytesIO

# Initialize the ElevenLabs client with your API key
client = ElevenLabs(api_key="")

# Function for generating speech
def generate_speech(text, voice_id):
    try:
        # Set voice settings and streaming parameters
        voice_settings = VoiceSettings(stability=0.1, similarity_boost=0.3, style=0.2)

        # Convert text to speech and get the audio stream (generator)
        audio_stream = client.text_to_speech.convert_as_stream(
            voice_id=voice_id,
            optimize_streaming_latency="0",  # optimize for lower latency
            output_format="mp3_22050_32",  # output format: 22050 Hz, 32 kbps
            text=text,
            voice_settings=voice_settings
        )

        # Read the generated audio stream into a BytesIO object
        audio_bytes = BytesIO()
        for chunk in audio_stream:
            audio_bytes.write(chunk)
        audio_bytes.seek(0)  # Rewind the BytesIO object to the start

        return audio_bytes

    except Exception as e:
        st.exception(e)
        return None

# Sidebar configuration
with st.sidebar:
    st.title("Text to Voice")
    # Add page selection
    page = st.radio("Choose a Landing Page", options=["Clone voice", "Audio Generation"], index=0)

# Page 1 Content
if page == "Clone voice":
    st.header("Text to Speech")
    st.caption("Choose a voice and enter text to convert it to speech.")
    
    # Sidebar content for Page 1
    API_KEY = st.text_input(label="API KEY for ElevenLabs", placeholder="Enter your API key")

    language = st.radio(label="Choose your language", options=['English', 'Multilingual'], index=0, horizontal=True)
    value = "I am the machine." if language == 'English' else "बस बातें अपने जैसे करते है"
    text = st.text_area(label="Enter the text here", value=value, max_chars=100 if not API_KEY else None)

    voices = [
        {"name": "English Voice 1", "id": "pMsXgVXv3BLzUgSXRplE"},
        {"name": "Ruhaan - Clean Indian English narration voice", "id": "siw1N9V8LmYeEWKyWBxv"},
        {"name": "Ruhaan - Clean Hindi Narration Voice", "id": "zs7UfyHqCCmny7uTxCYi"},
        {"name": "Niraj - Hindi Narrator", "id":"zgqefOY5FPQ3bB7OZTVR"},
        {"name": "Leena", "id": "ytlIxo3WdVHfMIO47oaO"},
        {"name": "Leena_voice2", "id": "tWY5Ru3Y5XXnXacAGZYH"}
    ]

    voice = st.selectbox(label="Choose the voice", options=[v['name'] for v in voices])

    # Trigger for generating speech
    if st.button("🔈 Generate Speech"):
        selected_voice_id = next(v['id'] for v in voices if v['name'] == voice)
        audio_bytes = generate_speech(text, selected_voice_id)
        if audio_bytes:
            st.audio(audio_bytes)

# Page 2 Content
elif page == "Audio Generation":
    st.header("Welcome to the Multilingual Text to Speech Page")
    st.caption("Choose a language and enter text to convert it to speech.")
    
    # Sidebar content for Page 2
    API_KEY = st.text_input(label="API KEY for ElevenLabs", placeholder="Enter your API key")

    language = st.radio(label="Choose your language", options=['English', 'Multilingual'], index=1, horizontal=True)
    value = "I am the machine." if language == 'English' else "बस बातें अपने जैसे करते है"
    text = st.text_area(label="Enter the text here", value=value, max_chars=100 if not API_KEY else None)

    voices = [
        {"name": "Ruhaan - Clean Indian English narration voice", "id": "siw1N9V8LmYeEWKyWBxv"},
        {"name": "Ruhaan - Clean Hindi Narration Voice", "id": "zs7UfyHqCCmny7uTxCYi"},
        {"name": "Niraj - Hindi Narrator", "id":"zgqefOY5FPQ3bB7OZTVR"},
        {"name": "Leena", "id": "ytlIxo3WdVHfMIO47oaO"},
        {"name": "Leena_voice2", "id": "tWY5Ru3Y5XXnXacAGZYH"}
    ]

    voice = st.selectbox(label="Choose the voice", options=[v['name'] for v in voices])

    # Trigger for generating speech
    if st.button("🔈 Generate Speech"):
        selected_voice_id = next(v['id'] for v in voices if v['name'] == voice)
        audio_bytes = generate_speech(text, selected_voice_id)
        if audio_bytes:
            st.audio(audio_bytes)

else:
    st.write('Select a landing page to begin.')
