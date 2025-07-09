from gtts import gTTS
from pydub import AudioSegment
import os
import platform
import subprocess
from dotenv import load_dotenv

load_dotenv()

def text_to_speech_with_gtts(input_text, output_filepath="output.mp3"):
    try:
        if not input_text.strip():
            raise ValueError("Text to speak is empty.")
        tts = gTTS(text=input_text, lang="en", slow=False)
        tts.save(output_filepath)
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return

   

    # Step 2: Convert MP3 to WAV (required for playback on Windows)
    wav_filepath = output_filepath.replace(".mp3", ".wav")
    try:
        sound = AudioSegment.from_mp3(output_filepath)
        sound.export(wav_filepath, format="wav")
    except Exception as e:
        print(f"Error converting to WAV: {e}")
        return

    # Step 3: Play the audio depending on the OS
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])
        else:
            print("Unsupported OS, cannot play audio automatically.")
    except Exception as e:
        print(f"Audio playback error: {e}")

# 🔊 Example usage
if __name__ == "__main__":
    text_to_speech_with_gtts("Hello Prachi! This is your AI voice from gTTS.")
