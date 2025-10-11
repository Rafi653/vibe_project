"""
Feedback model
"""

from sqlalchemy import String, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.db.base import Base
from app.models.base import TimestampMixin


class Feedback(Base, TimestampMixin):
    """Feedback model for user suggestions and issue reports"""
    
    __tablename__ = "feedback"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    page_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", backref="feedback_submissions")
    
    def __repr__(self) -> str:
        return f"<Feedback(id={self.id}, user_id={self.user_id}, anonymous={self.is_anonymous})>"
