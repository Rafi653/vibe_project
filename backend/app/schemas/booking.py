"""
Booking schemas for API validation
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.models.booking import BookingStatus


class BookingCreate(BaseModel):
    """Schema for creating a booking"""
    coach_id: int
    slot_number: int = Field(..., ge=1, description="Slot number to book")
    scheduled_at: Optional[datetime] = None
    notes: Optional[str] = None


class BookingUpdate(BaseModel):
    """Schema for updating a booking"""
    scheduled_at: Optional[datetime] = None
    status: Optional[BookingStatus] = None
    notes: Optional[str] = None


class BookingResponse(BaseModel):
    """Schema for booking response"""
    id: int
    coach_id: int
    client_id: int
    slot_number: int
    scheduled_at: Optional[datetime] = None
    status: BookingStatus
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class BookingWithDetails(BookingResponse):
    """Schema for booking with user details"""
    coach_name: str
    client_name: str
    
    model_config = {"from_attributes": True}


class CoachAvailability(BaseModel):
    """Schema for coach availability"""
    coach_id: int
    coach_name: str
    strengths: Optional[str] = None
    specialties: Optional[str] = None
    experience: Optional[str] = None
    available_slots: int
    total_slots: int = 10
    booked_slots: int
    
    model_config = {"from_attributes": True}
