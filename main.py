import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()

app = FastAPI()

# SECURITY: Allow the React frontend to talk to this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# 1. Load Embeddings and Local Database
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 5}) 

# 2. Auto-Detect Google Model
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
working_model = "gemini-1.5-flash"
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        working_model = m.name.replace("models/", "")
        break

llm = ChatGoogleGenerativeAI(model=working_model, temperature=0)

# 3. Build the Chain
system_prompt = (
    "You are Mika, a friendly, highly advanced clinical AI assistant. Use the provided retrieved context "
    "to answer the user's question about patient records. If you don't know the answer, "
    "say that you don't know. Do not hallucinate external medical facts.\n\n"
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# 4. Define the API Routes
class ChatRequest(BaseModel):
    message: str

@app.post('/chat')
async def chat_endpoint(req: ChatRequest):
    print(f"User asked: {req.message}")
    response = rag_chain.invoke({"input": req.message})
    return {"response": response["answer"]}

@app.get('/')
async def root():
    return {"status": "Mika Clinical AI Backend is actively running!"}