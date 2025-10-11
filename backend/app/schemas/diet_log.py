"""
Schemas for diet log operations
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

from app.models.diet_log import MealType


class DietLogBase(BaseModel):
    """Base schema for diet log"""
    meal_date: date
    meal_type: MealType
    food_name: str = Field(..., min_length=1, max_length=255)
    calories: Optional[float] = Field(None, ge=0)
    protein_grams: Optional[float] = Field(None, ge=0)
    carbs_grams: Optional[float] = Field(None, ge=0)
    fat_grams: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class DietLogCreate(DietLogBase):
    """Schema for creating a diet log"""
    pass


class DietLogUpdate(BaseModel):
    """Schema for updating a diet log"""
    meal_date: Optional[date] = None
    meal_type: Optional[MealType] = None
    food_name: Optional[str] = Field(None, min_length=1, max_length=255)
    calories: Optional[float] = Field(None, ge=0)
    protein_grams: Optional[float] = Field(None, ge=0)
    carbs_grams: Optional[float] = Field(None, ge=0)
    fat_grams: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class DietLogResponse(DietLogBase):
    """Schema for diet log response"""
    id: int
    user_id: int
    
    model_config = {
        "from_attributes": True
    }
