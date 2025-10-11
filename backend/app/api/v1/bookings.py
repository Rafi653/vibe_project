"""
Booking endpoints - for managing coach-client training sessions
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import List

from app.db.base import get_db
from app.core.dependencies import get_current_active_user, require_coach, require_admin
from app.models.user import User, UserRole
from app.models.booking import Booking, BookingStatus
from app.schemas.booking import (
    BookingCreate, 
    BookingUpdate, 
    BookingResponse, 
    BookingWithDetails,
    CoachAvailability
)

router = APIRouter()


# Client endpoints
@router.get("/coaches", response_model=List[CoachAvailability])
async def get_available_coaches(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of all coaches with their availability"""
    # Get all coaches
    result = await db.execute(
        select(User)
        .where(User.role == UserRole.COACH)
        .order_by(User.full_name)
    )
    coaches = result.scalars().all()
    
    # Get booking counts for each coach
    coach_availability = []
    for coach in coaches:
        # Count confirmed and pending bookings
        booking_count_result = await db.execute(
            select(func.count(Booking.id))
            .where(
                and_(
                    Booking.coach_id == coach.id,
                    Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING])
                )
            )
        )
        booked_slots = booking_count_result.scalar() or 0
        
        coach_availability.append(CoachAvailability(
            coach_id=coach.id,
            coach_name=coach.full_name,
            strengths=coach.strengths,
            specialties=coach.specialties,
            experience=coach.experience,
            available_slots=coach.available_slots,
            total_slots=10,
            booked_slots=booked_slots
        ))
    
    return coach_availability


@router.get("/coaches/{coach_id}", response_model=CoachAvailability)
async def get_coach_availability(
    coach_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific coach's profile and availability"""
    # Get coach
    result = await db.execute(
        select(User).where(
            and_(User.id == coach_id, User.role == UserRole.COACH)
        )
    )
    coach = result.scalar_one_or_none()
    
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coach not found"
        )
    
    # Count confirmed and pending bookings
    booking_count_result = await db.execute(
        select(func.count(Booking.id))
        .where(
            and_(
                Booking.coach_id == coach.id,
                Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING])
            )
        )
    )
    booked_slots = booking_count_result.scalar() or 0
    
    return CoachAvailability(
        coach_id=coach.id,
        coach_name=coach.full_name,
        strengths=coach.strengths,
        specialties=coach.specialties,
        experience=coach.experience,
        available_slots=coach.available_slots,
        total_slots=10,
        booked_slots=booked_slots
    )


@router.post("/book", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def book_training_slot(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Book a training slot with a coach (client only)"""
    # Only clients can book
    if current_user.role != UserRole.CLIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only clients can book training slots"
        )
    
    # Verify coach exists
    coach_result = await db.execute(
        select(User).where(
            and_(User.id == booking_data.coach_id, User.role == UserRole.COACH)
        )
    )
    coach = coach_result.scalar_one_or_none()
    
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coach not found"
        )
    
    # Check if coach has available slots
    if coach.available_slots <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coach has no available slots"
        )
    
    # Check if slot number is already booked by this client with this coach
    existing_booking = await db.execute(
        select(Booking).where(
            and_(
                Booking.coach_id == booking_data.coach_id,
                Booking.client_id == current_user.id,
                Booking.slot_number == booking_data.slot_number,
                Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING])
            )
        )
    )
    if existing_booking.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already booked this slot with this coach"
        )
    
    # Create booking
    booking = Booking(
        coach_id=booking_data.coach_id,
        client_id=current_user.id,
        slot_number=booking_data.slot_number,
        scheduled_at=booking_data.scheduled_at,
        status=BookingStatus.PENDING,
        notes=booking_data.notes
    )
    
    db.add(booking)
    
    # Update coach's available slots
    coach.available_slots -= 1
    
    await db.commit()
    await db.refresh(booking)
    
    return booking


@router.get("/my-bookings", response_model=List[BookingWithDetails])
async def get_my_bookings(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all bookings for the current user (client or coach)"""
    if current_user.role == UserRole.CLIENT:
        # Get bookings as client
        result = await db.execute(
            select(Booking)
            .where(Booking.client_id == current_user.id)
            .order_by(Booking.created_at.desc())
        )
    elif current_user.role == UserRole.COACH:
        # Get bookings as coach
        result = await db.execute(
            select(Booking)
            .where(Booking.coach_id == current_user.id)
            .order_by(Booking.created_at.desc())
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only clients and coaches can view bookings"
        )
    
    bookings = result.scalars().all()
    
    # Enrich bookings with user details
    bookings_with_details = []
    for booking in bookings:
        # Get coach and client names
        coach_result = await db.execute(select(User).where(User.id == booking.coach_id))
        client_result = await db.execute(select(User).where(User.id == booking.client_id))
        
        coach = coach_result.scalar_one_or_none()
        client = client_result.scalar_one_or_none()
        
        booking_dict = {
            "id": booking.id,
            "coach_id": booking.coach_id,
            "client_id": booking.client_id,
            "slot_number": booking.slot_number,
            "scheduled_at": booking.scheduled_at,
            "status": booking.status,
            "notes": booking.notes,
            "created_at": booking.created_at,
            "updated_at": booking.updated_at,
            "coach_name": coach.full_name if coach else "Unknown",
            "client_name": client.full_name if client else "Unknown"
        }
        bookings_with_details.append(BookingWithDetails(**booking_dict))
    
    return bookings_with_details


@router.put("/bookings/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a booking (coach can confirm/complete, client can cancel)"""
    # Get booking
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id)
    )
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CLIENT:
        # Client can only cancel their own bookings
        if booking.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own bookings"
            )
        # Client can only cancel
        if booking_data.status and booking_data.status != BookingStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Clients can only cancel bookings"
            )
    elif current_user.role == UserRole.COACH:
        # Coach can only update their own bookings
        if booking.coach_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own bookings"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only clients and coaches can update bookings"
        )
    
    # Update booking
    update_data = booking_data.model_dump(exclude_unset=True)
    
    # If status is being changed to cancelled, restore coach's available slot
    if "status" in update_data and update_data["status"] == BookingStatus.CANCELLED:
        if booking.status in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
            coach_result = await db.execute(select(User).where(User.id == booking.coach_id))
            coach = coach_result.scalar_one_or_none()
            if coach:
                coach.available_slots += 1
    
    for field, value in update_data.items():
        setattr(booking, field, value)
    
    await db.commit()
    await db.refresh(booking)
    
    return booking


