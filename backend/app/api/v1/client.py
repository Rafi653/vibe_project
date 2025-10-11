"""
Client endpoints - for client users to manage their fitness data
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract
from datetime import date, datetime, timedelta
from typing import List, Optional

from app.db.base import get_db
from app.core.dependencies import require_client
from app.models.user import User
from app.models.workout_log import WorkoutLog
from app.models.diet_log import DietLog
from app.models.workout_plan import WorkoutPlan
from app.models.diet_plan import DietPlan
from app.schemas.workout_log import WorkoutLogCreate, WorkoutLogUpdate, WorkoutLogResponse
from app.schemas.diet_log import DietLogCreate, DietLogUpdate, DietLogResponse
from app.schemas.workout_plan import WorkoutPlanResponse
from app.schemas.diet_plan import DietPlanResponse
from app.schemas.user import UserProfileUpdate
from app.schemas.auth import UserResponse

router = APIRouter()


# Workout Log Endpoints
@router.post("/workout-logs", response_model=WorkoutLogResponse, status_code=status.HTTP_201_CREATED)
async def create_workout_log(
    log_data: WorkoutLogCreate,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Create a new workout log entry"""
    workout_log = WorkoutLog(
        user_id=current_user.id,
        **log_data.model_dump()
    )
    db.add(workout_log)
    await db.commit()
    await db.refresh(workout_log)
    return workout_log


@router.get("/workout-logs", response_model=List[WorkoutLogResponse])
async def get_workout_logs(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get all workout logs for the current user, optionally filtered by date range"""
    query = select(WorkoutLog).where(WorkoutLog.user_id == current_user.id)
    
    if start_date:
        query = query.where(WorkoutLog.workout_date >= start_date)
    if end_date:
        query = query.where(WorkoutLog.workout_date <= end_date)
    
    query = query.order_by(WorkoutLog.workout_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/workout-logs/{log_id}", response_model=WorkoutLogResponse)
async def get_workout_log(
    log_id: int,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific workout log by ID"""
    result = await db.execute(
        select(WorkoutLog).where(
            and_(WorkoutLog.id == log_id, WorkoutLog.user_id == current_user.id)
        )
    )
    workout_log = result.scalar_one_or_none()
    
    if not workout_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout log not found"
        )
    
    return workout_log


@router.put("/workout-logs/{log_id}", response_model=WorkoutLogResponse)
async def update_workout_log(
    log_id: int,
    log_data: WorkoutLogUpdate,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Update a workout log"""
    result = await db.execute(
        select(WorkoutLog).where(
            and_(WorkoutLog.id == log_id, WorkoutLog.user_id == current_user.id)
        )
    )
    workout_log = result.scalar_one_or_none()
    
    if not workout_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout log not found"
        )
    
    update_data = log_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workout_log, field, value)
    
    await db.commit()
    await db.refresh(workout_log)
    return workout_log


@router.delete("/workout-logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout_log(
    log_id: int,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Delete a workout log"""
    result = await db.execute(
        select(WorkoutLog).where(
            and_(WorkoutLog.id == log_id, WorkoutLog.user_id == current_user.id)
        )
    )
    workout_log = result.scalar_one_or_none()
    
    if not workout_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout log not found"
        )
    
    await db.delete(workout_log)
    await db.commit()


