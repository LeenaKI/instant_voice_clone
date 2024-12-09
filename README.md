# Instant Voice Changer App

This **Instant Voice Changer App** allows users to train custom voices, clone existing voices, and generate text-to-speech (TTS) audio using the **Eleven Labs API**. The app provides a secure login system and an intuitive interface for exploring its features.

## Features
1. **Voice Training**  
   Train a custom voice by uploading audio files and generating synthesized audio in your custom voice.
   
2. **Voice Cloning**  
   Clone an existing voice by uploading an audio file and selecting from available voice models.

3. **User Authentication**  
   Secure login system ensures that only authorized users can access the app.

## How to Use
1. Clone this repository:
   ```bash
   git clone https://github.com/LeenaKI/instant_voice_clone.git
   cd voice-changer-app
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Eleven Labs API key in the appropriate files.
4. Run the app:
   ```bash
   streamlit run app.py
   ```
5. Open the app in your browser and log in with:
   - **Username**: `leena`  
   - **Password**: `clone@20127`  

6. Use the sidebar to navigate between **Voice Training**, **Voice Cloning**, and **Logout**.

## Prerequisites
- Python 3.8 or above
- Streamlit
- Eleven Labs API Key (Sign up at [Eleven Labs](https://elevenlabs.io/app/settings/api-keys))

## File Structure
- `app.py`: Main application file with login and navigation.
- `voice_training.py`: Handles voice training functionality.
- `voice_cloning.py`: Handles voice cloning functionality.
- `requirements.txt`: Python dependencies.
