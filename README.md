Markdown
# 🏥 MIKA OS: Full-Stack Clinical AI Companion

![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-black?style=for-the-badge&logo=three.js)

MIKA OS is a cinematic, dual-engine Retrieval-Augmented Generation (RAG) healthcare assistant. It bridges a highly secure Python/ChromaDB AI backend with a modern, glassmorphic Next.js 3D frontend. 

The system acts as a clinical companion, allowing users to query synthetic patient databases in natural language while maintaining strict hallucination guardrails.

---

## ✨ Key Features

* **Advanced RAG Pipeline:** Securely retrieves medical records from a local ChromaDB vector store before generating responses.
* **Holographic 3D UI:** Uses React Three Fiber to project a 2D clinical avatar onto a floating 3D holographic plane.
* **Asynchronous Backend:** Built on FastAPI to handle concurrent user requests efficiently.
* **Hallucination Guardrails:** The LLM is strictly prompted to only synthesize answers based on the retrieved local context, mitigating external medical hallucinations.
* **Apple-Inspired Glassmorphism:** Sleek, modern frontend utilizing TailwindCSS for a premium user experience.

---

## 🛠️ Architecture & Tech Stack

### The Backend (AI & Logic)
* **Framework:** FastAPI / Python
* **LLM Engine:** Google Gemini (1.5 Flash)
* **Orchestration:** LangChain
* **Vector Database:** ChromaDB
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)

### The Frontend (UI & 3D Rendering)
* **Framework:** Next.js (App Router) / React
* **Styling:** TailwindCSS
* **3D Engine:** Three.js / React Three Fiber / Drei
* **State Management:** React Hooks (`useState`, `useEffect`)

---

## 🚀 Local Installation & Setup

To run this full-stack application on your local machine, you will need two separate terminal windows running simultaneously.

### Prerequisites
* **Node.js** (v18 or higher)
* **Python** (3.10 or higher)
* **Git**

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Clinical-AI-Agent.git](https://github.com/YOUR_USERNAME/Clinical-AI-Agent.git)
cd Clinical-AI-Agent
2. Set Up the Backend (Terminal 1)
Bash
# Create and activate a virtual environment
python -m venv venv

# Windows Activation:
venv\Scripts\activate
# Mac/Linux Activation:
source venv/bin/activate

# Install Python dependencies
pip install fastapi uvicorn langchain langchain-google-genai langchain-community langchain-huggingface chromadb python-dotenv pydantic

# Create your environment variables file
# Add your Google API Key to a .env file in the root directory like this:
# GOOGLE_API_KEY="your_api_key_here"

# Start the FastAPI Server
uvicorn main:app --reload
The backend will now be running on http://localhost:8000

3. Set Up the Frontend (Terminal 2)
Bash
# Open a second terminal window and navigate to the frontend folder
cd frontend

# Install Node modules
npm install

# Start the Next.js development server
npm run dev
The frontend will now be running on http://localhost:3000

💻 Usage
Open your web browser and navigate to http://localhost:3000.

The MIKA OS interface will load, rendering the 3D clinical avatar.

Use the chat panel on the right to ask natural language questions about the synthetic patient database (e.g., "How many patients have Asthma?" or "What medications is Patient X currently taking?").

The frontend will query the FastAPI backend, process the vector search, and return a context-aware AI response.

⚠️ Disclaimer
This is a portfolio engineering project. All patient data within the chroma_db is 100% synthetic and programmatically generated. This AI is not intended to provide real medical advice, diagnosis, or treatment.

Built with passion by **Khaja mujahiddin**
