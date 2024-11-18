from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os

client = ElevenLabs(
  api_key="", 
)

voice = client.clone(
    name="Shah Rukh Khan - AI_cloned",
    description="Indian actor Shah Rukh Khan's voice in Indian english accent.",  
    files=["./Shah_Rukh_Khan_denoise.mp3"],
)

# Generate the audio
audio_generator = client.generate(text="Success is not a good teacher, failure makes you humble", voice=voice)

# Define the directory and file path where you want to save the audio
output_directory = 'C:/Users/Admin/Documents/Apprikart/voice_clone_generate_voice/output_audio/'
os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

output_file_path = os.path.join(output_directory, 'Shah_Rukh_Khan_cloned_voice.mp3')

# Save the audio as an MP3 file by iterating over the generator
with open(output_file_path, 'wb') as f:
    for chunk in audio_generator:
        f.write(chunk)

print(f"Audio saved to {output_file_path}")
