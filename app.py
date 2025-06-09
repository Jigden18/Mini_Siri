import sys
import os

# Ensure path correctness if running from a different directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from datetime import datetime
from utils.speech_to_text import convert_speech_to_text
from utils.text_to_speech import convert_text_to_speech
import google.generativeai as genai
import requests

# WeatherAPI.com API Key (replace this with your actual key)
WEATHER_API_KEY = "744717bc2bb94389aba54948252605"

# GEMINI API Key(Replace with your actual key)
GEMINI_API_KEY = "AIzaSyBTwT0zPMxd1HookkXlrBU1qo0yOb7Zro4"  
genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini 1.5 Flash for fast assistant-like performance
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

# check for available models and switch as per need 
# models = genai.list_models()
# for m in models:
#     print(m.name)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Function to fetch weather and local time using WeatherAPI
def get_weather_and_time(location):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
        print("Fetching weather for:", location)
        print("API URL:", url)

        response = requests.get(url)

        if response.status_code != 200:
            print("WeatherAPI error:", response.text)
            return f"Sorry, I couldn't find weather info for {location}."

        data = response.json()

        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        city = data["location"]["name"]
        local_time = data["location"]["localtime"].split(" ")[1]

        return f"It's {temp}°C with {condition} in {city}. The local time there is {local_time}."

    except Exception as e:
        print("Weather/time fetch error:", e)
        return f"Sorry, I couldn't fetch weather/time information for {location}."
    
# Function to make google request
def search_google(query):
    search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    return f"I didn't have a built-in answer, but you can check this: {search_url}"

# Function to open hardcoded browser tabs
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

    # Generic fallback using Google search
    if "open" in lower_text:
        app_name = lower_text.split("open", 1)[-1].strip()
        if app_name:
            search_url = f"https://www.google.com/search?q={requests.utils.quote(app_name)}"
            return f"__OPEN_BROWSER__{search_url}"

    return None  # No browser command detected

# Function to generate assistant response based on user input
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
        # Use Gemini AI for smart responses
        try:
            response = model.generate_content(user_text)
            if response.text.strip():
                return response.text.strip()
            else:
                return search_google(user_text)
        except Exception as e:
            print("Gemini error:", e)
            return search_google(user_text)

# Endpoint to handle speech-to-text conversion
@app.route("/stt", methods=["POST"])
def stt():
    if "file" not in request.files:
        return jsonify({"text": "No audio file received."}), 400

    audio = request.files["file"]
    text = convert_speech_to_text(audio)

    print("User said:", text)
    return jsonify({"text": text})

# Endpoint to handle text-to-speech conversion and response generation
@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    user_input = data.get("text", "").strip()

    if not user_input:
        return jsonify({"reply": "No input provided", "audio_path": ""}), 400

    reply_text = generate_response(user_input)
    print("Response:", reply_text)

    audio_path = convert_text_to_speech(reply_text)
    return jsonify({
        "reply": reply_text,
        "audio_path": f"/temp/{os.path.basename(audio_path)}"
    })

# Endpoint to serve generated audio files
@app.route("/temp/<filename>")
def serve_audio(filename):
    return send_from_directory("temp", filename)

# Endpoint to serve the frontend
@app.route("/")
def home():
    return render_template("index.html")

# Start the Flask development server
if __name__ == "__main__":
    app.run(debug=True)
