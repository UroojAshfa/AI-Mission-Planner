# Setup API keys for GROQ, Tavily, and NASA
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
NASA_API_KEY = os.environ.get("NASA_API_KEY")

# Setup LLM and tools
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool

# Initialize LLMs
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

system_prompt="You are an AI-powered mission planner agent that simplifies access to space-related data, provides educational tools, and fosters citizen engagement in space exploration."

# Custom tools for space data
@tool
def get_nasa_apod(date: str):
    """Fetch the Astronomy Picture of the Day (APOD) from NASA."""
    import requests
    url = f"https://api.nasa.gov/planetary/apod?date={date}&api_key={NASA_API_KEY}"
    response = requests.get(url)
    return response.json()

@tool
def get_iss_location():
    """Fetch the current location of the International Space Station (ISS)."""
    import requests
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    return response.json()

# Setup AI agent with search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

def get_response(llm_id, query, allow_search, system_prompt, provider):
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    
    # Include custom tools if search is allowed
    tools = [TavilySearchResults(max_results=2), get_nasa_apod, get_iss_location] if allow_search else []
    
    # Create the agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    
    # Invoke the agent
    state = {"messages": query}
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]
