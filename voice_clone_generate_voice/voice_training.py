import streamlit as st
import os
from elevenlabs.client import ElevenLabs

# Initialize ElevenLabs client
API_KEY = "sk_54bb120d056452299fd2f6aa61cb6cdd5a115d8e16a02485"
client = ElevenLabs(api_key=API_KEY)

# Create an audio directory if not present
AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Function to upload multiple files
def handle_file_upload():
    uploaded_files = st.file_uploader("Upload Audio Files (Multiple Allowed)", type=["mp3", "wav"], accept_multiple_files=True)
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
        if st.button("Train Voice"):
            try:
                # Train the voice by uploading the files
                voice = train_voice(name, description, file_paths)
                st.success(f"Voice '{name}' successfully trained!")
                
                # Generate audio with the newly trained voice for demonstration
                audio_generator = client.generate(text="This is the newly trained voice!", voice=voice)

                # Save the generated audio
                output_directory = "generated_audio"
                os.makedirs(output_directory, exist_ok=True)
                output_file_path = os.path.join(output_directory, f"{name}_generated.mp3")

                # Write audio to file
                with open(output_file_path, 'wb') as f:
                    for chunk in audio_generator:
                        f.write(chunk)

                # Show the generated audio file
                st.write(f"Generated Audio with Cloned Voice:")
                st.audio(output_file_path, format="audio/mp3")
                st.success(f"Generated audio saved as {output_file_path}")
            except Exception as e:
                st.error(f"Error in training the voice: {str(e)}")
    else:
        st.warning("Please fill out the name, description, and upload at least one audio file.")
