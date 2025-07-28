# Mini Siri – Your Personal Voice-Powered AI Assistant

**Mini Siri** is a virtual AI assistant that listens to your voice, understands your query using speech-to-text, responds intelligently with help from Google’s **Gemini AI**, and replies back using **text-to-speech**. It can check weather/time, open websites, or answer your questions conversationally — just like a mini version of Siri.

---

## ✨ Features

- 🎙️ Voice input with speech-to-text  
- 🧠 Smart AI responses using Gemini 1.5 Flash  
- 🌤️ Real-time weather and local time using WeatherAPI  
- 🔊 Text-to-speech replies with audio playback  
- 🌐 Auto-opens common websites like YouTube, Gmail, ChatGPT, etc.  
- 💻 Simple web interface using HTML5 + JavaScript  
- 🎛️ Optional Gradio interface for testing/demo  
- 🔁 Modular backend using Flask and Python utilities



## 📦 Folder Structure

```

MINI\_SIRI/
├── gradio\_app.py            # Main entry point for Gradio UI
├── app.py                   # Flask backend: routes, Gemini logic, weather, TTS/STT
├── utils/
│   ├── speech\_to\_text.py    # Converts audio to text using STT
│   └── text\_to\_speech.py    # Converts text reply to audio using TTS
├── temp/                    # Stores generated response audio (served to frontend)
├── requirements.txt         # Project dependencies

```


## 🚀 How to Clone and Use This Project

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MINI_SIRI.git
cd MINI_SIRI
````

> Replace `yourusername` with your actual GitHub username.

---

### 2. Set Up the Environment

> You’ll need Python 3.8 or higher.

#### (a) Create a Virtual Environment (recommended)

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

#### (b) Install Required Packages

```bash
pip install -r requirements.txt
```

---

### 3. Get API Keys

You need **two API keys** to run Mini Siri:

#### ✅ Google Gemini API Key

* Visit: [https://ai.google.dev/](https://ai.google.dev/)
* Get your API key and copy it.

#### ✅ WeatherAPI Key

* Visit: [https://www.weatherapi.com/](https://www.weatherapi.com/)
* Create a free account and get your API key.

---

### 4. Add Your API Keys

Create a file named `.env` in the root of the project and add:

```env
GEMINI_API_KEY=your_google_gemini_key
WEATHER_API_KEY=your_weatherapi_key
```

Alternatively, you can directly set them as environment variables in your terminal:

```bash
export GEMINI_API_KEY=your_google_gemini_key
export WEATHER_API_KEY=your_weatherapi_key
```

> On Windows, use `set` instead of `export`.

---

## 🖥️ Usage Options

### ✅ Option 1: Run with Flask (Web Interface)

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

🎤 Click **Record**, speak your question, then click **Get Response** to hear Mini Siri’s reply!

---


## 💬 Example Commands

Try asking:

* “Hello”
* “What’s the weather in Paris?”
* “Open YouTube”
* “What’s the time in New York?”
* “Who is the president of France?”

Mini Siri will:

* Recognize your voice
* Understand your question
* Reply back with an answer
* Play the response in voice form
* Open websites if requested

---

## 🧰 Tech Stack

* **Python 3.8+**
* **Flask** – Web backend for STT, TTS, and AI
* **Gradio** – Lightweight UI for demos
* **Google Generative AI (Gemini 1.5 Flash)** – Assistant-like response generation
* **WeatherAPI.com** – Real-time weather and time info
* **HTML5 + JavaScript** – Frontend interaction
* **Web APIs** – For microphone and audio playback


## 👨‍💻 Author

Built by [Jigden Shakya](https://github.com/jigden18)
2nd-year Software Engineering student at the College of Science and Technology.

---

## 💡 Want to Contribute?

Pull requests and ideas are welcome!
Feel free to fork this project and enhance it with:

* Chat history logging
* Multilingual speech support
* Emotion-aware voice replies
* Mobile-friendly design


### Demonstration of the App
[Live Demo](https://drive.google.com/drive/folders/1pGRzJtORIQGvLsGXlofQRDjEe4xAJTFa?usp=drive_link)




