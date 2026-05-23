import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

def main():
    print("Loading documents...")
    loader = DirectoryLoader("clinical_notes", glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()

    print("Chunking text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    print("Generating Local Embeddings (HIPAA Compliant) and building database...")
    # Using free, local embeddings! No API key needed for this part.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    db = Chroma.from_documents(chunks, embeddings, persist_directory="chroma_db")
    db.persist()
    print("✅ Vector database successfully built!")

if __name__ == "__main__":
    main()