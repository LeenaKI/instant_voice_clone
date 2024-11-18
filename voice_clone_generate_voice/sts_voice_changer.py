from pygame import mixer 
from pydub import AudioSegment
from termcolor import colored
import io, os, re
import time, json
import requests

# Load Eleven Labs API key from environment
API_KEY = "sk_54bb120d056452299fd2f6aa61cb6cdd5a115d8e16a02485"

# Set the directory for storing audio files
AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Clear terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()
time.sleep(1)

# Function to remove emojis from text
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Fetch available voices from Eleven Labs
def get_voices(API_KEY):
    headers = {"xi-api-key": API_KEY}
    voices_map = {}
    response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers).json()
    voices = response.get("voices", [])
    
    print(colored("Available voices:", "blue"))
    for voice in voices:
        name = remove_emojis(voice["name"]).strip()
        voices_map[name] = voice["voice_id"]
        print(colored(f"    - {name} ({voice['category']})", "light_blue"))

    return voices_map

# Get voices and prompt the user to select one
voices_map = get_voices(API_KEY)
while True:
    voice_input = input(colored("Select your voice: ", "light_green"))
    voice_id = voices_map.get(voice_input)
    if voice_id:
        break
    else:
        print(colored("Invalid voice", "red"))

# Constants for Eleven Labs API settings
ELEVENLABS_STABILITY = 0.4
ELEVENLABS_SIMILARITY_BOOST = 0.5

# Convert WAV to MP3 (if needed) and store it
def convert_audio_to_mp3(input_path, output_path):
    sound = AudioSegment.from_file(input_path)
    sound.export(output_path, format="mp3")

# Function to apply speech-to-speech transformation
def apply_speech_to_speech(wav_path):
    try:
        url = f"https://api.elevenlabs.io/v1/speech-to-speech/{voice_id}/stream"
        headers = {"xi-api-key": API_KEY}
        data = {
            "model_id": "eleven_english_sts_v2",
            "voice_settings": json.dumps({
                "stability": ELEVENLABS_STABILITY,
                "similarity_boost": ELEVENLABS_SIMILARITY_BOOST,
            }),
        }
        
        with open(wav_path, 'rb') as f:
            files = {'audio': ('audio.wav', f, 'audio/wav')}
            response = requests.post(url, headers=headers, data=data, files=files)

        # Check for error in the response
        if response.status_code != 200 or len(response.content) <= 200:
            try:
                load = json.loads(response.content)
                print(colored(f"Error: {load['detail']['message']}", "red"))
            except Exception:
                print(colored("Error processing audio.", "red"))
            return None

        # Save the generated audio as MP3
        generated_audio_path = os.path.join(AUDIO_DIR, "generated_audio.mp3")
        with open(generated_audio_path, 'wb') as f:
            f.write(response.content)

        return generated_audio_path

    except Exception as e:
        print(colored(f"Error: {str(e)}", "red"))
        return None

# Play the generated audio
def play_audio(chunk_path):
    print(colored("Playing generated audio", "green"))
    mixer.init()
    mixer.music.load(chunk_path)
    mixer.music.set_volume(1.0)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.1)

    mixer.music.stop()
    mixer.quit()

# Main function
def main():
    try:
        wav_path = input("Enter the path to the audio file you want to clone: ")

        # Check if the file exists
        if not os.path.isfile(wav_path):
            print(colored("File not found. Please check the path and try again.", "red"))
            return

        # Convert input audio to MP3 (if not already in MP3 format)
        input_audio_mp3_path = os.path.join(AUDIO_DIR, "input_audio.mp3")
        convert_audio_to_mp3(wav_path, input_audio_mp3_path)
        print(colored(f"Input audio saved as {input_audio_mp3_path}", "blue"))

        # Process the input audio with Eleven Labs
        generated_audio_path = apply_speech_to_speech(input_audio_mp3_path)
        if generated_audio_path:
            print(colored(f"Generated audio saved as {generated_audio_path}", "blue"))
            play_audio(generated_audio_path)
        else:
            print(colored("Failed to process audio for voice cloning.", "red"))

    except KeyboardInterrupt:
        print(colored("Voice changer stopped", "red"))

main()
