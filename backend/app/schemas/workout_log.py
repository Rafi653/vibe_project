"""
Schemas for workout log operations
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class WorkoutLogBase(BaseModel):
    """Base schema for workout log"""
    workout_date: date
    exercise_name: str = Field(..., min_length=1, max_length=255)
    sets: Optional[int] = Field(None, ge=0)
    reps: Optional[int] = Field(None, ge=0)
    weight: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class WorkoutLogCreate(WorkoutLogBase):
    """Schema for creating a workout log"""
    pass


class WorkoutLogUpdate(BaseModel):
    """Schema for updating a workout log"""
    workout_date: Optional[date] = None
    exercise_name: Optional[str] = Field(None, min_length=1, max_length=255)
    sets: Optional[int] = Field(None, ge=0)
    reps: Optional[int] = Field(None, ge=0)
    weight: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class WorkoutLogResponse(WorkoutLogBase):
    """Schema for workout log response"""
    id: int
    user_id: int
    
    model_config = {
        "from_attributes": True
    }
