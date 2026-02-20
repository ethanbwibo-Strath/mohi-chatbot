from fastapi import FastAPI
from pydantic import BaseModel
from app.services.chatbot import get_rafiki_answer

app = FastAPI(title="MOHI Rafiki IT Chatbot")

# Define the request model ONLY ONCE
class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.get("/")
def health_check():
    return {"status": "online", "service": "Rafiki IT"}

@app.post("/chat")
async def chat_with_rafiki(request: ChatRequest):
    # This calls the service with BOTH the message and the history
    answer = get_rafiki_answer(request.message, chat_history=request.history)
    return {"response": answer}