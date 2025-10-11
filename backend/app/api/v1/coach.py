"""
Coach endpoints - for coaches to manage clients and plans
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from datetime import date, timedelta
from typing import List, Optional

from app.db.base import get_db
from app.core.dependencies import require_coach
from app.models.user import User, UserRole
from app.models.workout_log import WorkoutLog
from app.models.diet_log import DietLog
from app.models.workout_plan import WorkoutPlan
from app.models.diet_plan import DietPlan
from app.schemas.workout_log import WorkoutLogResponse
from app.schemas.diet_log import DietLogResponse
from app.schemas.workout_plan import WorkoutPlanCreate, WorkoutPlanUpdate, WorkoutPlanResponse
from app.schemas.diet_plan import DietPlanCreate, DietPlanUpdate, DietPlanResponse
from app.schemas.auth import UserResponse
from app.schemas.user import CoachProfileUpdate

router = APIRouter()


# Client Management
@router.get("/clients", response_model=List[UserResponse])
async def get_clients(
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get list of all clients connected to the coach through bookings"""
    # For coaches, only show clients they have bookings with
    # For admins, show all clients
    if current_user.role == UserRole.COACH:
        from app.models.booking import Booking
        # Get unique client IDs from bookings
        result = await db.execute(
            select(User)
            .join(Booking, User.id == Booking.client_id)
            .where(Booking.coach_id == current_user.id)
            .distinct()
            .order_by(User.full_name)
        )
    else:
        # Admin can see all clients
        result = await db.execute(
            select(User)
            .where(User.role == UserRole.CLIENT)
            .order_by(User.full_name)
        )
    return result.scalars().all()


@router.get("/clients/{client_id}", response_model=UserResponse)
async def get_client(
    client_id: int,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific client's profile (only if connected through booking)"""
    # Verify client exists
    result = await db.execute(
        select(User).where(
            and_(User.id == client_id, User.role == UserRole.CLIENT)
        )
    )
    client = result.scalar_one_or_none()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # For coaches, verify they have a booking with this client
    if current_user.role == UserRole.COACH:
        from app.models.booking import Booking
        booking_check = await db.execute(
            select(Booking).where(
                and_(
                    Booking.coach_id == current_user.id,
                    Booking.client_id == client_id
                )
            )
        )
        if not booking_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view profiles of clients you're connected with through bookings"
            )
    
    return client


