"""
Chat models for real-time messaging
"""

from sqlalchemy import String, Boolean, Integer, Text, ForeignKey, Enum as SQLEnum, Index, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
import enum

from app.db.base import Base
from app.models.base import TimestampMixin


class ConversationType(str, enum.Enum):
    """Conversation type enumeration"""
    DIRECT = "direct"
    GROUP = "group"


class Conversation(Base, TimestampMixin):
    """Conversation model for chat sessions"""
    
    __tablename__ = "conversations"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # For group chats
    conversation_type: Mapped[ConversationType] = mapped_column(
        SQLEnum(ConversationType, values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        default=ConversationType.DIRECT,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relationships
    participants: Mapped[list["ConversationParticipant"]] = relationship(
        "ConversationParticipant", back_populates="conversation", cascade="all, delete-orphan"
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, type={self.conversation_type})>"


class ConversationParticipant(Base, TimestampMixin):
    """Participant in a conversation"""
    
    __tablename__ = "conversation_participants"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)  # For group chats
    last_read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)  # For read receipts
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="participants")
    user: Mapped["User"] = relationship("User")
    
    # Composite index for faster lookups
    __table_args__ = (
        Index('idx_conversation_user', 'conversation_id', 'user_id'),
    )
    
    def __repr__(self) -> str:
        return f"<ConversationParticipant(conversation_id={self.conversation_id}, user_id={self.user_id})>"


class Message(Base, TimestampMixin):
    """Message model for chat messages"""
    
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), nullable=False, index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
    sender: Mapped["User"] = relationship("User")
    
    # Composite index for faster message retrieval
    __table_args__ = (
        Index('idx_conversation_created', 'conversation_id', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<Message(id={self.id}, conversation_id={self.conversation_id}, sender_id={self.sender_id})>"
