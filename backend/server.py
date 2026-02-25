"""
Rafiki IT - Backend Server
Proxies chat requests to the existing FastAPI chatbot endpoint
"""

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent app directory to path for importing the chatbot
sys.path.insert(0, str(Path(__file__).parent.parent))

# Try to import the chatbot service directly
try:
    from app.services.chatbot import get_rafiki_answer
    CHATBOT_AVAILABLE = True
    print("✓ Chatbot service loaded successfully")
except ImportError as e:
    CHATBOT_AVAILABLE = False
    print(f"⚠ Chatbot service not available: {e}")
    print("  Will use HTTP proxy mode instead")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    print("=" * 50)
    print("🚀 Rafiki IT Backend Starting...")
    print(f"   Chatbot Direct Mode: {CHATBOT_AVAILABLE}")
    print("=" * 50)
    yield
    print("👋 Rafiki IT Backend Shutting Down...")

app = FastAPI(
    title="Rafiki IT Backend",
    description="Backend service for MOHI Rafiki IT Support Chat",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str

class HealthResponse(BaseModel):
    status: str
    service: str
    chatbot_mode: str

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="online",
        service="Rafiki IT Backend",
        chatbot_mode="direct" if CHATBOT_AVAILABLE else "proxy"
    )

@app.get("/api/health", response_model=HealthResponse)
async def api_health_check():
    """API Health check endpoint"""
    return HealthResponse(
        status="online",
        service="Rafiki IT Backend",
        chatbot_mode="direct" if CHATBOT_AVAILABLE else "proxy"
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_rafiki(request: ChatRequest):
    """
    Chat endpoint that either:
    1. Calls the chatbot service directly (if available)
    2. Proxies to the existing FastAPI endpoint
    """
    try:
        if CHATBOT_AVAILABLE:
            # Direct call to chatbot service
            history_dicts = [{"role": msg.role, "content": msg.content} for msg in (request.history or [])]
            answer = get_rafiki_answer(request.message, chat_history=history_dicts)
            return ChatResponse(response=answer)
        else:
            # Proxy to existing endpoint (fallback)
            async with httpx.AsyncClient(timeout=60.0) as client:
                history_dicts = [{"role": msg.role, "content": msg.content} for msg in (request.history or [])]
                response = await client.post(
                    "http://127.0.0.1:8000/chat",
                    json={
                        "message": request.message,
                        "history": history_dicts
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return ChatResponse(response=data.get("response", "I'm having trouble responding right now."))
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Chatbot service returned an error"
                    )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="The chatbot service is taking too long to respond. Please try again."
        )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the chatbot service. Please ensure it's running."
        )
    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
