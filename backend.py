# Step1: Setup Pydantic Model (Schema Validation)
from pydantic import BaseModel
from typing import List
import os
from fastapi import FastAPI, HTTPException
import requests

# Add this to your existing imports
NASA_API_KEY = os.getenv("NASA_API_KEY")  # Make sure to add your NASA API key in the .env file

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


# Step2: Setup AI Agent from FrontEnd Request
from fastapi import FastAPI
from agent import get_response_from_ai_agent

ALLOWED_MODEL_NAMES = ["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]

app = FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState): 
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model"}
    
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider

    # Create AI Agent and get response from it! 
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return response

@app.get("/apod")
def get_apod():
    """
    Fetch the Astronomy Picture of the Day (APOD) from NASA API.
    """
    if not NASA_API_KEY:
        raise HTTPException(status_code=400, detail="NASA API key is missing. Please check your .env file.")
    
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch APOD data: {str(e)}")

# Step3: Run app & Explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)
