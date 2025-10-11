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


# Chart Data Endpoints
@router.get("/charts/user-growth")
async def get_user_growth_chart(
    days: int = 90,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get user growth over time"""
    start_date = date.today() - timedelta(days=days)
    
    # Get user registrations grouped by date
    result = await db.execute(
        select(
            func.date(User.created_at).label('date'),
            func.count(User.id).label('count'),
            User.role
        )
        .where(User.created_at >= start_date)
        .group_by(func.date(User.created_at), User.role)
        .order_by(func.date(User.created_at))
    )
    
    data = result.all()
    
    # Organize by role
    growth_data = {}
    for row in data:
        date_str = row.date.isoformat() if hasattr(row.date, 'isoformat') else str(row.date)
        if date_str not in growth_data:
            growth_data[date_str] = {"clients": 0, "coaches": 0, "admins": 0}
        
        if row.role == "client":
            growth_data[date_str]["clients"] = row.count
        elif row.role == "coach":
            growth_data[date_str]["coaches"] = row.count
        elif row.role == "admin":
            growth_data[date_str]["admins"] = row.count
    
    return {
        "labels": list(growth_data.keys()),
        "clients": [growth_data[k]["clients"] for k in growth_data.keys()],
        "coaches": [growth_data[k]["coaches"] for k in growth_data.keys()],
        "admins": [growth_data[k]["admins"] for k in growth_data.keys()]
    }


@router.get("/charts/platform-usage")
async def get_platform_usage_chart(
    days: int = 30,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get platform usage statistics over time"""
    start_date = date.today() - timedelta(days=days)
    
    # Get daily workout logs
    workout_result = await db.execute(
        select(
            WorkoutLog.workout_date,
            func.count(WorkoutLog.id).label('count')
        )
        .where(WorkoutLog.workout_date >= start_date)
        .group_by(WorkoutLog.workout_date)
        .order_by(WorkoutLog.workout_date)
    )
    workout_data = workout_result.all()
    
    # Get daily diet logs
    diet_result = await db.execute(
        select(
            DietLog.meal_date,
            func.count(DietLog.id).label('count')
        )
        .where(DietLog.meal_date >= start_date)
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


@router.get("/charts/coach-performance")
async def get_coach_performance_chart(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get coach performance metrics"""
    
    # Get plans created by coach (would need coach_id in plans table, for now show all plans)
    workout_plans_result = await db.execute(
        select(func.count(WorkoutPlan.id))
    )
    diet_plans_result = await db.execute(
        select(func.count(DietPlan.id))
    )
    
    # Get client counts
    clients_result = await db.execute(
        select(func.count(User.id))
        .where(User.role == UserRole.CLIENT)
    )
    
    return {
        "total_workout_plans": workout_plans_result.scalar() or 0,
        "total_diet_plans": diet_plans_result.scalar() or 0,
        "total_clients": clients_result.scalar() or 0
    }


@router.get("/charts/system-health")
async def get_system_health_chart(
    days: int = 7,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get system health indicators"""
    start_date = date.today() - timedelta(days=days)
    
    # Get daily active users (users who logged workouts or diet)
    active_users_result = await db.execute(
        select(
            func.date(WorkoutLog.workout_date).label('date'),
            func.count(func.distinct(WorkoutLog.user_id)).label('count')
        )
        .where(WorkoutLog.workout_date >= start_date)
        .group_by(func.date(WorkoutLog.workout_date))
        .order_by(func.date(WorkoutLog.workout_date))
    )
    active_users_data = active_users_result.all()
    
    # Get total users
    total_users_result = await db.execute(
        select(func.count(User.id))
    )
    total_users = total_users_result.scalar() or 0
    
    # Calculate engagement rate
    return {
        "daily_active_users": {
            "labels": [row.date.isoformat() if hasattr(row.date, 'isoformat') else str(row.date) for row in active_users_data],
            "data": [row.count for row in active_users_data]
        },
        "total_users": total_users,
        "active_rate": (active_users_data[-1].count / total_users * 100) if active_users_data and total_users > 0 else 0
    }
