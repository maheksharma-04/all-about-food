import os
import sys
import datetime
import webbrowser
import pyttsx3
import speech_recognition as sr
from openai import OpenAI

# -------------------------------------------------------------
# 1. INITIALIZE VOICE ENGINE (TTS)
# -------------------------------------------------------------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Set a voice (0 = male, 1 = female depending on system settings)
engine.setProperty('voice', voices[0].id) 
engine.setProperty('rate', 180)  # Speech rate

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

# -------------------------------------------------------------
# 2. INITIALIZE AI BRAIN (OpenAI API or local host)
# -------------------------------------------------------------
# Set your API key in environment variables, or pass directly:
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"
client = OpenAI()

def ask_ai(prompt):
    """Sends user query to OpenAI for a JARVIS-like persona response."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or gpt-4o
            messages=[
                {"role": "system", "content": "You are JARVIS, a polite, witty, and highly efficient AI assistant modeled after Iron Man's assistant. Keep responses concise and conversational."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "I encountered an issue connecting to my central processing unit, sir."

# -------------------------------------------------------------
# 3. SPEECH RECOGNITION (STT)
# -------------------------------------------------------------
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"User: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Network error with the speech recognition service.")
            return ""

# -------------------------------------------------------------
# 4. SYSTEM ACTIONS & MAIN LOOP
# -------------------------------------------------------------
def run_jarvis():
    speak("JARVIS system online. How may I assist you today, sir?")
    
    while True:
        query = listen()
        if not query:
            continue

        # Native Commands
        if "open youtube" in query:
            speak("Opening YouTube, sir.")
            webbrowser.open("https://youtube.com")

        elif "open google" in query:
            speak("Opening Google.")
            webbrowser.open("https://google.com")

        elif "time" in query:
            str_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is currently {str_time}.")

        elif "goodbye" in query or "shutdown" in query or "exit" in query:
            speak("Shutting down systems. Have a good day, sir.")
            sys.exit()

        # AI-Powered Fallback
        else:
            ai_response = ask_ai(query)
            speak(ai_response)

if __name__ == "__main__":
    run_jarvis()
