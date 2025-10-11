"""
WorkoutPlan model
"""

from sqlalchemy import String, Integer, Text, ForeignKey, Date, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base
from app.models.base import TimestampMixin


class PlanStatus(str, enum.Enum):
    """Plan status enumeration"""
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class WorkoutPlan(Base, TimestampMixin):
    """WorkoutPlan model for structured workout programs"""
    
    __tablename__ = "workout_plans"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=True)
    status: Mapped[PlanStatus] = mapped_column(SQLEnum(PlanStatus), default=PlanStatus.ACTIVE, nullable=False)
    duration_weeks: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Store workout details as JSON (can be structured later with separate tables)
    workout_details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="workout_plans")
    
    def __repr__(self) -> str:
        return f"<WorkoutPlan(id={self.id}, user_id={self.user_id}, name={self.name}, status={self.status})>"
