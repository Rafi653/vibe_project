"""
Booking model for coach-client training sessions
"""

from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
import enum

from app.db.base import Base
from app.models.base import TimestampMixin


class BookingStatus(str, enum.Enum):
    """Booking status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Booking(Base, TimestampMixin):
    """Booking model for personal training sessions"""
    
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    coach_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    slot_number: Mapped[int] = mapped_column(Integer, nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[BookingStatus] = mapped_column(
        SQLEnum(BookingStatus, values_callable=lambda enum_cls: [e.value for e in enum_cls]), 
        default=BookingStatus.PENDING, 
        nullable=False
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    coach: Mapped["User"] = relationship("User", foreign_keys=[coach_id], back_populates="coach_bookings")
    client: Mapped["User"] = relationship("User", foreign_keys=[client_id], back_populates="client_bookings")
    
    def __repr__(self) -> str:
        return f"<Booking(id={self.id}, coach_id={self.coach_id}, client_id={self.client_id}, status={self.status})>"
