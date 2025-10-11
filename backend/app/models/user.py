"""
User model
"""

from sqlalchemy import String, Boolean, Enum as SQLEnum, Integer, Float, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, Dict, Any
import enum

from app.db.base import Base
from app.models.base import TimestampMixin


class UserRole(str, enum.Enum):
    """User role enumeration"""
    CLIENT = "client"
    COACH = "coach"
    ADMIN = "admin"


class User(Base, TimestampMixin):
    """User model for authentication and profile"""
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, values_callable=lambda enum_cls: [e.value for e in enum_cls]), default=UserRole.CLIENT, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Common profile fields
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Client-specific profile fields
    height: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bicep_size: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    waist: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    target_goals: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dietary_restrictions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    health_complications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    injuries: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    gym_access: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    supplements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    referral_source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Coach-specific profile fields
    track_record: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    experience: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    certifications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    competitions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    qualifications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    specialties: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    strengths: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    available_slots: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    
    # Custom fields for extensibility
    custom_fields: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    workout_logs: Mapped[list["WorkoutLog"]] = relationship(
        "WorkoutLog", back_populates="user", cascade="all, delete-orphan"
    )
    diet_logs: Mapped[list["DietLog"]] = relationship(
        "DietLog", back_populates="user", cascade="all, delete-orphan"
    )
    workout_plans: Mapped[list["WorkoutPlan"]] = relationship(
        "WorkoutPlan", back_populates="user", cascade="all, delete-orphan"
    )
    diet_plans: Mapped[list["DietPlan"]] = relationship(
        "DietPlan", back_populates="user", cascade="all, delete-orphan"
    )
    coach_bookings: Mapped[list["Booking"]] = relationship(
        "Booking", foreign_keys="[Booking.coach_id]", back_populates="coach", cascade="all, delete-orphan"
    )
    client_bookings: Mapped[list["Booking"]] = relationship(
        "Booking", foreign_keys="[Booking.client_id]", back_populates="client", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
