from gtts import gTTS
import os
import uuid

def convert_text_to_speech(text):
    os.makedirs("temp", exist_ok=True)
    filename = f"temp_audio_{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join("temp", filename)

    try:
        tts = gTTS(text)
        tts.save(audio_path)
        return f"/temp/{filename}"  # This is the correct relative path for the frontend
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        return ""  # Return empty string if TTS fails
