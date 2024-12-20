import streamlit as st
import os
from elevenlabs.client import ElevenLabs

# Initialize ElevenLabs client
API_KEY = "sk_54bb120d056452299fd2f6aa61cb6cdd5a115d8e16a02485"
client = ElevenLabs(api_key=API_KEY)

# Create directories for audio
AUDIO_DIR = "audio_files"
GENERATED_AUDIO_DIR = "generated_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(GENERATED_AUDIO_DIR, exist_ok=True)

# Function to upload multiple files
def handle_file_upload():
    uploaded_files = st.file_uploader("Upload Audio Files for training voice(Multiple Allowed)", type=["mp3", "wav"], accept_multiple_files=True)
    if uploaded_files:
        file_paths = []
        for file in uploaded_files:
            file_path = os.path.join(AUDIO_DIR, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            file_paths.append(file_path)
        return uploaded_files, file_paths
    else:
        return [], []

# Function to clone the voice using Eleven Labs API
def train_voice(name, description, files):
    voice = client.clone(name=name, description=description, files=files)
    return voice

# Streamlit page function
def show_voice_training_page():
    st.title("Voice Training")
    st.write("Train a custom voice using your audio files.")

    # Language selection
    language = st.radio("Choose Language:", options=["English", "Hindi"])

    # User inputs for voice name and description
    name = st.text_input("Enter the voice name:")
    description = st.text_area("Enter a description for the voice:")

    # Handle file uploads
    uploaded_files, file_paths = handle_file_upload()

    # Display uploaded audio files for the user to play
    if uploaded_files:
        st.write("Uploaded Audio Files:")
        for uploaded_file in uploaded_files:
            st.audio(uploaded_file, format="audio/mp3")

    # If files are uploaded and fields are filled
    if name and description and uploaded_files:
        user_text = st.text_area(f"Enter text in {language}:")
        if st.button("Train Voice and Generate Audio"):
            try:
                # Train the voice by uploading the files
                voice = train_voice(name, description, file_paths)
                st.success(f"Voice '{name}' successfully trained!")

                if user_text.strip():
                    # Generate audio with the newly trained voice
                    audio_generator = client.generate(text=user_text, voice=voice)

                    # Save the generated audio
                    output_file_path = os.path.join(GENERATED_AUDIO_DIR, f"{name}_generated.mp3")
                    with open(output_file_path, 'wb') as f:
                        for chunk in audio_generator:
                            f.write(chunk)

                    # Show the generated audio file
                    st.write("Generated Audio with Cloned Voice:")
                    st.audio(output_file_path, format="audio/mp3")
                    st.success(f"Generated audio saved as {output_file_path}")
                else:
                    st.error("Please enter text for audio generation.")
            except Exception as e:
                st.error(f"Error in training the voice or generating audio: {str(e)}")
    else:
        st.warning("Please fill out the name, description, and upload at least one audio file.")

# Show the page
show_voice_training_page()
