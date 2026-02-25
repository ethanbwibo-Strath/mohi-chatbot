from fastapi import FastAPI
from pydantic import BaseModel
from app.services.chatbot import get_rafiki_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MOHI Rafiki IT Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, replace with ['https://portal.mohi.org']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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