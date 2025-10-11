"""
Database seed script for charts and dashboards with comprehensive historical data
"""

import asyncio
import random
from datetime import date, datetime, timezone, timedelta
from sqlalchemy import text

from app.db.base import AsyncSessionLocal
from app.models import User, UserRole, WorkoutLog, DietLog, MealType, WorkoutPlan, DietPlan, PlanStatus
from app.core.security import get_password_hash


# Sample data for variety
EXERCISES = [
    "Bench Press", "Squats", "Deadlifts", "Overhead Press", "Barbell Rows",
    "Pull-ups", "Dips", "Lunges", "Leg Press", "Bicep Curls",
    "Tricep Extensions", "Lateral Raises", "Romanian Deadlifts", "Front Squats",
    "Running", "Cycling", "Swimming", "Jump Rope"
]

BREAKFAST_FOODS = [
    ("Oatmeal with berries", 350, 12, 55, 8),
    ("Scrambled eggs with toast", 420, 24, 35, 18),
    ("Greek yogurt with granola", 380, 20, 45, 12),
    ("Protein pancakes", 450, 28, 52, 14),
    ("Avocado toast with eggs", 480, 22, 38, 26),
]

LUNCH_FOODS = [
    ("Chicken breast with rice and vegetables", 520, 45, 55, 10),
    ("Salmon with quinoa and broccoli", 580, 42, 48, 22),
    ("Turkey sandwich with salad", 460, 35, 48, 15),
    ("Beef stir-fry with brown rice", 550, 40, 52, 18),
    ("Tuna salad wrap", 420, 38, 42, 12),
]

DINNER_FOODS = [
    ("Grilled chicken with sweet potato", 540, 48, 50, 14),
    ("Lean beef with pasta", 620, 45, 58, 20),
    ("Fish tacos with beans", 510, 38, 54, 16),
    ("Shrimp stir-fry with vegetables", 450, 42, 45, 12),
    ("Turkey meatballs with zoodles", 480, 44, 38, 18),
]

SNACK_FOODS = [
    ("Protein shake", 280, 30, 25, 8),
    ("Apple with almond butter", 240, 8, 28, 14),
    ("Cottage cheese with berries", 220, 24, 20, 6),
    ("Trail mix", 310, 12, 32, 18),
    ("Rice cakes with peanut butter", 260, 10, 30, 12),
]


