from fastapi import FastAPI

app = FastAPI(title="MOHI Rafiki IT Engine")

@app.get("/")
def read_root():
    return {"status": "Online", "message": "MOHI Chatbot Engine is running"}

@app.post("/chat")
async def chat_endpoint(user_message: str):
    # This is where the AI logic will eventually go
    return {"response": f"You said: {user_message}. I'm still learning!"}