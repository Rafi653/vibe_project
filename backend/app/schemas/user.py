"""
Schemas for user management operations
"""

from typing import Optional, Dict, Any
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
    """Schema for client updating their own profile"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    # Common fields
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = Field(None, max_length=50)
    # Client-specific fields
    height: Optional[float] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    bicep_size: Optional[float] = Field(None, gt=0)
    waist: Optional[float] = Field(None, gt=0)
    target_goals: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    health_complications: Optional[str] = None
    injuries: Optional[str] = None
    gym_access: Optional[str] = Field(None, max_length=255)
    supplements: Optional[str] = None
    referral_source: Optional[str] = Field(None, max_length=255)
    custom_fields: Optional[Dict[str, Any]] = None


class CoachProfileUpdate(BaseModel):
    """Schema for coach updating their own profile"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    # Common fields
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = Field(None, max_length=50)
    # Coach-specific fields
    track_record: Optional[str] = None
    experience: Optional[str] = None
    certifications: Optional[str] = None
    competitions: Optional[str] = None
    qualifications: Optional[str] = None
    specialties: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


class CoachAssignment(BaseModel):
    """Schema for assigning a coach to a client"""
    client_id: int
    coach_id: int
