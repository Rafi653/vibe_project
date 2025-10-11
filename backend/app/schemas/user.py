"""
Schemas for user management operations
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class UserUpdate(BaseModel):
    """Schema for updating a user (admin only)"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserProfileUpdate(BaseModel):
    """Schema for user updating their own profile"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)


class CoachAssignment(BaseModel):
    """Schema for assigning a coach to a client"""
    client_id: int
    coach_id: int
