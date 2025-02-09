# 🚀 AI-Powered Space AI Agent

An intelligent space data assistant that simplifies access to space-related information, enhances citizen engagement, and provides real-time insights through AI-driven queries.

## 🌌 Features

### 1️⃣ **AI Chat Agent**

- Utilizes **Groq-powered LLMs** (*Llama 3.3-70B Versatile* and *Mixtral-8x7B*) to process user queries.
- Provides informative responses related to space exploration and astronomy.
- Option to enable **web search** for enhanced accuracy.

### 2️⃣ **NASA Astronomy Picture of the Day (APOD)**

- Fetches the NASA **APOD** for a given date.
- Displays the image along with an explanation from NASA.

## 🔜 Incoming Features

### 🔹 **Speech Recognition Support** 🎙️

- Enables users to **speak their queries** instead of typing.
- Uses **Google Speech Recognition** to convert speech to text.
- Adjusts for ambient noise to improve recognition.

### 🔹 **International Space Station (ISS) Tracker**

- Retrieves and displays the **real-time location** of the ISS.
- Provides latitude and longitude coordinates.

## 🛠️ Installation & Setup

### **Prerequisites**

- Python 3.8+
- Virtual Environment (recommended)
- API Keys for:
  - **GROQ** (LLM)
  - **Tavily** (Web Search)
  - **NASA** (Space Data)

### **Installation Steps**

```bash
# Clone the repository
git clone https://github.com/your-username/ai-mission-planner.git
cd ai-mission-planner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### **Running the App**

```bash
# Start the FastAPI backend
uvicorn backend:app --host 127.0.0.1 --port 9999
```

```bash
# Run the Streamlit UI
streamlit run app.py
```

## 🎯 Usage Guide

1️⃣ **Open the Streamlit app** in your browser. 2️⃣ **Choose a query type** (General Space Info, APOD, or ISS Location). 3️⃣ **Enter text or use voice input** to ask a question. 4️⃣ **View results** including AI-generated responses, images, or ISS coordinates.

## 🛠️ API Endpoints

- `POST /chat` → Handles AI queries and space data requests.

## 🔹 Known Limitations

- Speech recognition may require **a quiet environment** for best results.
- APOD retrieval is limited by **NASA API availability**.
- ISS tracking relies on **open-notify API** and may have occasional downtimes.

## 📜 License

This project is open-source and available under the **MIT License**.

---

**Developed for the 48-hour hackathon, enhancing mission planning with AI!** 🚀

