from fastapi import FastAPI
from pydantic import BaseModel
from app.services.chatbot import get_rafiki_answer

app = FastAPI(title="MOHI Rafiki IT Chatbot")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def health_check():
    return {"status": "online", "service": "Rafiki IT"}

@app.post("/chat")
async def chat_with_rafiki(request: ChatRequest):
    # This calls the chatbot service we just tested
    answer = get_rafiki_answer(request.message)
    return {"response": answer}