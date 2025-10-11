"""
Schemas for workout plan operations
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

from app.models.workout_plan import PlanStatus


class WorkoutPlanBase(BaseModel):
    """Base schema for workout plan"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    duration_weeks: Optional[int] = Field(None, ge=1)
    workout_details: Optional[dict] = None


class WorkoutPlanCreate(WorkoutPlanBase):
    """Schema for creating a workout plan"""
    user_id: int = Field(..., description="ID of the user this plan is for")


class WorkoutPlanUpdate(BaseModel):
    """Schema for updating a workout plan"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[PlanStatus] = None
    duration_weeks: Optional[int] = Field(None, ge=1)
    workout_details: Optional[dict] = None


class WorkoutPlanResponse(WorkoutPlanBase):
    """Schema for workout plan response"""
    id: int
    user_id: int
    status: PlanStatus
    
    model_config = {
        "from_attributes": True
    }
