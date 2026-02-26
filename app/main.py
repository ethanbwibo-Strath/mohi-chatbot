from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
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

class FeedbackRequest(BaseModel):
    messageIndex: int
    messageContent: Optional[str] = None
    feedbackType: str  # 'positive' or 'negative'
    feedbackReason: Optional[str] = None  # 'confused', 'more-detail', 'wrong', 'human'
    timestamp: str

class FeedbackResponse(BaseModel):
    success: bool
    message: str

@app.get("/")
def health_check():
    return {"status": "online", "service": "Rafiki IT"}

@app.post("/chat")
async def chat_with_rafiki(request: ChatRequest):
    # This calls the service with BOTH the message and the history
    answer = get_rafiki_answer(request.message, chat_history=request.history)
    return {"response": answer}

# In-memory storage for feedback (could be moved to MongoDB for persistence)
feedback_store = []

@app.post("/api/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Store user feedback about Rafiki's responses.
    This data can be used to improve the chatbot over time.
    """
    try:
        feedback_entry = {
            "messageIndex": request.messageIndex,
            "messageContent": request.messageContent,
            "feedbackType": request.feedbackType,
            "feedbackReason": request.feedbackReason,
            "timestamp": request.timestamp
        }
        
        feedback_store.append(feedback_entry)
        
        # Log feedback for analysis
        feedback_icon = "👍" if request.feedbackType == "positive" else "👎"
        reason_text = f" - {request.feedbackReason}" if request.feedbackReason else ""
        print(f"{feedback_icon} Feedback received{reason_text}")
        
        return FeedbackResponse(
            success=True,
            message="Thank you for your feedback!"
        )
    except Exception as e:
        print(f"Feedback error: {str(e)}")
        return FeedbackResponse(
            success=False,
            message="Failed to save feedback"
        )

@app.get("/feedback/stats")
async def get_feedback_stats():
    """Get aggregated feedback statistics"""
    if not feedback_store:
        return {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "reasons": {}
        }
    
    positive = sum(1 for f in feedback_store if f["feedbackType"] == "positive")
    negative = sum(1 for f in feedback_store if f["feedbackType"] == "negative")
    
    reasons = {}
    for f in feedback_store:
        if f["feedbackReason"]:
            reasons[f["feedbackReason"]] = reasons.get(f["feedbackReason"], 0) + 1
    
    return {
        "total": len(feedback_store),
        "positive": positive,
        "negative": negative,
        "satisfaction_rate": round((positive / len(feedback_store)) * 100, 1) if feedback_store else 0,
        "reasons": reasons
    }