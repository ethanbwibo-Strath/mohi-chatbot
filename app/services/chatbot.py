import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

load_dotenv()

def get_rafiki_answer(query: str, chat_history: list = []):
    db_path = "./chroma_db_openai"
    
    # 1. Load the existing 'Brain'
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    
    # 2. Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
    
    # 3. Flatten Chat History for the Prompt
    # This prevents the 'Missing Key' error by pre-filling the history
    history_str = ""
    for msg in chat_history[-5:]: # Keep last 5 messages for context
        role = "Staff" if msg["role"] == "user" else "Rafiki"
        history_str += f"{role}: {msg['content']}\n"

    # 4. Define the Personality & Directives
    template = """You are Rafiki, the friendly and supportive I.T. Assistant for Missions of Hope International (MOHI).
    MOHI is a Christ-centered NGO dedicated to transforming impoverished communities in Kenya through holistic ministry.
    Your goal is to help staff with technical issues while reflecting MOHI's values of grace.

    GUIDELINES:
    1. If the answer is in the context, explain it clearly and warmly.
    2. If a user mentions stress or illness, acknowledge it with empathy first.
    3. Conciseness: Use numbered steps and bold text for menu items (e.g., **Employee** > **Leave**).
    4. If unknown, suggest contacting the I.T. department at Pangani (Ext 303/304).

    CONTEXT: {context}
    
    CHAT HISTORY: 
    {chat_history}

    STAFF MEMBER: {question}
    RAFIKI:"""

    # Note: chat_history is NOT in input_variables because we 'partial' it
    RAFIKI_PROMPT = PromptTemplate(
        template=template, 
        input_variables=["context", "question"]
    ).partial(chat_history=history_str)

    # 5. Create the Retrieval Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": RAFIKI_PROMPT}
    )
    
    # 6. Run the query
    print(f"🔍 Rafiki is searching for: {query}")
    response = qa_chain.invoke({"query": query, "question": query})
    
    return response["result"]

if __name__ == "__main__":
    # Internal Test Run
    user_query = "How many centers do we have in Nairobi?"
    answer = get_rafiki_answer(user_query, chat_history=[])
    print(f"\n🤖 Rafiki IT: {answer}")