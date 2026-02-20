import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load environment variables (your GOOGLE_API_KEY)
load_dotenv()

def run_ingestion():
    # 1. Define paths
    data_path = "./data"
    db_path = "./chroma_db"
    
    print("📂 Loading MOHI documents...")
    # Load all PDFs and Docx files from your data folder
    pdf_loader = DirectoryLoader(data_path, glob="./*.pdf", loader_cls=PyPDFLoader)
    docx_loader = DirectoryLoader(data_path, glob="./*.docx", loader_cls=Docx2txtLoader)
    
    docs = pdf_loader.load() + docx_loader.load()
    
    # 2. Split text into chunks
    # We use a 1000-character chunk so we don't lose context on long policy sections
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(docs)
    
    # 3. Initialize Google Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    
    # 4. Create and persist the Vector Store
    print(f"🧠 Vectorizing {len(chunks)} chunks into ChromaDB...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )
    
    print(f"✅ Success! Rafiki IT now knows about:")
    print(f"- I.T. Policies")
    print(f"- Portal Navigation")
    print(f"- Office Extensions")
    print(f"- MOHI Locations & Values")
    
    return vector_db

if __name__ == "__main__":
    run_ingestion()