# View Client Workout Logs
@router.get("/clients/{client_id}/workout-logs", response_model=List[WorkoutLogResponse])
async def get_client_workout_logs(
    client_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get workout logs for a specific client (only if connected through booking)"""
    # Verify client exists
    client_result = await db.execute(
        select(User).where(
            and_(User.id == client_id, User.role == UserRole.CLIENT)
        )
    )
    if not client_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # For coaches, verify they have a booking with this client
    if current_user.role == UserRole.COACH:
        from app.models.booking import Booking
        booking_check = await db.execute(
            select(Booking).where(
                and_(
                    Booking.coach_id == current_user.id,
                    Booking.client_id == client_id
                )
            )
        )
        if not booking_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view logs of clients you're connected with through bookings"
            )
    
    query = select(WorkoutLog).where(WorkoutLog.user_id == client_id)
    
    if start_date:
        query = query.where(WorkoutLog.workout_date >= start_date)
    if end_date:
        query = query.where(WorkoutLog.workout_date <= end_date)
    
    query = query.order_by(WorkoutLog.workout_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


# View Client Diet Logs
@router.get("/clients/{client_id}/diet-logs", response_model=List[DietLogResponse])
async def get_client_diet_logs(
    client_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get diet logs for a specific client (only if connected through booking)"""
    # Verify client exists
    client_result = await db.execute(
        select(User).where(
            and_(User.id == client_id, User.role == UserRole.CLIENT)
        )
    )
    if not client_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # For coaches, verify they have a booking with this client
    if current_user.role == UserRole.COACH:
        from app.models.booking import Booking
        booking_check = await db.execute(
            select(Booking).where(
                and_(
                    Booking.coach_id == current_user.id,
                    Booking.client_id == client_id
                )
            )
        )
        if not booking_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view logs of clients you're connected with through bookings"
            )
    
    query = select(DietLog).where(DietLog.user_id == client_id)
    
    if start_date:
        query = query.where(DietLog.meal_date >= start_date)
    if end_date:
        query = query.where(DietLog.meal_date <= end_date)
    
    query = query.order_by(DietLog.meal_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


# Client Progress
@router.get("/clients/{client_id}/progress")
async def get_client_progress(
    client_id: int,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get progress metrics for a specific client (only if connected through booking)"""
    # Verify client exists
    client_result = await db.execute(
        select(User).where(
            and_(User.id == client_id, User.role == UserRole.CLIENT)
        )
    )
    if not client_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # For coaches, verify they have a booking with this client
    if current_user.role == UserRole.COACH:
        from app.models.booking import Booking
        booking_check = await db.execute(
            select(Booking).where(
                and_(
                    Booking.coach_id == current_user.id,
                    Booking.client_id == client_id
                )
            )
        )
        if not booking_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view progress of clients you're connected with through bookings"
            )
    
    # Get statistics
    thirty_days_ago = date.today() - timedelta(days=30)
    
    workout_count = await db.execute(
        select(func.count(WorkoutLog.id))
        .where(
            and_(
                WorkoutLog.user_id == client_id,
                WorkoutLog.workout_date >= thirty_days_ago
            )
        )
    )
    
    diet_count = await db.execute(
        select(func.count(DietLog.id))
        .where(
            and_(
                DietLog.user_id == client_id,
                DietLog.meal_date >= thirty_days_ago
            )
        )
    )
    
    return {
        "client_id": client_id,
        "last_30_days": {
            "workout_sessions": workout_count.scalar() or 0,
            "diet_logs": diet_count.scalar() or 0
        }
    }


# Workout Plan Management
@router.post("/workout-plans", response_model=WorkoutPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_workout_plan(
    plan_data: WorkoutPlanCreate,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Create a workout plan for a client"""
    # Verify the target user is a client
    user_result = await db.execute(
        select(User).where(
            and_(User.id == plan_data.user_id, User.role == UserRole.CLIENT)
        )
    )
    if not user_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    workout_plan = WorkoutPlan(**plan_data.model_dump())
    db.add(workout_plan)
    await db.commit()
    await db.refresh(workout_plan)
    return workout_plan


@router.get("/workout-plans", response_model=List[WorkoutPlanResponse])
async def get_all_workout_plans(
    client_id: Optional[int] = None,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get all workout plans, optionally filtered by client"""
    query = select(WorkoutPlan)
    
    if client_id:
        query = query.where(WorkoutPlan.user_id == client_id)
    
    query = query.order_by(WorkoutPlan.start_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.put("/workout-plans/{plan_id}", response_model=WorkoutPlanResponse)
async def update_workout_plan(
    plan_id: int,
    plan_data: WorkoutPlanUpdate,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Update a workout plan"""
    result = await db.execute(
        select(WorkoutPlan).where(WorkoutPlan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found"
        )
    
    update_data = plan_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)
    
    await db.commit()
    await db.refresh(plan)
    return plan


@router.delete("/workout-plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout_plan(
    plan_id: int,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Delete a workout plan"""
    result = await db.execute(
        select(WorkoutPlan).where(WorkoutPlan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found"
        )
    
    await db.delete(plan)
    await db.commit()


# Diet Plan Management
@router.post("/diet-plans", response_model=DietPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_diet_plan(
    plan_data: DietPlanCreate,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Create a diet plan for a client"""
    # Verify the target user is a client
    user_result = await db.execute(
        select(User).where(
            and_(User.id == plan_data.user_id, User.role == UserRole.CLIENT)
        )
    )
    if not user_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    diet_plan = DietPlan(**plan_data.model_dump())
    db.add(diet_plan)
    await db.commit()
    await db.refresh(diet_plan)
    return diet_plan


@router.get("/diet-plans", response_model=List[DietPlanResponse])
async def get_all_diet_plans(
    client_id: Optional[int] = None,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get all diet plans, optionally filtered by client"""
    query = select(DietPlan)
    
    if client_id:
        query = query.where(DietPlan.user_id == client_id)
    
    query = query.order_by(DietPlan.start_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.put("/diet-plans/{plan_id}", response_model=DietPlanResponse)
async def update_diet_plan(
    plan_id: int,
    plan_data: DietPlanUpdate,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Update a diet plan"""
    result = await db.execute(
        select(DietPlan).where(DietPlan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet plan not found"
        )
    
    update_data = plan_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)
    
    await db.commit()
    await db.refresh(plan)
    return plan


@router.delete("/diet-plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diet_plan(
    plan_id: int,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Delete a diet plan"""
    result = await db.execute(
        select(DietPlan).where(DietPlan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet plan not found"
        )
    
    await db.delete(plan)
    await db.commit()


# Chart Data Endpoints
@router.get("/charts/client-overview")
async def get_client_overview_chart(
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get overview of client activity for coach dashboard"""
    thirty_days_ago = date.today() - timedelta(days=30)
    
    # Get all clients
    clients_result = await db.execute(
        select(User)
        .where(User.role == UserRole.CLIENT)
    )
    clients = clients_result.scalars().all()
    
    client_data = []
    for client in clients:
        # Get workout count
        workout_count = await db.execute(
            select(func.count(WorkoutLog.id))
            .where(
                and_(
                    WorkoutLog.user_id == client.id,
                    WorkoutLog.workout_date >= thirty_days_ago
                )
            )
        )
        
        # Get diet log count
        diet_count = await db.execute(
            select(func.count(DietLog.id))
            .where(
                and_(
                    DietLog.user_id == client.id,
                    DietLog.meal_date >= thirty_days_ago
                )
            )
        )
        
        # Get active plans
        active_plans = await db.execute(
            select(func.count(WorkoutPlan.id))
            .where(
                and_(
                    WorkoutPlan.user_id == client.id,
                    WorkoutPlan.status == "active"
                )
            )
        )
        
        client_data.append({
            "client_name": client.full_name,
            "client_id": client.id,
            "workouts": workout_count.scalar() or 0,
            "diet_logs": diet_count.scalar() or 0,
            "active_plans": active_plans.scalar() or 0
        })
    
    return {"clients": client_data}


@router.get("/charts/engagement")
async def get_engagement_chart(
    days: int = 30,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get client engagement metrics over time"""
    start_date = date.today() - timedelta(days=days)
    
    # Get daily workout logs across all clients
    workout_result = await db.execute(
        select(
            WorkoutLog.workout_date,
            func.count(WorkoutLog.id).label('count')
        )
        .join(User, WorkoutLog.user_id == User.id)
        .where(
            and_(
                User.role == UserRole.CLIENT,
                WorkoutLog.workout_date >= start_date
            )
        )
        .group_by(WorkoutLog.workout_date)
        .order_by(WorkoutLog.workout_date)
    )
    workout_data = workout_result.all()
    
    # Get daily diet logs across all clients
    diet_result = await db.execute(
        select(
            DietLog.meal_date,
            func.count(DietLog.id).label('count')
        )
        .join(User, DietLog.user_id == User.id)
        .where(
            and_(
                User.role == UserRole.CLIENT,
                DietLog.meal_date >= start_date
            )
        )
        .group_by(DietLog.meal_date)
        .order_by(DietLog.meal_date)
    )
    diet_data = diet_result.all()
    
    return {
        "workouts": {
            "labels": [row.workout_date.isoformat() for row in workout_data],
            "data": [row.count for row in workout_data]
        },
        "diet_logs": {
            "labels": [row.meal_date.isoformat() for row in diet_data],
            "data": [row.count for row in diet_data]
        }
    }


@router.get("/charts/plan-assignments")
async def get_plan_assignments_chart(
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Get plan assignment statistics"""
    # Count plans by status
    workout_plan_result = await db.execute(
        select(
            WorkoutPlan.status,
            func.count(WorkoutPlan.id).label('count')
        )
        .group_by(WorkoutPlan.status)
    )
    
    diet_plan_result = await db.execute(
        select(
            DietPlan.status,
            func.count(DietPlan.id).label('count')
        )
        .group_by(DietPlan.status)
    )
    
    workout_plans = {row.status: row.count for row in workout_plan_result.all()}
    diet_plans = {row.status: row.count for row in diet_plan_result.all()}
    
    return {
        "workout_plans": workout_plans,
        "diet_plans": diet_plans
    }


# Profile management
@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(require_coach),
):
    """Get coach's own profile"""
    return UserResponse.model_validate(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: CoachProfileUpdate,
    current_user: User = Depends(require_coach),
    db: AsyncSession = Depends(get_db)
):
    """Update coach's own profile"""
    update_data = profile_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    return UserResponse.model_validate(current_user)
