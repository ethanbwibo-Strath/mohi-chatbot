"""
Rafiki IT - Backend Server
Provides chat functionality for MOHI IT Support
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

# Track chatbot availability
CHATBOT_AVAILABLE = False
get_rafiki_answer = None

# Try to import the chatbot service directly
try:
    # Change working directory for correct path resolution
    original_cwd = os.getcwd()
    os.chdir(Path(__file__).parent.parent)
    
    from app.services.chatbot import get_rafiki_answer as _get_rafiki_answer
    get_rafiki_answer = _get_rafiki_answer
    CHATBOT_AVAILABLE = True
    print("✓ Chatbot service loaded successfully")
    
    os.chdir(original_cwd)
except ImportError as e:
    print(f"⚠ Chatbot service not available: {e}")
    print("  Using built-in response mode")
except Exception as e:
    print(f"⚠ Chatbot initialization error: {e}")
    print("  Using built-in response mode")

# Built-in responses for when the full chatbot isn't available
BUILTIN_RESPONSES = {
    "it office": """The **MOHI IT Office** is located at the **Pangani Head Office**. 

**Contact Information:**
- 📞 Extension: **303** or **304**
- 📍 Location: Pangani Head Office, Nairobi

Feel free to reach out during working hours (8:00 AM - 5:00 PM). God bless! 🙏""",
    
    "locked": """I'm sorry to hear you're locked out of your portal! Here's how to get help:

**Steps to Resolve Portal Lockout:**
1. Contact the IT department at **Extension 303 or 304**
2. Provide your **Staff ID** and **Username**
3. Wait for password reset (usually within 30 minutes)

**Tip:** While waiting, you can verify your internet connection is stable.

Don't worry, we'll get you back in quickly! 🔑""",
    
    "leave": """Here's how to apply for leave through the MOHI Portal:

**Steps to Apply for Leave:**
1. Log into the **MOHI Staff Portal**
2. Navigate to **Employee** > **Leave Application**
3. Select the **Leave Type** (Annual, Sick, etc.)
4. Enter your **Start Date** and **End Date**
5. Add any required **Supporting Documents**
6. Click **Submit** and wait for supervisor approval

Need help? Contact HR at the Pangani office. 📝""",

    "default": """Thank you for reaching out! I'm Rafiki, your friendly IT assistant for MOHI.

I'm currently in **limited mode**, but I can still help guide you! Here are some quick options:

• **IT Office Location** - Our team is at Pangani (Ext 303/304)
• **Portal Issues** - Contact IT for password resets
• **Leave Applications** - Use Employee > Leave in the portal

For complex technical issues, please contact the IT department directly. May God bless your work today! 🙏"""
}

def get_builtin_response(message: str) -> str:
    """Get a built-in response based on message content"""
    message_lower = message.lower()
    
    if "office" in message_lower and ("it" in message_lower or "location" in message_lower or "where" in message_lower):
        return BUILTIN_RESPONSES["it office"]
    elif "lock" in message_lower or "password" in message_lower or "reset" in message_lower:
        return BUILTIN_RESPONSES["locked"]
    elif "leave" in message_lower or "apply" in message_lower or "vacation" in message_lower:
        return BUILTIN_RESPONSES["leave"]
    else:
        return BUILTIN_RESPONSES["default"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    print("=" * 50)
    print("🚀 Rafiki IT Backend Starting...")
    print(f"   Chatbot Mode: {'AI-Powered' if CHATBOT_AVAILABLE else 'Built-in Responses'}")
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

class FeedbackRequest(BaseModel):
    messageIndex: int
    messageContent: Optional[str] = None
    feedbackType: str  # 'positive' or 'negative'
    feedbackReason: Optional[str] = None  # 'confused', 'more-detail', 'wrong', 'human'
    timestamp: str

class FeedbackResponse(BaseModel):
    success: bool
    message: str

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="online",
        service="Rafiki IT Backend",
        chatbot_mode="ai-powered" if CHATBOT_AVAILABLE else "builtin"
    )

@app.get("/api/health", response_model=HealthResponse)
async def api_health_check():
    """API Health check endpoint"""
    return HealthResponse(
        status="online",
        service="Rafiki IT Backend",
        chatbot_mode="ai-powered" if CHATBOT_AVAILABLE else "builtin"
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_rafiki(request: ChatRequest):
    """
    Chat endpoint that either:
    1. Calls the AI-powered chatbot service (if available)
    2. Uses built-in intelligent responses
    """
    try:
        if CHATBOT_AVAILABLE and get_rafiki_answer:
            # Direct call to AI chatbot service
            history_dicts = [{"role": msg.role, "content": msg.content} for msg in (request.history or [])]
            answer = get_rafiki_answer(request.message, chat_history=history_dicts)
            return ChatResponse(response=answer)
        else:
            # Use built-in responses
            response_text = get_builtin_response(request.message)
            return ChatResponse(response=response_text)
            
    except Exception as e:
        print(f"Chat error: {str(e)}")
        # Fallback to built-in response on any error
        response_text = get_builtin_response(request.message)
        return ChatResponse(response=response_text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