# Diet Log Endpoints
@router.post("/diet-logs", response_model=DietLogResponse, status_code=status.HTTP_201_CREATED)
async def create_diet_log(
    log_data: DietLogCreate,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Create a new diet log entry"""
    diet_log = DietLog(
        user_id=current_user.id,
        **log_data.model_dump()
    )
    db.add(diet_log)
    await db.commit()
    await db.refresh(diet_log)
    return diet_log


@router.get("/diet-logs", response_model=List[DietLogResponse])
async def get_diet_logs(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get all diet logs for the current user, optionally filtered by date range"""
    query = select(DietLog).where(DietLog.user_id == current_user.id)
    
    if start_date:
        query = query.where(DietLog.meal_date >= start_date)
    if end_date:
        query = query.where(DietLog.meal_date <= end_date)
    
    query = query.order_by(DietLog.meal_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/diet-logs/{log_id}", response_model=DietLogResponse)
async def get_diet_log(
    log_id: int,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific diet log by ID"""
    result = await db.execute(
        select(DietLog).where(
            and_(DietLog.id == log_id, DietLog.user_id == current_user.id)
        )
    )
    diet_log = result.scalar_one_or_none()
    
    if not diet_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet log not found"
        )
    
    return diet_log


@router.put("/diet-logs/{log_id}", response_model=DietLogResponse)
async def update_diet_log(
    log_id: int,
    log_data: DietLogUpdate,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Update a diet log"""
    result = await db.execute(
        select(DietLog).where(
            and_(DietLog.id == log_id, DietLog.user_id == current_user.id)
        )
    )
    diet_log = result.scalar_one_or_none()
    
    if not diet_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet log not found"
        )
    
    update_data = log_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(diet_log, field, value)
    
    await db.commit()
    await db.refresh(diet_log)
    return diet_log


@router.delete("/diet-logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diet_log(
    log_id: int,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Delete a diet log"""
    result = await db.execute(
        select(DietLog).where(
            and_(DietLog.id == log_id, DietLog.user_id == current_user.id)
        )
    )
    diet_log = result.scalar_one_or_none()
    
    if not diet_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet log not found"
        )
    
    await db.delete(diet_log)
    await db.commit()


# Workout Plans
@router.get("/workout-plans", response_model=List[WorkoutPlanResponse])
async def get_workout_plans(
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get all workout plans for the current user"""
    result = await db.execute(
        select(WorkoutPlan)
        .where(WorkoutPlan.user_id == current_user.id)
        .order_by(WorkoutPlan.start_date.desc())
    )
    return result.scalars().all()


@router.get("/workout-plans/{plan_id}", response_model=WorkoutPlanResponse)
async def get_workout_plan(
    plan_id: int,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific workout plan by ID"""
    result = await db.execute(
        select(WorkoutPlan).where(
            and_(WorkoutPlan.id == plan_id, WorkoutPlan.user_id == current_user.id)
        )
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found"
        )
    
    return plan


# Diet Plans
@router.get("/diet-plans", response_model=List[DietPlanResponse])
async def get_diet_plans(
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get all diet plans for the current user"""
    result = await db.execute(
        select(DietPlan)
        .where(DietPlan.user_id == current_user.id)
        .order_by(DietPlan.start_date.desc())
    )
    return result.scalars().all()


@router.get("/diet-plans/{plan_id}", response_model=DietPlanResponse)
async def get_diet_plan(
    plan_id: int,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific diet plan by ID"""
    result = await db.execute(
        select(DietPlan).where(
            and_(DietPlan.id == plan_id, DietPlan.user_id == current_user.id)
        )
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diet plan not found"
        )
    
    return plan


# Progress tracking
@router.get("/progress")
async def get_progress(
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get user's progress metrics"""
    # Get workout statistics for the last 30 days
    thirty_days_ago = date.today() - timedelta(days=30)
    
    workout_result = await db.execute(
        select(func.count(WorkoutLog.id))
        .where(
            and_(
                WorkoutLog.user_id == current_user.id,
                WorkoutLog.workout_date >= thirty_days_ago
            )
        )
    )
    workout_count = workout_result.scalar() or 0
    
    # Get diet log statistics
    diet_result = await db.execute(
        select(func.count(DietLog.id))
        .where(
            and_(
                DietLog.user_id == current_user.id,
                DietLog.meal_date >= thirty_days_ago
            )
        )
    )
    diet_log_count = diet_result.scalar() or 0
    
    # Get active plans count
    active_workout_plans = await db.execute(
        select(func.count(WorkoutPlan.id))
        .where(
            and_(
                WorkoutPlan.user_id == current_user.id,
                WorkoutPlan.status == "active"
            )
        )
    )
    active_workout_plan_count = active_workout_plans.scalar() or 0
    
    active_diet_plans = await db.execute(
        select(func.count(DietPlan.id))
        .where(
            and_(
                DietPlan.user_id == current_user.id,
                DietPlan.status == "active"
            )
        )
    )
    active_diet_plan_count = active_diet_plans.scalar() or 0
    
    return {
        "last_30_days": {
            "workout_sessions": workout_count,
            "diet_logs": diet_log_count
        },
        "active_plans": {
            "workout_plans": active_workout_plan_count,
            "diet_plans": active_diet_plan_count
        }
    }


@router.get("/charts/workout-frequency")
async def get_workout_frequency_chart(
    days: int = 30,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get workout frequency data for charts (workouts per day over time)"""
    start_date = date.today() - timedelta(days=days)
    
    # Get workout counts grouped by date
    result = await db.execute(
        select(
            WorkoutLog.workout_date,
            func.count(WorkoutLog.id).label('count')
        )
        .where(
            and_(
                WorkoutLog.user_id == current_user.id,
                WorkoutLog.workout_date >= start_date
            )
        )
        .group_by(WorkoutLog.workout_date)
        .order_by(WorkoutLog.workout_date)
    )
    
    data = result.all()
    return {
        "labels": [row.workout_date.isoformat() for row in data],
        "data": [row.count for row in data]
    }


@router.get("/charts/diet-adherence")
async def get_diet_adherence_chart(
    days: int = 30,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get diet adherence data for charts (calories and macros over time)"""
    start_date = date.today() - timedelta(days=days)
    
    # Get daily nutrition totals
    result = await db.execute(
        select(
            DietLog.meal_date,
            func.sum(DietLog.calories).label('total_calories'),
            func.sum(DietLog.protein_grams).label('total_protein'),
            func.sum(DietLog.carbs_grams).label('total_carbs'),
            func.sum(DietLog.fat_grams).label('total_fat')
        )
        .where(
            and_(
                DietLog.user_id == current_user.id,
                DietLog.meal_date >= start_date
            )
        )
        .group_by(DietLog.meal_date)
        .order_by(DietLog.meal_date)
    )
    
    data = result.all()
    
    # Get target from active diet plan
    target_result = await db.execute(
        select(DietPlan)
        .where(
            and_(
                DietPlan.user_id == current_user.id,
                DietPlan.status == "active"
            )
        )
        .order_by(DietPlan.start_date.desc())
        .limit(1)
    )
    active_plan = target_result.scalar_one_or_none()
    
    return {
        "labels": [row.meal_date.isoformat() for row in data],
        "calories": [float(row.total_calories or 0) for row in data],
        "protein": [float(row.total_protein or 0) for row in data],
        "carbs": [float(row.total_carbs or 0) for row in data],
        "fat": [float(row.total_fat or 0) for row in data],
        "targets": {
            "calories": float(active_plan.target_calories) if active_plan else None,
            "protein": float(active_plan.target_protein_grams) if active_plan else None,
            "carbs": float(active_plan.target_carbs_grams) if active_plan else None,
            "fat": float(active_plan.target_fat_grams) if active_plan else None
        }
    }


@router.get("/charts/workout-volume")
async def get_workout_volume_chart(
    days: int = 90,
    exercise: Optional[str] = None,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Get workout volume trends (weight progression over time)"""
    start_date = date.today() - timedelta(days=days)
    
    # Base query
    query = select(
        WorkoutLog.workout_date,
        WorkoutLog.exercise_name,
        func.avg(WorkoutLog.weight).label('avg_weight'),
        func.max(WorkoutLog.weight).label('max_weight')
    ).where(
        and_(
            WorkoutLog.user_id == current_user.id,
            WorkoutLog.workout_date >= start_date,
            WorkoutLog.weight.isnot(None)
        )
    )
    
    # Filter by exercise if specified
    if exercise:
        query = query.where(WorkoutLog.exercise_name == exercise)
    
    query = query.group_by(WorkoutLog.workout_date, WorkoutLog.exercise_name).order_by(WorkoutLog.workout_date)
    
    result = await db.execute(query)
    data = result.all()
    
    # Get unique exercises
    exercises_result = await db.execute(
        select(WorkoutLog.exercise_name)
        .where(
            and_(
                WorkoutLog.user_id == current_user.id,
                WorkoutLog.workout_date >= start_date,
                WorkoutLog.weight.isnot(None)
            )
        )
        .distinct()
    )
    exercises = [row[0] for row in exercises_result.all()]
    
    # Group data by exercise
    exercise_data = {}
    for row in data:
        if row.exercise_name not in exercise_data:
            exercise_data[row.exercise_name] = {"dates": [], "avg_weights": [], "max_weights": []}
        exercise_data[row.exercise_name]["dates"].append(row.workout_date.isoformat())
        exercise_data[row.exercise_name]["avg_weights"].append(float(row.avg_weight or 0))
        exercise_data[row.exercise_name]["max_weights"].append(float(row.max_weight or 0))
    
    return {
        "exercises": exercises,
        "data": exercise_data
    }


# Profile management
@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(require_client),
    db: AsyncSession = Depends(get_db)
):
    """Update user's own profile"""
    update_data = profile_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    return UserResponse.model_validate(current_user)
