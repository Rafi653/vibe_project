"""
WorkoutLog model
"""

from sqlalchemy import String, Integer, Float, Text, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import TimestampMixin


class WorkoutLog(Base, TimestampMixin):
    """WorkoutLog model for tracking user workouts"""
    
    __tablename__ = "workout_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    workout_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    exercise_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sets: Mapped[int] = mapped_column(Integer, nullable=True)
    reps: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)  # in kg or lbs
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="workout_logs")
    
    def __repr__(self) -> str:
        return f"<WorkoutLog(id={self.id}, user_id={self.user_id}, exercise={self.exercise_name}, date={self.workout_date})>"
