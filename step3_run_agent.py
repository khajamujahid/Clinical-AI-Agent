import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()

def get_working_model():
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return m.name.replace("models/", "")
    return "gemini-1.5-flash" 

def main():
    print("Starting up the AI Agent... Please wait a moment.")
    
    # 1. Load Local Embeddings and Database
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 5}) 
    
    # 2. Auto-Detect the Model
    working_model = get_working_model()
    llm = ChatGoogleGenerativeAI(model=working_model, temperature=0)

    # 3. Define the Prompt
    system_prompt = (
        "You are a clinical AI assistant. Use the provided retrieved context "
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

    # 4. Interactive Terminal Loop
    print("\n" + "="*50)
    print("✅ Clinical AI Agent is READY!")
    print("Type 'exit' or 'quit' to stop.")
    print("="*50 + "\n")

    while True:
        # This pauses the script and waits for you to type in the terminal!
        user_query = input("What would you like to ask the medical records? \n> ")
        
        # Check if you want to turn it off
        if user_query.lower() in ['exit', 'quit']:
            print("Shutting down the AI Agent. Great job today!")
            break
            
        if not user_query.strip():
            continue
            
        print("\n🤖 AI is thinking...")
        response = rag_chain.invoke({"input": user_query})
        print(f"\nAI Agent Response:\n{response['answer']}\n")
        print("-" * 50 + "\n")

if __name__ == "__main__":
    main()