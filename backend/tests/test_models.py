"""
Tests for database models
"""

import pytest
from datetime import date, timedelta
from sqlalchemy import select

from app.models.user import User, UserRole
from app.models.workout_log import WorkoutLog
from app.models.diet_log import DietLog, MealType
from app.models.workout_plan import WorkoutPlan
from app.models.diet_plan import DietPlan


@pytest.mark.asyncio
async def test_user_model_creation(test_db):
    """Test creating a user model"""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        full_name="Test User",
        role=UserRole.CLIENT,
        is_active=True,
        is_verified=False
    )
    
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.role == UserRole.CLIENT
    assert user.is_active is True
    assert user.created_at is not None


@pytest.mark.asyncio
async def test_user_role_enum():
    """Test user role enum values"""
    assert UserRole.CLIENT.value == "client"
    assert UserRole.COACH.value == "coach"
    assert UserRole.ADMIN.value == "admin"


@pytest.mark.asyncio
async def test_workout_log_model(test_db):
    """Test creating a workout log"""
    user = User(
        email="workout@example.com",
        hashed_password="hashed",
        full_name="Workout User",
        role=UserRole.CLIENT,
        is_active=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    
    workout_log = WorkoutLog(
        user_id=user.id,
        workout_date=date.today(),
        exercise_name="Squats",
        sets=4,
        reps=8,
        weight=100.0,
        duration_minutes=30,
        notes="Felt strong today"
    )
    
    test_db.add(workout_log)
    await test_db.commit()
    await test_db.refresh(workout_log)
    
    assert workout_log.id is not None
    assert workout_log.user_id == user.id
    assert workout_log.exercise_name == "Squats"
    assert workout_log.sets == 4
    assert workout_log.weight == 100.0


@pytest.mark.asyncio
async def test_diet_log_model(test_db):
    """Test creating a diet log"""
    user = User(
        email="diet@example.com",
        hashed_password="hashed",
        full_name="Diet User",
        role=UserRole.CLIENT,
        is_active=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    
    diet_log = DietLog(
        user_id=user.id,
        meal_date=date.today(),
        meal_type=MealType.BREAKFAST,
        food_name="Oatmeal with fruits",
        calories=350.0,
        protein_grams=12.0,
        carbs_grams=55.0,
        fat_grams=8.0
    )
    
    test_db.add(diet_log)
    await test_db.commit()
    await test_db.refresh(diet_log)
    
    assert diet_log.id is not None
    assert diet_log.user_id == user.id
    assert diet_log.meal_type == MealType.BREAKFAST
    assert diet_log.calories == 350.0


@pytest.mark.asyncio
async def test_meal_type_enum():
    """Test meal type enum values"""
    assert MealType.BREAKFAST.value == "breakfast"
    assert MealType.LUNCH.value == "lunch"
    assert MealType.DINNER.value == "dinner"
    assert MealType.SNACK.value == "snack"


@pytest.mark.asyncio
async def test_workout_plan_model(test_db):
    """Test creating a workout plan"""
    # Create client
    client = User(
        email="client@example.com",
        hashed_password="hashed",
        full_name="Client User",
        role=UserRole.CLIENT,
        is_active=True
    )
    test_db.add(client)
    await test_db.commit()
    await test_db.refresh(client)
    
    workout_plan = WorkoutPlan(
        user_id=client.id,
        name="Strength Training",
        description="4-week strength program",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=28)
    )
    
    test_db.add(workout_plan)
    await test_db.commit()
    await test_db.refresh(workout_plan)
    
    assert workout_plan.id is not None
    assert workout_plan.user_id == client.id
    assert workout_plan.name == "Strength Training"


@pytest.mark.asyncio
async def test_diet_plan_model(test_db):
    """Test creating a diet plan"""
    # Create client
    client = User(
        email="client2@example.com",
        hashed_password="hashed",
        full_name="Client User",
        role=UserRole.CLIENT,
        is_active=True
    )
    test_db.add(client)
    await test_db.commit()
    await test_db.refresh(client)
    
    diet_plan = DietPlan(
        user_id=client.id,
        name="High Protein Diet",
        description="2000 cal/day high protein",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=28),
        target_calories=2000,
        target_protein_grams=150,
        target_carbs_grams=200,
        target_fat_grams=67
    )
    
    test_db.add(diet_plan)
    await test_db.commit()
    await test_db.refresh(diet_plan)
    
    assert diet_plan.id is not None
    assert diet_plan.user_id == client.id
    assert diet_plan.target_calories == 2000
    assert diet_plan.target_protein_grams == 150


@pytest.mark.asyncio
async def test_user_relationships(test_db):
    """Test user model relationships"""
    user = User(
        email="relationships@example.com",
        hashed_password="hashed",
        full_name="Relationship User",
        role=UserRole.CLIENT,
        is_active=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    
    # Add workout log
    workout_log = WorkoutLog(
        user_id=user.id,
        workout_date=date.today(),
        exercise_name="Push-ups",
        sets=3,
        reps=15
    )
    test_db.add(workout_log)
    
    # Add diet log
    diet_log = DietLog(
        user_id=user.id,
        meal_date=date.today(),
        meal_type=MealType.LUNCH,
        food_name="Chicken Salad",
        calories=450.0
    )
    test_db.add(diet_log)
    
    await test_db.commit()
    
    # Query back
    result = await test_db.execute(
        select(User).where(User.id == user.id)
    )
    queried_user = result.scalar_one()
    
    assert queried_user.id == user.id
    assert queried_user.email == "relationships@example.com"
