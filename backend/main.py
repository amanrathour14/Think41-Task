from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import os
from datetime import datetime
import logging

# Import our services and models
from database import get_db, create_tables
from models import Base
from conversation_service import ConversationService
from llm_service import LLMService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="E-commerce Customer Support Chatbot", version="2.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class ChatMessage(BaseModel):
    message: str
    user_email: str = "anonymous@example.com"
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class ConversationResponse(BaseModel):
    conversation_id: str
    title: str
    created_at: str
    updated_at: str
    total_messages: int
    user_messages: int
    ai_messages: int
    is_active: bool

class MessageResponse(BaseModel):
    id: str
    content: str
    is_user_message: bool
    created_at: str
    metadata: Optional[Dict[str, Any]] = None

# Initialize LLM service
llm_service = LLMService()

@app.on_event("startup")
async def startup_event():
    """Initialize database and create tables"""
    try:
        create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

@app.get("/")
async def root():
    return {
        "message": "E-commerce Customer Support Chatbot API v2.0",
        "version": "2.0.0",
        "features": [
            "Database-backed conversations",
            "LLM integration with Groq",
            "Multi-user support",
            "Conversation history"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_message: ChatMessage,
    db: Session = Depends(get_db)
):
    """Main chat endpoint with database persistence and LLM integration"""
    try:
        # Initialize services
        conversation_service = ConversationService(db)
        
        # Get or create user
        user = conversation_service.create_user(
            email=chat_message.user_email,
            first_name="Anonymous",
            last_name="User"
        )
        
        # Get or create conversation
        conversation = conversation_service.get_or_create_conversation(
            user_id=user.id,
            conversation_id=chat_message.conversation_id
        )
        
        # Add user message to conversation
        user_message = conversation_service.add_message(
            conversation_id=conversation.id,
            content=chat_message.message,
            is_user_message=True
        )
        
        # Get conversation history for context
        conversation_history = conversation_service.get_conversation_history(
            conversation_id=conversation.id,
            limit=10
        )
        
        # Generate AI response using LLM
        llm_response = llm_service.generate_response(
            user_message=chat_message.message,
            conversation_history=conversation_history,
            db=db
        )
        
        # Add AI response to conversation
        ai_message = conversation_service.add_message(
            conversation_id=conversation.id,
            content=llm_response["response"],
            is_user_message=False,
            message_metadata=llm_response.get("metadata", {})
        )
        
        return ChatResponse(
            response=llm_response["response"],
            conversation_id=conversation.id,
            data=llm_response.get("data"),
            metadata=llm_response.get("metadata")
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{user_email}", response_model=List[ConversationResponse])
async def get_user_conversations(
    user_email: str,
    db: Session = Depends(get_db)
):
    """Get all conversations for a user"""
    try:
        conversation_service = ConversationService(db)
        user = conversation_service.create_user(email=user_email)
        conversations = conversation_service.get_user_conversations(user.id)
        
        return [
            ConversationResponse(
                conversation_id=conv.id,
                title=conv.title,
                created_at=conv.created_at.isoformat() if conv.created_at else "",
                updated_at=conv.updated_at.isoformat() if conv.updated_at else "",
                total_messages=len(conversation_service.get_conversation_messages(conv.id)),
                user_messages=len([m for m in conversation_service.get_conversation_messages(conv.id) if m.is_user_message]),
                ai_messages=len([m for m in conversation_service.get_conversation_messages(conv.id) if not m.is_user_message]),
                is_active=conv.is_active
            )
            for conv in conversations
        ]
    except Exception as e:
        logger.error(f"Error getting user conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get messages for a specific conversation"""
    try:
        conversation_service = ConversationService(db)
        messages = conversation_service.get_conversation_messages(conversation_id, limit=100)
        
        return [
            MessageResponse(
                id=msg.id,
                content=msg.content,
                is_user_message=msg.is_user_message,
                created_at=msg.created_at.isoformat() if msg.created_at else "",
                metadata=msg.message_metadata
            )
            for msg in messages
        ]
    except Exception as e:
        logger.error(f"Error getting conversation messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/conversations/{conversation_id}/title")
async def update_conversation_title(
    conversation_id: str,
    title: str,
    db: Session = Depends(get_db)
):
    """Update conversation title"""
    try:
        conversation_service = ConversationService(db)
        success = conversation_service.update_conversation_title(conversation_id, title)
        
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {"message": "Conversation title updated successfully"}
    except Exception as e:
        logger.error(f"Error updating conversation title: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/conversations/{conversation_id}")
async def deactivate_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Deactivate a conversation"""
    try:
        conversation_service = ConversationService(db)
        success = conversation_service.deactivate_conversation(conversation_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {"message": "Conversation deactivated successfully"}
    except Exception as e:
        logger.error(f"Error deactivating conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Legacy endpoint for backward compatibility
@app.post("/chat", response_model=ChatResponse)
async def legacy_chat_endpoint(chat_message: ChatMessage, db: Session = Depends(get_db)):
    """Legacy chat endpoint for backward compatibility"""
    return await chat_endpoint(chat_message, db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 