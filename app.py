import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# --- 1. SET UP THE WEB PAGE ---
st.set_page_config(page_title="Clinical AI Companion", page_icon="🏥", layout="wide")

# --- 2. CACHE THE AI ENGINE ---
@st.cache_resource
def load_ai_engine():
    load_dotenv()
    
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    working_model = "gemini-1.5-flash"
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            working_model = m.name.replace("models/", "")
            break
            
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 5}) 
    
    llm = ChatGoogleGenerativeAI(model=working_model, temperature=0)
    system_prompt = (
        "You are a friendly, helpful clinical AI assistant. Use the provided retrieved context "
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
    
    return rag_chain

rag_chain = load_ai_engine()

# --- 3. BUILD THE LOCKED LEFT SIDEBAR ---
with st.sidebar:
    try:
        # This locks your 3D avatar to the top left!
        st.image("nurse.jpg", use_container_width=True)
    except:
        st.error("Image 'nurse.jpg' not found.")
        
    st.title("Clinical AI Companion")
    st.caption("Ask me anything about the local patient database!")
    st.divider()
    st.markdown("**Instructions:**")
    st.markdown("- Type your query on the right.\n- I will securely scan the local database.\n- Scroll the right panel to see chat history.")

# --- 4. BUILD THE SCROLLING CHAT (RIGHT SIDE) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT INPUT BOX ---
if user_query := st.chat_input("Type your medical query here..."):
    
    with st.chat_message("user"):
        st.markdown(user_query)
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        with st.spinner("Accessing medical records..."):
            response = rag_chain.invoke({"input": user_query})
            answer = response["answer"]
            st.markdown(answer)
            
    st.session_state.messages.append({"role": "assistant", "content": answer})