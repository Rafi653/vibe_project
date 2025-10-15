"""
Chat models for real-time messaging
"""

from sqlalchemy import String, Boolean, Integer, ForeignKey, Text, Enum as SQLEnum, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
import enum

from app.db.base import Base
from app.models.base import TimestampMixin


class MessageType(str, enum.Enum):
    """Message type enumeration"""
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"


class ChatRoomType(str, enum.Enum):
    """Chat room type enumeration"""
    DIRECT = "direct"
    GROUP = "group"


# Association table for chat room participants
chat_participants = Table(
    'chat_participants',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('chat_room_id', Integer, ForeignKey('chat_rooms.id', ondelete='CASCADE'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    Column('joined_at', Integer, nullable=False),  # Unix timestamp
    Column('last_read_at', Integer, nullable=True),  # Unix timestamp
)


class ChatRoom(Base, TimestampMixin):
    """Chat room model for 1:1 and group chats"""
    
    __tablename__ = "chat_rooms"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # For group chats
    type: Mapped[ChatRoomType] = mapped_column(
        SQLEnum(ChatRoomType, values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        default=ChatRoomType.DIRECT,
        nullable=False
    )
    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="chat_room", cascade="all, delete-orphan"
    )
    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_id])
    
    def __repr__(self) -> str:
        return f"<ChatRoom(id={self.id}, type={self.type}, name={self.name})>"


class Message(Base, TimestampMixin):
    """Message model for chat messages"""
    
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chat_room_id: Mapped[int] = mapped_column(Integer, ForeignKey('chat_rooms.id', ondelete='CASCADE'), nullable=False, index=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[MessageType] = mapped_column(
        SQLEnum(MessageType, values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        default=MessageType.TEXT,
        nullable=False
    )
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relationships
    chat_room: Mapped["ChatRoom"] = relationship("ChatRoom", back_populates="messages")
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id])
    
    def __repr__(self) -> str:
        return f"<Message(id={self.id}, sender_id={self.sender_id}, type={self.message_type})>"


class UserPresence(Base):
    """User presence model for online status tracking"""
    
    __tablename__ = "user_presence"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, index=True)
    is_online: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_seen: Mapped[int] = mapped_column(Integer, nullable=False)  # Unix timestamp
    
    # Relationship
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    
    def __repr__(self) -> str:
        return f"<UserPresence(user_id={self.user_id}, is_online={self.is_online})>"
