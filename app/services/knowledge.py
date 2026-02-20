import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load environment variables (ensure GOOGLE_API_KEY is in your .env)
load_dotenv()

def run_ingestion():
    data_path = "./data"
    #db_path = "./chroma_db_gemini"
    db_path = "./chroma_db_openai"
    
    # 1. Load all PDFs and Docx files from your data folder
    print("📂 Loading MOHI documents from /data...")
    pdf_loader = DirectoryLoader(data_path, glob="./*.pdf", loader_cls=PyPDFLoader)
    docx_loader = DirectoryLoader(data_path, glob="./*.docx", loader_cls=Docx2txtLoader)
    
    docs = pdf_loader.load() + docx_loader.load()
    
    # 2. Split text into chunks
    # 1000 characters helps keep the context of MOHI policy sections together
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(docs)
    
    # 3. Initialize Google Embeddings with the stable model name
    # embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    print(f"🧠 Vectorizing {len(chunks)} chunks into ChromaDB...")
    
    # 4. Batching Logic to stay under Free Tier Rate Limits (preventing 429 errors)
    batch_size = 5  # Processing 5 chunks at a time
    vector_db = None

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        
        if vector_db is None:
            # Initialize the database with the first batch
            vector_db = Chroma.from_documents(
                documents=batch, 
                embedding=embeddings, 
                persist_directory=db_path
            )
        else:
            # Add subsequent batches to the existing database
            vector_db.add_documents(batch)
        
        print(f"✅ Processed chunks {i} to {min(i + batch_size, len(chunks))}...")
        
        # This 10-second sleep is our "Speed Bump" for the Google API
        time.sleep(10)

    print(f"\n✨ Success! Rafiki IT Knowledge Base is ready.")
    print(f"📍 Database saved at: {os.path.abspath(db_path)}")
    return vector_db

if __name__ == "__main__":
    run_ingestion()