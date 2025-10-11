"""
DietLog model
"""

from sqlalchemy import String, Integer, Float, Text, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from typing import Optional

from app.db.base import Base
from app.models.base import TimestampMixin


class MealType(str, enum.Enum):
    """Meal type enumeration"""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class DietLog(Base, TimestampMixin):
    """DietLog model for tracking user meals and nutrition"""
    
    __tablename__ = "diet_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    meal_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    meal_type: Mapped[MealType] = mapped_column(SQLEnum(MealType, values_callable=lambda enum_cls: [e.value for e in enum_cls]), nullable=False)
    food_name: Mapped[str] = mapped_column(String(255), nullable=False)
    calories: Mapped[float] = mapped_column(Float, nullable=True)
    protein_grams: Mapped[float] = mapped_column(Float, nullable=True)
    carbs_grams: Mapped[float] = mapped_column(Float, nullable=True)
    fat_grams: Mapped[float] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="diet_logs")
    
    def __repr__(self) -> str:
        return f"<DietLog(id={self.id}, user_id={self.user_id}, food={self.food_name}, date={self.meal_date})>"
