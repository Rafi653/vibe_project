"""
Authentication schemas for request/response validation
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class UserSignup(BaseModel):
    """Schema for user signup request"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=255)
    role: UserRole = Field(default=UserRole.CLIENT)


class UserLogin(BaseModel):
    """Schema for user login request"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    is_verified: bool
    # Common profile fields
    age: Optional[int] = None
    gender: Optional[str] = None
    # Client-specific fields
    height: Optional[float] = None
    weight: Optional[float] = None
    bicep_size: Optional[float] = None
    waist: Optional[float] = None
    target_goals: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    health_complications: Optional[str] = None
    injuries: Optional[str] = None
    gym_access: Optional[str] = None
    supplements: Optional[str] = None
    referral_source: Optional[str] = None
    # Coach-specific fields
    track_record: Optional[str] = None
    experience: Optional[str] = None
    certifications: Optional[str] = None
    competitions: Optional[str] = None
    qualifications: Optional[str] = None
    specialties: Optional[str] = None
    # Custom fields
    custom_fields: Optional[dict] = None
    
    model_config = {
        "from_attributes": True
    }


class UserWithToken(BaseModel):
    """Schema for user response with token"""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
