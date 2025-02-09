# Setup Pydantic Model (schema validation)
from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool
    query_type: str  # New field for space data queries

# Setup AI agent from frontend request
from fastapi import FastAPI
from ai_agent import get_response, get_nasa_apod, get_iss_location

ALLOWED_MODEL_NAMES = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]

app = FastAPI(title="Space Data AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request.
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"Error!": "Invalid model name: kindly select a valid AI model"}
    
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider
    query_type = request.query_type  # New field

    # Handle space data queries
    if query_type == "APOD":
        date = query[0].split()[-1]  # Extract date from query
        response = get_nasa_apod(date)
        return response
    elif query_type == "ISS Location":
        response = get_iss_location()
        return response
    else:
        # Default AI agent response
        response = get_response(llm_id, query, allow_search, system_prompt, provider)
        return response

# Run app and explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)
