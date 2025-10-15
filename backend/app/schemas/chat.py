"""
Chat schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.models.chat import ConversationType, MessageStatus


# Message Schemas
class MessageCreate(BaseModel):
    """Schema for creating a new message"""
    conversation_id: int
    content: str = Field(..., min_length=1, max_length=5000)


class MessageResponse(BaseModel):
    """Schema for message response"""
    id: int
    conversation_id: int
    sender_id: int
    content: str
    status: MessageStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Conversation Schemas
class ConversationCreate(BaseModel):
    """Schema for creating a new conversation"""
    type: ConversationType = ConversationType.DIRECT
    name: Optional[str] = None
    participant_ids: List[int] = Field(..., min_length=1)


class ConversationResponse(BaseModel):
    """Schema for conversation response"""
    id: int
    type: ConversationType
    name: Optional[str]
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    participant_ids: List[int] = []
    last_message: Optional[MessageResponse] = None

    class Config:
        from_attributes = True


class ConversationDetail(BaseModel):
    """Schema for detailed conversation with messages"""
    id: int
    type: ConversationType
    name: Optional[str]
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    participant_ids: List[int] = []
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True


# User Presence Schemas
class UserPresenceResponse(BaseModel):
    """Schema for user presence response"""
    user_id: int
    is_online: bool
    last_seen: Optional[str]

    class Config:
        from_attributes = True


class ActiveUsersResponse(BaseModel):
    """Schema for active users list"""
    online_users: List[dict]  # Contains id, full_name, email, role


# WebSocket Message Schemas
class WebSocketMessage(BaseModel):
    """Schema for WebSocket messages"""
    type: str  # 'message', 'typing', 'read', 'presence'
    conversation_id: Optional[int] = None
    message: Optional[MessageResponse] = None
    user_id: Optional[int] = None
    is_online: Optional[bool] = None
