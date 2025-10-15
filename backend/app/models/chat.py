"""
Chat models for messaging functionality
"""

from sqlalchemy import String, Text, ForeignKey, Boolean, Enum as SQLEnum, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
import enum

from app.db.base import Base
from app.models.base import TimestampMixin


class ConversationType(str, enum.Enum):
    """Conversation type enumeration"""
    DIRECT = "direct"
    GROUP = "group"


class MessageStatus(str, enum.Enum):
    """Message status enumeration"""
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"


# Association table for conversation participants
conversation_participants = Table(
    'conversation_participants',
    Base.metadata,
    Column('conversation_id', Integer, ForeignKey('conversations.id', ondelete='CASCADE'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
)


class Conversation(Base, TimestampMixin):
    """Conversation model for chat threads"""
    
    __tablename__ = "conversations"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[ConversationType] = mapped_column(
        SQLEnum(ConversationType, values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        default=ConversationType.DIRECT,
        nullable=False
    )
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # For group chats
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    
    # Relationships
    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_id])
    participants: Mapped[List["User"]] = relationship(
        "User",
        secondary=conversation_participants,
        backref="conversations"
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at"
    )
    
    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, type={self.type}, name={self.name})>"


class Message(Base, TimestampMixin):
    """Message model for chat messages"""
    
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id", ondelete='CASCADE'), nullable=False, index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[MessageStatus] = mapped_column(
        SQLEnum(MessageStatus, values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        default=MessageStatus.SENT,
        nullable=False
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id])
    
    def __repr__(self) -> str:
        return f"<Message(id={self.id}, sender_id={self.sender_id}, conversation_id={self.conversation_id})>"


class UserPresence(Base, TimestampMixin):
    """User presence model for online status tracking"""
    
    __tablename__ = "user_presence"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=False, unique=True, index=True)
    is_online: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_seen: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # ISO timestamp
    
    # Relationships
    user: Mapped["User"] = relationship("User", backref="presence")
    
    def __repr__(self) -> str:
        return f"<UserPresence(user_id={self.user_id}, is_online={self.is_online})>"
