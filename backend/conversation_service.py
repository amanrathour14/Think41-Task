from sqlalchemy.orm import Session
from models import User, Conversation, Message
from typing import List, Dict, Optional
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConversationService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, email: str, first_name: str = "Anonymous", last_name: str = "User") -> User:
        """Create a new user or get existing user"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                id=str(uuid.uuid4()),
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"Created new user: {user.id}")
        return user
    
    def create_conversation(self, user_id: str, title: str = None) -> Conversation:
        """Create a new conversation for a user"""
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        logger.info(f"Created new conversation: {conversation.id}")
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """Get all conversations for a user"""
        return self.db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.is_active == True
        ).order_by(Conversation.updated_at.desc()).all()
    
    def add_message(self, conversation_id: str, content: str, is_user_message: bool, message_metadata: Dict = None) -> Message:
        """Add a message to a conversation"""
        message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            content=content,
            is_user_message=is_user_message,
            message_metadata=message_metadata or {}
        )
        self.db.add(message)
        
        # Update conversation timestamp
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.updated_at = datetime.now()
        
        self.db.commit()
        self.db.refresh(message)
        logger.info(f"Added message to conversation {conversation_id}")
        return message
    
    def get_conversation_messages(self, conversation_id: str, limit: int = 50) -> List[Message]:
        """Get messages for a conversation"""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit).all()
    
    def get_conversation_history(self, conversation_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history as list of dicts for LLM context"""
        messages = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).limit(limit).all()
        
        return [
            {
                "content": msg.content,
                "is_user_message": msg.is_user_message,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
                "metadata": msg.message_metadata
            }
            for msg in messages
        ]
    
    def update_conversation_title(self, conversation_id: str, title: str) -> bool:
        """Update conversation title"""
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.title = title
            self.db.commit()
            return True
        return False
    
    def deactivate_conversation(self, conversation_id: str) -> bool:
        """Deactivate a conversation"""
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.is_active = False
            self.db.commit()
            return True
        return False
    
    def get_or_create_conversation(self, user_id: str, conversation_id: str = None) -> Conversation:
        """Get existing conversation or create new one"""
        if conversation_id:
            conversation = self.get_conversation(conversation_id)
            if conversation and conversation.user_id == user_id:
                return conversation
        
        # Create new conversation
        return self.create_conversation(user_id)
    
    def get_conversation_summary(self, conversation_id: str) -> Dict:
        """Get summary of a conversation"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return {}
        
        messages = self.get_conversation_messages(conversation_id)
        user_messages = [msg for msg in messages if msg.is_user_message]
        ai_messages = [msg for msg in messages if not msg.is_user_message]
        
        return {
            "conversation_id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
            "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None,
            "total_messages": len(messages),
            "user_messages": len(user_messages),
            "ai_messages": len(ai_messages),
            "is_active": conversation.is_active
        } 