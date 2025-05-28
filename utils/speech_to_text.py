import speech_recognition as sr
from pydub import AudioSegment
import os
import uuid

def convert_speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    os.makedirs("temp", exist_ok=True)

    temp_input_path = f"temp/{uuid.uuid4()}.webm"
    audio_file.save(temp_input_path)

    temp_output_path = temp_input_path.replace(".webm", ".wav")
    AudioSegment.from_file(temp_input_path).export(temp_output_path, format="wav")

    try:
        with sr.AudioFile(temp_output_path) as source:
            audio_data = recognizer.record(source)

            # Attempt transcription
            try:
                text = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                text = "Sorry, I couldn't understand the audio."
            except sr.RequestError:
                text = "Sorry, speech service is unavailable."
    except Exception as e:
        text = f"An error occurred while processing audio: {str(e)}"

    # Always clean up temp files
    try:
        os.remove(temp_input_path)
        os.remove(temp_output_path)
    except FileNotFoundError:
        pass  # Already deleted or never created

    return text
