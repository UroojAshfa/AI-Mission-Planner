import streamlit as st
import requests
from gtts import gTTS
import speech_recognition as sr
import os



# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")
    os.system("start response.mp3" if os.name == "nt" else "afplay response.mp3")  # Play the audio file

# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("Sorry, there was an issue with the speech recognition service.")
            return None

st.set_page_config(page_title="Space Data AI Agent", layout="centered")
st.title("AI-Powered Mission Planner Agent")
st.write("Enhance your access to space-related data and insights!")

# System prompt
system_prompt = st.text_area(
    "Define your AI Agent: ",
    height=70,
    placeholder="Type your system prompt: ",
    value="You are an AI-powered mission planner agent that simplifies access to space-related data, provides educational tools, and fosters citizen engagement in space exploration."
)

# Model selection
MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
provider = st.radio("Select Provider: ", ("Groq",))
selected_model = st.selectbox("Select Model: ", MODEL_NAMES_GROQ)

# Query type selection
query_type = st.radio("Select Query Type: ", ("General Space Info", "APOD", "ISS Location"))

# Voice input toggle
use_voice_input = st.checkbox("Use Voice Input")

# User input
if use_voice_input:
    if st.button("Start Voice Input"):
        user_query = speech_to_text()
else:
    if query_type == "APOD":
        date = st.text_input("Enter date (YYYY-MM-DD):", "2023-10-01")
        user_query = f"Fetch APOD for {date}"
    elif query_type == "ISS Location":
        user_query = "Fetch current ISS location"
    else:
        user_query = st.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")

# Allow web search
allow_web_search = st.checkbox("Allow Web Search")

# API URL
API_URL = "http://127.0.0.1:9999/chat"

# Send request to backend
if st.button("Ask Agent!"):
    if user_query.strip():
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search,
            "query_type": query_type
        }
        logger.info(f"Sending payload to backend: {payload}")
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                if query_type == "APOD":
                    st.image(response_data["url"], caption=response_data["title"])
                    st.write(response_data["explanation"])
                elif query_type == "ISS Location":
                    st.write(f"ISS Location: Latitude = {response_data['iss_position']['latitude']}, Longitude = {response_data['iss_position']['longitude']}")
                else:
                    st.markdown(f"Final Response: {response_data['response']}")
                
                # Convert response to speech
                if st.checkbox("Enable Voice Output"):
                    text_to_speech(response_data['response'])
