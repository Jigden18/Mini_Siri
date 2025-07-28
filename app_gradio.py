import gradio as gr
import os
import uuid
import sys
import requests
import google.generativeai as genai

from utils.speech_to_text import convert_speech_to_text
from utils.text_to_speech import convert_text_to_speech

# Ensure path for utils is correct
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

# API keys
WEATHER_API_KEY = "744717bc2bb94389aba54948252605"
GEMINI_API_KEY = "AIzaSyBTwT0zPMxd1HookkXlrBU1qo0yOb7Zro4"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

def get_weather_and_time(location):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
        response = requests.get(url)
        if response.status_code != 200:
            return f"Sorry, I couldn't find weather info for {location}."
        data = response.json()
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        city = data["location"]["name"]
        local_time = data["location"]["localtime"].split(" ")[1]
        return f"It's {temp}°C with {condition} in {city}. The local time there is {local_time}."
    except Exception as e:
        return f"Sorry, I couldn't fetch weather/time information for {location}."

def search_google(query):
    search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    return f"I didn't have a built-in answer, but you can check this: {search_url}"

def handle_open_browser(user_text):
    lower_text = user_text.lower()
    predefined_sites = {
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "google": "https://www.google.com",
        "chatgpt": "https://chat.openai.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://twitter.com",
        "gmail": "https://mail.google.com",
        "github": "https://github.com"
    }

    for keyword, url in predefined_sites.items():
        if f"open {keyword}" in lower_text:
            return f"__OPEN_BROWSER__{url}"

    if "open" in lower_text:
        app_name = lower_text.split("open", 1)[-1].strip()
        if app_name:
            search_url = f"https://www.google.com/search?q={requests.utils.quote(app_name)}"
            return f"__OPEN_BROWSER__{search_url}"

    return None

def generate_response(user_text):
    lower_text = user_text.lower()

    if "hello" in lower_text:
        return "Hi! How can I help you today?"
    elif "your name" in lower_text:
        return "I'm your virtual assistant, Mini Siri!"

    browser_response = handle_open_browser(user_text)
    if browser_response:
        return browser_response

    elif "weather in" in lower_text or "time in" in lower_text:
        location_start = lower_text.find("in") + 2
        location = user_text[location_start:].strip()
        return get_weather_and_time(location)

    elif "weather" in lower_text or "time" in lower_text:
        return "Please specify a location like 'weather in London' or 'time in Tokyo'."

    else:
        try:
            response = model.generate_content(user_text)
            return response.text.strip() if response.text.strip() else search_google(user_text)
        except Exception:
            return search_google(user_text)

def mini_siri(audio):
    if audio is None:
        return "No audio received", None

    text = convert_speech_to_text(audio)
    reply = generate_response(text)
    audio_reply_path = convert_text_to_speech(reply)

    return reply, audio_reply_path

demo = gr.Interface(
    fn=mini_siri,
    inputs=gr.Audio(source="microphone", type="filepath", label="Speak here"),
    outputs=[
        gr.Textbox(label="Assistant Response"),
        gr.Audio(label="Reply Audio")
    ],
    title="Mini Siri",
    description="Speak to the mic. It will transcribe your voice, respond with Gemini AI, and play back the response."
)

if __name__ == "__main__":
    demo.launch()
