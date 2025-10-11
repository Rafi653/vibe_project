"""
DietPlan model
"""

from sqlalchemy import String, Integer, Float, Text, ForeignKey, Date, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.db.base import Base
from app.models.base import TimestampMixin
from app.models.workout_plan import PlanStatus  # Reuse the same status enum


class DietPlan(Base, TimestampMixin):
    """DietPlan model for structured diet programs"""
    
    __tablename__ = "diet_plans"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=True)
    status: Mapped[PlanStatus] = mapped_column(SQLEnum(PlanStatus), default=PlanStatus.ACTIVE, nullable=False)
    
    # Nutritional targets
    target_calories: Mapped[float] = mapped_column(Float, nullable=True)
    target_protein_grams: Mapped[float] = mapped_column(Float, nullable=True)
    target_carbs_grams: Mapped[float] = mapped_column(Float, nullable=True)
    target_fat_grams: Mapped[float] = mapped_column(Float, nullable=True)
    
    # Store meal plan details as JSON (can be structured later with separate tables)
    meal_plan_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="diet_plans")
    
    def __repr__(self) -> str:
        return f"<DietPlan(id={self.id}, user_id={self.user_id}, name={self.name}, status={self.status})>"
