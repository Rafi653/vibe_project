"""
Schemas for diet plan operations
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

from app.models.workout_plan import PlanStatus


class DietPlanBase(BaseModel):
    """Base schema for diet plan"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    target_calories: Optional[float] = Field(None, ge=0)
    target_protein_grams: Optional[float] = Field(None, ge=0)
    target_carbs_grams: Optional[float] = Field(None, ge=0)
    target_fat_grams: Optional[float] = Field(None, ge=0)
    meal_plan_details: Optional[dict] = None


class DietPlanCreate(DietPlanBase):
    """Schema for creating a diet plan"""
    user_id: int = Field(..., description="ID of the user this plan is for")


class DietPlanUpdate(BaseModel):
    """Schema for updating a diet plan"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[PlanStatus] = None
    target_calories: Optional[float] = Field(None, ge=0)
    target_protein_grams: Optional[float] = Field(None, ge=0)
    target_carbs_grams: Optional[float] = Field(None, ge=0)
    target_fat_grams: Optional[float] = Field(None, ge=0)
    meal_plan_details: Optional[dict] = None


class DietPlanResponse(DietPlanBase):
    """Schema for diet plan response"""
    id: int
    user_id: int
    status: PlanStatus
    
    model_config = {
        "from_attributes": True
    }
