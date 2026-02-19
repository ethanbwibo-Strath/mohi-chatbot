from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def ingest_mohi_docs():
    # 1. Load all PDFs and Docx files from your /data folder
    pdf_loader = DirectoryLoader('./data', glob="./*.pdf", loader_cls=PyPDFLoader)
    docx_loader = DirectoryLoader('./data', glob="./*.docx", loader_cls=Docx2txtLoader)
    
    docs = pdf_loader.load() + docx_loader.load()
    
    # 2. Split them into manageable chunks (approx 1000 characters)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    
    print(f"✅ Ingested {len(docs)} documents and created {len(chunks)} knowledge chunks.")
    return chunks