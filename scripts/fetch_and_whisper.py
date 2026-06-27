import requests
import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
BRONTO_API_KEY = os.getenv("BRONTO_API_KEY")

def get_latest_error_from_bronto():
    """
    Simulates fetching the latest error log from Bronto API.
    In a fully live setup, this would be a GET request to Bronto's query API.
    """
    # For demo purposes, we will return a simulated error string that sounds good when spoken
    print("Fetching logs from Bronto...")
    return "Warning: The payment processing microservice has crashed for user Jane Doe due to a database deadlock. I have logged the trace in Bronto."

def generate_and_play_audio(text):
    if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "your_elevenlabs_api_key_here":
        print("Error: ElevenLabs API Key is missing. Please set it in the .env file.")
        sys.exit(1)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    print("Synthesizing voice via ElevenLabs...")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        mp3_path = os.path.abspath("alert.mp3")
        with open(mp3_path, "wb") as f:
            f.write(response.content)
        print(f"Audio saved to {mp3_path}")
        
        # WSL Audio Hack: Play the audio via Windows PowerShell to ensure it uses the host speakers
        print("Playing audio on host speakers...")
        # We need to convert the WSL path to a Windows path for PowerShell
        # Using wslpath tool
        try:
            win_path = subprocess.check_output(['wslpath', '-w', mp3_path]).decode().strip()
            ps_command = f"Add-Type -AssemblyName PresentationCore; $player = New-Object System.Windows.Media.MediaPlayer; $player.Open('{win_path}'); $player.Play(); Start-Sleep -s 10"
            subprocess.run(["powershell.exe", "-c", ps_command])
        except Exception as e:
            print(f"Failed to play audio via PowerShell: {e}")
    else:
        print(f"ElevenLabs Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    error_text = get_latest_error_from_bronto()
    print(f"Latest Error: {error_text}")
    generate_and_play_audio(error_text)
