"""
User model
"""

from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.CLIENT, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
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
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