async def seed_charts_data():
    """Seed the database with comprehensive data for charts and dashboards"""
    
    async with AsyncSessionLocal() as session:
        print("Seeding database with comprehensive charts data...")
        
        # Create multiple users
        admin_user = User(
            email="admin2@vibe.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
            created_at=datetime.now(timezone.utc) - timedelta(days=180),
            updated_at=datetime.now(timezone.utc),
        )
        
        # Create 3 coaches with profile data
        coaches_data = [
            {
                "name": "Coach A",
                "strengths": "Strength Training, Powerlifting, Olympic Lifts",
                "specialties": "Powerlifting, Bodybuilding",
                "experience": "10 years of professional coaching experience",
                "certifications": "NASM-CPT, CSCS, USA Weightlifting Level 1",
            },
            {
                "name": "Coach B",
                "strengths": "Weight Loss, Cardio Training, HIIT",
                "specialties": "Weight Loss, Endurance Training",
                "experience": "8 years of personal training experience",
                "certifications": "ACE-CPT, Precision Nutrition Level 1",
            },
            {
                "name": "Coach C",
                "strengths": "Functional Training, CrossFit, Athletic Performance",
                "specialties": "CrossFit, Athletic Performance",
                "experience": "12 years of coaching athletes and fitness enthusiasts",
                "certifications": "CrossFit Level 2, FMS Level 1, USAW Sports Performance",
            }
        ]
        
        coaches = []
        for i, coach_data in enumerate(coaches_data, 1):
            coach = User(
                email=f"coach{i}@vibe.com",
                hashed_password=get_password_hash(f"coach{i}123"),
                full_name=coach_data["name"],
                role=UserRole.COACH,
                is_active=True,
                is_verified=True,
                strengths=coach_data["strengths"],
                specialties=coach_data["specialties"],
                experience=coach_data["experience"],
                certifications=coach_data["certifications"],
                available_slots=10,
                age=random.randint(28, 45),
                gender=random.choice(["Male", "Female"]),
                created_at=datetime.now(timezone.utc) - timedelta(days=150),
                updated_at=datetime.now(timezone.utc),
            )
            coaches.append(coach)
        
        # Create 10 clients with profile data
        client_goals = [
            "Build muscle mass and strength",
            "Lose weight and improve cardiovascular health",
            "Improve overall fitness and endurance",
            "Train for a marathon",
            "Gain muscle definition and reduce body fat",
            "Increase strength for powerlifting competition",
            "Improve flexibility and mobility",
            "Get back in shape after injury",
            "Prepare for athletic season",
            "Maintain fitness and healthy lifestyle"
        ]
        
        clients = []
        for i in range(1, 11):
            client = User(
                email=f"client{i}@vibe.com",
                hashed_password=get_password_hash(f"client{i}123"),
                full_name=f"Client {chr(64+i)}",
                role=UserRole.CLIENT,
                is_active=True,
                is_verified=True,
                age=random.randint(22, 55),
                gender=random.choice(["Male", "Female"]),
                height=round(random.uniform(160, 190), 1),
                weight=round(random.uniform(60, 100), 1),
                bicep_size=round(random.uniform(30, 45), 1),
                waist=round(random.uniform(70, 95), 1),
                target_goals=client_goals[i-1],
                gym_access=random.choice(["Home Gym", "Commercial Gym", "CrossFit Box", "No Gym"]),
                dietary_restrictions=random.choice([None, "Vegetarian", "Vegan", "Gluten-Free", "Lactose Intolerant"]),
                health_complications=random.choice([None, "High blood pressure", "Diabetes Type 2", "Asthma"]),
                injuries=random.choice([None, "Previous knee injury", "Lower back pain", "Shoulder impingement"]),
                created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(30, 120)),
                updated_at=datetime.now(timezone.utc),
            )
            clients.append(client)
        
        session.add_all([admin_user] + coaches + clients)
        await session.commit()
        
        print(f"Created 1 admin, {len(coaches)} coaches, and {len(clients)} clients")
        
        # Refresh to get IDs
        for client in clients:
            await session.refresh(client)
        for coach in coaches:
            await session.refresh(coach)
        
        # Generate historical workout logs for each client (last 90 days)
        workout_logs = []
        for client in clients:
            # Each client has different workout frequency (2-6 times per week)
            workouts_per_week = random.randint(2, 6)
            days_back = 90
            
            for day_offset in range(days_back):
                workout_date = date.today() - timedelta(days=day_offset)
                
                # Randomly skip days based on frequency
                if random.random() < (workouts_per_week / 7):
                    # Each workout day, log 2-5 exercises
                    num_exercises = random.randint(2, 5)
                    for _ in range(num_exercises):
                        exercise = random.choice(EXERCISES)
                        
                        # Progressive overload - weight increases slightly over time
                        weight_base = random.uniform(20, 100)
                        weight_progress = (days_back - day_offset) / days_back * 10
                        weight = round(weight_base + weight_progress, 1)
                        
                        workout_log = WorkoutLog(
                            user_id=client.id,
                            workout_date=workout_date,
                            exercise_name=exercise,
                            sets=random.randint(2, 5),
                            reps=random.randint(6, 15),
                            weight=weight,
                            duration_minutes=random.randint(15, 60),
                            notes="Feeling good!" if random.random() > 0.7 else None,
                            created_at=datetime.combine(workout_date, datetime.min.time()).replace(tzinfo=timezone.utc),
                            updated_at=datetime.combine(workout_date, datetime.min.time()).replace(tzinfo=timezone.utc),
                        )
                        workout_logs.append(workout_log)
        
        session.add_all(workout_logs)
        await session.commit()
        print(f"Created {len(workout_logs)} workout logs")
        
        # Generate historical diet logs for each client (last 90 days)
        diet_logs = []
        for client in clients:
            # Each client logs 1-4 meals per day
            meals_per_day = random.randint(1, 4)
            days_back = 90
            
            for day_offset in range(days_back):
                meal_date = date.today() - timedelta(days=day_offset)
                
                # Randomly skip days (70% compliance rate)
                if random.random() < 0.7:
                    # Log meals for the day
                    meal_types_to_log = random.sample(list(MealType), meals_per_day)
                    
                    for meal_type in meal_types_to_log:
                        if meal_type == MealType.BREAKFAST:
                            food_data = random.choice(BREAKFAST_FOODS)
                        elif meal_type == MealType.LUNCH:
                            food_data = random.choice(LUNCH_FOODS)
                        elif meal_type == MealType.DINNER:
                            food_data = random.choice(DINNER_FOODS)
                        else:
                            food_data = random.choice(SNACK_FOODS)
                        
                        food_name, calories, protein, carbs, fat = food_data
                        
                        diet_log = DietLog(
                            user_id=client.id,
                            meal_date=meal_date,
                            meal_type=meal_type,
                            food_name=food_name,
                            calories=float(calories),
                            protein_grams=float(protein),
                            carbs_grams=float(carbs),
                            fat_grams=float(fat),
                            notes="Delicious!" if random.random() > 0.8 else None,
                            created_at=datetime.combine(meal_date, datetime.min.time()).replace(tzinfo=timezone.utc),
                            updated_at=datetime.combine(meal_date, datetime.min.time()).replace(tzinfo=timezone.utc),
                        )
                        diet_logs.append(diet_log)
        
        session.add_all(diet_logs)
        await session.commit()
        print(f"Created {len(diet_logs)} diet logs")
        
        # Create workout plans for clients (assigned by coaches)
        workout_plans = []
        plan_names = [
            "Beginner Strength Program",
            "Advanced Hypertrophy",
            "Fat Loss Circuit",
            "Powerlifting Prep",
            "Athletic Performance",
            "Home Workout Plan",
            "Full Body Split"
        ]
        
        for i, client in enumerate(clients):
            # Each client has 1-3 plans (some active, some completed)
            num_plans = random.randint(1, 3)
            for plan_idx in range(num_plans):
                plan_start = date.today() - timedelta(days=random.randint(10, 80))
                plan_status = PlanStatus.ACTIVE if plan_idx == 0 else random.choice([PlanStatus.ACTIVE, PlanStatus.COMPLETED])
                
                workout_plan = WorkoutPlan(
                    user_id=client.id,
                    name=random.choice(plan_names),
                    description=f"Customized plan for {client.full_name}",
                    start_date=plan_start,
                    status=plan_status,
                    duration_weeks=random.choice([4, 8, 12, 16]),
                    workout_details={
                        "days_per_week": random.randint(3, 6),
                        "focus": random.choice(["Strength", "Hypertrophy", "Endurance", "Full Body"]),
                        "exercises": [
                            {"name": random.choice(EXERCISES), "sets": random.randint(3, 5), "reps": random.randint(6, 12)}
                            for _ in range(random.randint(4, 8))
                        ]
                    },
                    created_at=datetime.combine(plan_start, datetime.min.time()).replace(tzinfo=timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                workout_plans.append(workout_plan)
        
        session.add_all(workout_plans)
        await session.commit()
        print(f"Created {len(workout_plans)} workout plans")
        
        # Create diet plans for clients
        diet_plans = []
        diet_names = [
            "Muscle Building Diet",
            "Fat Loss Nutrition",
            "Maintenance Macros",
            "Performance Nutrition",
            "Flexible Dieting",
            "Clean Eating Plan"
        ]
        
        for i, client in enumerate(clients):
            # Each client has 1-2 diet plans
            num_plans = random.randint(1, 2)
            for plan_idx in range(num_plans):
                plan_start = date.today() - timedelta(days=random.randint(10, 80))
                plan_status = PlanStatus.ACTIVE if plan_idx == 0 else random.choice([PlanStatus.ACTIVE, PlanStatus.COMPLETED])
                
                diet_plan = DietPlan(
                    user_id=client.id,
                    name=random.choice(diet_names),
                    description=f"Nutrition plan tailored for {client.full_name}",
                    start_date=plan_start,
                    status=plan_status,
                    target_calories=float(random.randint(1800, 3000)),
                    target_protein_grams=float(random.randint(120, 200)),
                    target_carbs_grams=float(random.randint(200, 350)),
                    target_fat_grams=float(random.randint(50, 100)),
                    meal_plan_details={
                        "meals_per_day": random.randint(3, 6),
                        "meal_timing": ["7:00", "10:00", "13:00", "16:00", "19:00", "22:00"][:random.randint(3, 6)],
                    },
                    created_at=datetime.combine(plan_start, datetime.min.time()).replace(tzinfo=timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                diet_plans.append(diet_plan)
        
        session.add_all(diet_plans)
        await session.commit()
        print(f"Created {len(diet_plans)} diet plans")
        
        # Create some bookings
        from app.models.booking import Booking, BookingStatus
        bookings = []
        
        # Each coach has some bookings from different clients
        for coach_idx, coach in enumerate(coaches):
            # Random number of bookings per coach (3-5)
            num_bookings = random.randint(3, 5)
            # Select random clients for bookings
            booking_clients = random.sample(clients, num_bookings)
            
            for slot_num, client in enumerate(booking_clients, 1):
                # Create booking with different statuses
                booking_status = random.choice([
                    BookingStatus.CONFIRMED, 
                    BookingStatus.COMPLETED, 
                    BookingStatus.PENDING
                ])
                
                # Scheduled time can be past or future
                days_offset = random.randint(-30, 30)
                scheduled_time = datetime.now(timezone.utc) + timedelta(days=days_offset)
                
                booking = Booking(
                    coach_id=coach.id,
                    client_id=client.id,
                    slot_number=slot_num,
                    scheduled_at=scheduled_time,
                    status=booking_status,
                    notes=f"Training session {slot_num}" if random.random() > 0.5 else None,
                    created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 60)),
                    updated_at=datetime.now(timezone.utc),
                )
                bookings.append(booking)
        
        session.add_all(bookings)
        await session.commit()
        print(f"Created {len(bookings)} bookings")
        
        # Update available_slots for coaches based on confirmed bookings
        for coach in coaches:
            confirmed_bookings = len([b for b in bookings if b.coach_id == coach.id and b.status in [BookingStatus.CONFIRMED, BookingStatus.PENDING]])
            coach.available_slots = max(0, 10 - confirmed_bookings)
        
        await session.commit()
        print("Updated coach available slots")
        
        print("\n" + "="*60)
        print("Database seeded successfully with comprehensive data!")
        print("="*60)
        print("\nSample credentials:")
        print("  Admin: admin2@vibe.com / admin123")
        print("  Coaches: coach1@vibe.com / coach1123, coach2@vibe.com / coach2123, coach3@vibe.com / coach3123")
        print("  Clients: client1@vibe.com / client1123 through client10@vibe.com / client10123")
        print("\nData Summary:")
        print(f"  - {len(workout_logs)} workout logs across 10 clients over 90 days")
        print(f"  - {len(diet_logs)} diet logs with varied meal patterns")
        print(f"  - {len(workout_plans)} workout plans")
        print(f"  - {len(diet_plans)} diet plans")
        print(f"  - {len(bookings)} coach-client bookings")
        print("="*60)


if __name__ == "__main__":
    asyncio.run(seed_charts_data())
