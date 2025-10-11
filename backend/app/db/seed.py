"""
Database seed script for initial data
"""

import asyncio
from datetime import date, datetime, timezone
from sqlalchemy import text

from app.db.base import AsyncSessionLocal
from app.models import User, UserRole, WorkoutLog, DietLog, MealType, WorkoutPlan, DietPlan, PlanStatus
from app.core.security import get_password_hash


async def seed_database():
    """Seed the database with initial data"""
    
    async with AsyncSessionLocal() as session:
        # Check if users already exist
        result = await session.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        
        if count > 0:
            print("Database already seeded. Skipping...")
            return
        
        print("Seeding database with initial data...")
        
        # Create sample users with hashed passwords
        admin_user = User(
            email="admin@vibe.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        
        coach_user = User(
            email="coach@vibe.com",
            hashed_password=get_password_hash("coach123"),
            full_name="John Coach",
            role=UserRole.COACH,
            is_active=True,
            is_verified=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        
        client_user = User(
            email="client@vibe.com",
            hashed_password=get_password_hash("client123"),
            full_name="Jane Client",
            role=UserRole.CLIENT,
            is_active=True,
            is_verified=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        
        session.add_all([admin_user, coach_user, client_user])
        await session.commit()
        
        print(f"Created users: {admin_user.email}, {coach_user.email}, {client_user.email}")
        
        # Refresh to get IDs
        await session.refresh(client_user)
        
        # Create sample workout log
        workout_log = WorkoutLog(
            user_id=client_user.id,
            workout_date=date.today(),
            exercise_name="Bench Press",
            sets=3,
            reps=10,
            weight=60.0,
            duration_minutes=30,
            notes="Felt good today!",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(workout_log)
        
        # Create sample diet log
        diet_log = DietLog(
            user_id=client_user.id,
            meal_date=date.today(),
            meal_type=MealType.BREAKFAST,
            food_name="Oatmeal with berries",
            calories=350.0,
            protein_grams=12.0,
            carbs_grams=55.0,
            fat_grams=8.0,
            notes="Healthy start to the day",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(diet_log)
        
        # Create sample workout plan
        workout_plan = WorkoutPlan(
            user_id=client_user.id,
            name="Beginner Strength Program",
            description="A 12-week program focused on building foundational strength",
            start_date=date.today(),
            status=PlanStatus.ACTIVE,
            duration_weeks=12,
            workout_details={
                "days_per_week": 3,
                "focus": "Full Body",
                "exercises": [
                    {"name": "Squats", "sets": 3, "reps": 10},
                    {"name": "Bench Press", "sets": 3, "reps": 10},
                    {"name": "Deadlifts", "sets": 3, "reps": 8},
                ]
            },
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(workout_plan)
        
        # Create sample diet plan
        diet_plan = DietPlan(
            user_id=client_user.id,
            name="Muscle Building Diet",
            description="High protein diet for muscle gain",
            start_date=date.today(),
            status=PlanStatus.ACTIVE,
            target_calories=2500.0,
            target_protein_grams=150.0,
            target_carbs_grams=300.0,
            target_fat_grams=70.0,
            meal_plan_details={
                "meals_per_day": 5,
                "meal_timing": ["7:00", "10:00", "13:00", "16:00", "19:00"],
            },
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(diet_plan)
        
        await session.commit()
        
        print("Database seeded successfully!")
        print("\nSample credentials:")
        print("  Admin: admin@vibe.com / admin123")
        print("  Coach: coach@vibe.com / coach123")
        print("  Client: client@vibe.com / client123")


if __name__ == "__main__":
    asyncio.run(seed_database())
