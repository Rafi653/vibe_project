"""
Chat-related Pydantic schemas
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.chat import ConversationType


# Base schemas
class MessageBase(BaseModel):
    """Base message schema"""
    content: str = Field(..., min_length=1, max_length=10000)


class ConversationBase(BaseModel):
    """Base conversation schema"""
    name: Optional[str] = Field(None, max_length=255)
    conversation_type: ConversationType = ConversationType.DIRECT


class ConversationParticipantBase(BaseModel):
    """Base conversation participant schema"""
    user_id: int
    is_admin: bool = False


# Request schemas
class MessageCreate(MessageBase):
    """Schema for creating a message"""
    conversation_id: int


class MessageUpdate(BaseModel):
    """Schema for updating a message"""
    content: str = Field(..., min_length=1, max_length=10000)


class ConversationCreate(ConversationBase):
    """Schema for creating a conversation"""
    participant_ids: List[int] = Field(..., min_items=1)


class ConversationUpdate(BaseModel):
    """Schema for updating a conversation"""
    name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class AddParticipant(BaseModel):
    """Schema for adding a participant to a conversation"""
    user_id: int
    is_admin: bool = False


# Response schemas
class UserInfo(BaseModel):
    """User information for chat"""
    id: int
    full_name: str
    email: str
    role: str
    
    class Config:
        from_attributes = True


class MessageResponse(MessageBase):
    """Response schema for a message"""
    id: int
    conversation_id: int
    sender_id: int
    sender: UserInfo
    is_read: bool
    is_edited: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConversationParticipantResponse(BaseModel):
    """Response schema for a conversation participant"""
    id: int
    conversation_id: int
    user_id: int
    user: UserInfo
    is_admin: bool
    last_read_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationResponse(ConversationBase):
    """Response schema for a conversation"""
    id: int
    is_active: bool
    participants: List[ConversationParticipantResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConversationWithMessages(ConversationResponse):
    """Response schema for a conversation with messages"""
    messages: List[MessageResponse]
    unread_count: int = 0


class ConversationListItem(ConversationResponse):
    """Response schema for conversation list item"""
    last_message: Optional[MessageResponse] = None
    unread_count: int = 0


# WebSocket message schemas
class WSMessageType(str):
    """WebSocket message types"""
    MESSAGE = "message"
    TYPING = "typing"
    READ_RECEIPT = "read_receipt"
    USER_STATUS = "user_status"
    ERROR = "error"


class WSMessage(BaseModel):
    """WebSocket message schema"""
    type: str
    data: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TypingIndicator(BaseModel):
    """Typing indicator schema"""
    conversation_id: int
    user_id: int
    is_typing: bool


class ReadReceipt(BaseModel):
    """Read receipt schema"""
    conversation_id: int
    message_id: int
    user_id: int


class UserStatus(BaseModel):
    """User status schema"""
    user_id: int
    is_online: bool
    last_seen: Optional[datetime] = None
