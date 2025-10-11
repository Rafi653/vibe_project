"""
Admin endpoints - for system administration and management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import date, timedelta
from typing import List

from app.db.base import get_db
from app.core.dependencies import require_admin
from app.models.user import User, UserRole
from app.models.workout_log import WorkoutLog
from app.models.diet_log import DietLog
from app.models.workout_plan import WorkoutPlan
from app.models.diet_plan import DietPlan
from app.schemas.user import UserUpdate
from app.schemas.auth import UserResponse

router = APIRouter()


# User Management
@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    role: UserRole = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get all users, optionally filtered by role"""
    query = select(User)
    
    if role:
        query = query.where(User.role == role)
    
    query = query.order_by(User.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific user by ID"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Update a user (admin only)"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if email is being changed and if it's already taken
    if user_data.email and user_data.email != user.email:
        email_check = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        if email_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Delete a user (admin only)"""
    # Prevent admin from deleting themselves
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await db.delete(user)
    await db.commit()


# Platform Statistics
@router.get("/stats")
async def get_platform_stats(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get platform-wide statistics"""
    # User counts by role
    total_users = await db.execute(select(func.count(User.id)))
    active_users = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    clients = await db.execute(
        select(func.count(User.id)).where(User.role == UserRole.CLIENT)
    )
    coaches = await db.execute(
        select(func.count(User.id)).where(User.role == UserRole.COACH)
    )
    admins = await db.execute(
        select(func.count(User.id)).where(User.role == UserRole.ADMIN)
    )
    
    # Activity statistics
    total_workouts = await db.execute(select(func.count(WorkoutLog.id)))
    total_diet_logs = await db.execute(select(func.count(DietLog.id)))
    
    # Last 30 days activity
    thirty_days_ago = date.today() - timedelta(days=30)
    recent_workouts = await db.execute(
        select(func.count(WorkoutLog.id))
        .where(WorkoutLog.workout_date >= thirty_days_ago)
    )
    recent_diet_logs = await db.execute(
        select(func.count(DietLog.id))
        .where(DietLog.meal_date >= thirty_days_ago)
    )
    
    # Plans statistics
    active_workout_plans = await db.execute(
        select(func.count(WorkoutPlan.id))
        .where(WorkoutPlan.status == "active")
    )
    active_diet_plans = await db.execute(
        select(func.count(DietPlan.id))
        .where(DietPlan.status == "active")
    )
    
    return {
        "users": {
            "total": total_users.scalar() or 0,
            "active": active_users.scalar() or 0,
            "clients": clients.scalar() or 0,
            "coaches": coaches.scalar() or 0,
            "admins": admins.scalar() or 0
        },
        "activity": {
            "total_workouts": total_workouts.scalar() or 0,
            "total_diet_logs": total_diet_logs.scalar() or 0
        },
        "last_30_days": {
            "workouts": recent_workouts.scalar() or 0,
            "diet_logs": recent_diet_logs.scalar() or 0
        },
        "plans": {
            "active_workout_plans": active_workout_plans.scalar() or 0,
            "active_diet_plans": active_diet_plans.scalar() or 0
        }
    }


# Usage Report
@router.get("/reports/usage")
async def generate_usage_report(
    days: int = 30,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Generate a usage report for the specified period"""
    start_date = date.today() - timedelta(days=days)
    
    # New users in period
    new_users = await db.execute(
        select(func.count(User.id))
        .where(User.created_at >= start_date)
    )
    
    # Activity in period
    workouts_in_period = await db.execute(
        select(func.count(WorkoutLog.id))
        .where(WorkoutLog.workout_date >= start_date)
    )
    
    diet_logs_in_period = await db.execute(
        select(func.count(DietLog.id))
        .where(DietLog.meal_date >= start_date)
    )
    
    # Plans created in period
    workout_plans_created = await db.execute(
        select(func.count(WorkoutPlan.id))
        .where(WorkoutPlan.created_at >= start_date)
    )
    
    diet_plans_created = await db.execute(
        select(func.count(DietPlan.id))
        .where(DietPlan.created_at >= start_date)
    )
    
    # Most active users
    most_active_workout = await db.execute(
        select(User.id, User.full_name, User.email, func.count(WorkoutLog.id).label('count'))
        .join(WorkoutLog, User.id == WorkoutLog.user_id)
        .where(WorkoutLog.workout_date >= start_date)
        .group_by(User.id, User.full_name, User.email)
        .order_by(func.count(WorkoutLog.id).desc())
        .limit(5)
    )
    
    top_users = [
        {
            "user_id": row[0],
            "full_name": row[1],
            "email": row[2],
            "workout_count": row[3]
        }
        for row in most_active_workout.all()
    ]
    
    return {
        "report_period_days": days,
        "start_date": start_date.isoformat(),
        "end_date": date.today().isoformat(),
        "new_users": new_users.scalar() or 0,
        "activity": {
            "workouts_logged": workouts_in_period.scalar() or 0,
            "diet_logs": diet_logs_in_period.scalar() or 0
        },
        "plans_created": {
            "workout_plans": workout_plans_created.scalar() or 0,
            "diet_plans": diet_plans_created.scalar() or 0
        },
        "top_users": top_users
    }