# Coach endpoints
@router.get("/coach/bookings", response_model=List[BookingWithDetails])
async def get_coach_bookings(
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get all bookings for the current coach"""
    result = await db.execute(
        select(Booking)
        .where(Booking.coach_id == current_user.id)
        .order_by(Booking.scheduled_at.desc())
    )
    bookings = result.scalars().all()
    
    # Enrich with client names
    bookings_with_details = []
    for booking in bookings:
        client_result = await db.execute(select(User).where(User.id == booking.client_id))
        client = client_result.scalar_one_or_none()
        
        booking_dict = {
            "id": booking.id,
            "coach_id": booking.coach_id,
            "client_id": booking.client_id,
            "slot_number": booking.slot_number,
            "scheduled_at": booking.scheduled_at,
            "status": booking.status,
            "notes": booking.notes,
            "created_at": booking.created_at,
            "updated_at": booking.updated_at,
            "coach_name": current_user.full_name,
            "client_name": client.full_name if client else "Unknown"
        }
        bookings_with_details.append(BookingWithDetails(**booking_dict))
    
    return bookings_with_details


# Admin endpoints
@router.get("/admin/bookings", response_model=List[BookingWithDetails])
async def get_all_bookings(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get all bookings (admin only)"""
    result = await db.execute(
        select(Booking).order_by(Booking.created_at.desc())
    )
    bookings = result.scalars().all()
    
    # Enrich with user names
    bookings_with_details = []
    for booking in bookings:
        coach_result = await db.execute(select(User).where(User.id == booking.coach_id))
        client_result = await db.execute(select(User).where(User.id == booking.client_id))
        
        coach = coach_result.scalar_one_or_none()
        client = client_result.scalar_one_or_none()
        
        booking_dict = {
            "id": booking.id,
            "coach_id": booking.coach_id,
            "client_id": booking.client_id,
            "slot_number": booking.slot_number,
            "scheduled_at": booking.scheduled_at,
            "status": booking.status,
            "notes": booking.notes,
            "created_at": booking.created_at,
            "updated_at": booking.updated_at,
            "coach_name": coach.full_name if coach else "Unknown",
            "client_name": client.full_name if client else "Unknown"
        }
        bookings_with_details.append(BookingWithDetails(**booking_dict))
    
    return bookings_with_details


@router.get("/admin/coaches/{coach_id}/bookings", response_model=List[BookingWithDetails])
async def get_coach_calendar(
    coach_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get all bookings for a specific coach (admin only)"""
    # Verify coach exists
    coach_result = await db.execute(
        select(User).where(and_(User.id == coach_id, User.role == UserRole.COACH))
    )
    coach = coach_result.scalar_one_or_none()
    
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coach not found"
        )
    
    result = await db.execute(
        select(Booking)
        .where(Booking.coach_id == coach_id)
        .order_by(Booking.scheduled_at.desc())
    )
    bookings = result.scalars().all()
    
    # Enrich with client names
    bookings_with_details = []
    for booking in bookings:
        client_result = await db.execute(select(User).where(User.id == booking.client_id))
        client = client_result.scalar_one_or_none()
        
        booking_dict = {
            "id": booking.id,
            "coach_id": booking.coach_id,
            "client_id": booking.client_id,
            "slot_number": booking.slot_number,
            "scheduled_at": booking.scheduled_at,
            "status": booking.status,
            "notes": booking.notes,
            "created_at": booking.created_at,
            "updated_at": booking.updated_at,
            "coach_name": coach.full_name,
            "client_name": client.full_name if client else "Unknown"
        }
        bookings_with_details.append(BookingWithDetails(**booking_dict))
    
    return bookings_with_details
