import my_demo as st
from elevenlabs import ElevenLabs, VoiceSettings
from io import BytesIO

# Initialize the ElevenLabs client with your API key
client = ElevenLabs(api_key="sk_54bb120d056452299fd2f6aa61cb6cdd5a115d8e16a02485")

# Display logo and caption
#st.image(image='./LOGO-eleven-labs.png', caption="Model supports multiple languages, including English, German, Polish, Spanish, Italian, French, Portuguese, and Hindi.")

# Sidebar configuration for API key and language selection
with st.sidebar:
    with st.expander(label="ElevenLabs", expanded=False):
        st.caption("The basic API has a limited number of characters. To increase this limit, you can get a free API key from [ElevenLabs](https://beta.elevenlabs.io/subscription)")
        API_KEY = st.text_input(label="API KEY")

    st.title("Text to Voice")
    language = st.radio(label="Choose your language", options=['English', 'Multilingual'], index=0, horizontal=True)

    value = "I am the machine." if language == 'English' else "बस बातें अपने जैसे करते है"
    text = st.text_area(label="Enter the text here", value=value, max_chars=100 if not API_KEY else None)

    # Voice selection - manually specify available voices
    voices = [
        {"name": "English Voice 1", "id": "pMsXgVXv3BLzUgSXRplE"},
        {"name": "Ruhaan - Clean Indian English narration voice", "id": "siw1N9V8LmYeEWKyWBxv"},
        {"name": "Ruhaan - Clean Hindi Narration Voice", "id": "zs7UfyHqCCmny7uTxCYi"},
        {"name": "Niraj - Hindi Narrator", "id":"zgqefOY5FPQ3bB7OZTVR"},
        {"name": "Leena", "id": "ytlIxo3WdVHfMIO47oaO"},
        {"name": "Leena_voice2", "id": "tWY5Ru3Y5XXnXacAGZYH"}
    ]

    voice = st.selectbox(label="Choose the voice", options=[v['name'] for v in voices])

    st.divider()

# Trigger for generating speech
if st.button("🔈 Generate Speech"):
    try:
        # Find the voice ID based on user selection
        selected_voice_id = next(v['id'] for v in voices if v['name'] == voice)

        # Set voice settings and streaming parameters
        voice_settings = VoiceSettings(stability=0.1, similarity_boost=0.3, style=0.2)

        # Convert text to speech and get the audio stream (generator)
        audio_stream = client.text_to_speech.convert_as_stream(
            voice_id=selected_voice_id,
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

        # Play the generated audio stream in Streamlit
        st.audio(audio_bytes)

    except Exception as e:
        st.exception(e)

else:
    st.write('Input the text and click Generate')
