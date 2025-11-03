"""
Chat schemas for API validation
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from app.models.chat import MessageType, ChatRoomType


class MessageCreate(BaseModel):
    """Schema for creating a message"""
    chat_room_id: int
    content: str = Field(..., min_length=1, max_length=5000)
    message_type: MessageType = MessageType.TEXT


class MessageUpdate(BaseModel):
    """Schema for updating a message"""
    content: str = Field(..., min_length=1, max_length=5000)


class MessageResponse(BaseModel):
    """Schema for message response"""
    id: int
    chat_room_id: int
    sender_id: int
    sender_name: str
    content: str
    message_type: MessageType
    is_edited: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class ChatRoomCreate(BaseModel):
    """Schema for creating a chat room"""
    name: Optional[str] = None
    type: ChatRoomType = ChatRoomType.DIRECT
    participant_ids: List[int] = Field(..., min_length=1)


class ChatRoomResponse(BaseModel):
    """Schema for chat room response"""
    id: int
    name: Optional[str]
    type: ChatRoomType
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    participant_count: int
    last_message: Optional[str] = None
    last_message_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


class ChatRoomWithMessages(ChatRoomResponse):
    """Schema for chat room with messages"""
    messages: List[MessageResponse]
    participants: List[int]


class UserPresenceResponse(BaseModel):
    """Schema for user presence response"""
    user_id: int
    user_name: str
    is_online: bool
    last_seen: datetime
    
    model_config = {"from_attributes": True}


class ChatParticipantAdd(BaseModel):
    """Schema for adding participants to a chat room"""
    user_ids: List[int] = Field(..., min_length=1)


class MarkAsReadRequest(BaseModel):
    """Schema for marking messages as read"""
    chat_room_id: int


class WebSocketMessage(BaseModel):
    """Schema for WebSocket messages"""
    type: str  # 'message', 'typing', 'read', 'presence'
    data: dict
