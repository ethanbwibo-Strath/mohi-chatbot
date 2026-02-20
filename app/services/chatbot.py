import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# NEW
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA

load_dotenv()

def get_rafiki_answer(query: str):
    db_path = "./chroma_db_openai"
    
    # 1. Load the existing 'Brain' we just built
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    
    # 2. Initialize the LLM (The "Thinker")
    # Using gpt-4o-mini is much cheaper than gpt-4o and perfect for this
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # 3. Create the Retrieval Chain
    # This chain handles: Searching DB -> Finding Chunks -> Giving them to GPT -> Getting Answer
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", # "Stuffs" all found chunks into one prompt
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}) # Get top 3 chunks
    )
    
    # 4. Run the query
    print(f"🔍 Rafiki is searching for: {query}")
    response = qa_chain.invoke({"query": query})
    
    return response["result"]

if __name__ == "__main__":
    # TEST RUN: Let's see if it knows about our Nairobi centers
    user_query = "How many centers do we have in Nairobi?"
    answer = get_rafiki_answer(user_query)
    print(f"\n🤖 Rafiki IT: {answer}")