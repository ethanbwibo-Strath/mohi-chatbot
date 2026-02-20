import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

load_dotenv()

def get_rafiki_answer(query: str):
    db_path = "./chroma_db_openai"
    
    # 1. Load the existing 'Brain' we just built
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    
    # 2. Initialize the LLM (The "Thinker")
    # Using gpt-4o-mini is much cheaper than gpt-4o and perfect for this
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
# Define the Personality/Directives
    template = """You are Rafiki, the friendly and supportive I.T. Assistant for Missions of Hope International (MOHI).
    Your goal is to help staff with technical issues while reflecting MOHI's values of grace and holistic ministry.
    
    GUIDELINES:
    1. If the answer is in the context, explain it clearly and warmly.
    2. If you don't know the answer, don't make it up. Suggest they contact the I.T. department at Pangani.
    3. Keep your tone professional yet brotherly.

    CONTEXT: {context}
    
    STAFF MEMBER: {question}
    RAFIKI:"""

    RAFIKI_PROMPT = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )

    # 3. Create the Retrieval Chain
    # This chain handles: Searching DB -> Finding Chunks -> Giving them to GPT -> Getting Answer
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", # "Stuffs" all found chunks into one prompt
        retriever=vector_db.as_retriever(search_kwargs={"k": 5}), # Get top 5 chunks
        chain_type_kwargs={"prompt": RAFIKI_PROMPT}
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