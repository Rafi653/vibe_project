"""
Schemas for feedback operations
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class FeedbackBase(BaseModel):
    """Base schema for feedback"""
    message: str = Field(..., min_length=1, max_length=5000)
    name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    is_anonymous: bool = False
    page_url: Optional[str] = Field(None, max_length=500)


class FeedbackCreate(FeedbackBase):
    """Schema for creating feedback"""
    pass


class FeedbackResponse(FeedbackBase):
    """Schema for feedback response"""
    id: int
    user_id: Optional[int] = None
    user_agent: Optional[str] = None
    
    model_config = {
        "from_attributes": True
    }
