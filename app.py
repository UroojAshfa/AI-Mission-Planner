# Setup Streamlit UI (model provider, model, system prompt, web search, query)
import streamlit as st
import requests

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

# User input
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
                    st.markdown(f"Final Response: {response_data}")