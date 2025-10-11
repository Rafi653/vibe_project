"""
Tests for client endpoints
"""

import pytest
from datetime import date, timedelta
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base, get_db
from app.models.user import User, UserRole
from app.models.workout_log import WorkoutLog
from app.models.diet_log import DietLog, MealType
from app.core.security import create_access_token

# Import all models to ensure they're registered with Base
from app.models import User, WorkoutLog, DietLog, WorkoutPlan, DietPlan

# Test database URL with StaticPool for proper in-memory SQLite sharing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine with StaticPool to share the same connection
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db():
    """Override database dependency for testing"""
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Create and drop database tables for each test"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_db():
    """Get a test database session"""
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
async def client_user(test_db: AsyncSession):
    """Create a test client user"""
    user = User(
        email="testclient@example.com",
        hashed_password="hashed_password",
        full_name="Test Client",
        role=UserRole.CLIENT,
        is_active=True,
        is_verified=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
def client_token(client_user):
    """Create an access token for the client user"""
    return create_access_token({"sub": client_user.email, "user_id": client_user.id})


@pytest.mark.asyncio
async def test_create_workout_log(client_token, test_db):
    """Test creating a workout log"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/client/workout-logs",
            headers={"Authorization": f"Bearer {client_token}"},
            json={
                "workout_date": date.today().isoformat(),
                "exercise_name": "Bench Press",
                "sets": 3,
                "reps": 10,
                "weight": 60.0,
                "duration_minutes": 30,
                "notes": "Felt good"
            }
        )
    
    assert response.status_code == 201
    data = response.json()
    assert data["exercise_name"] == "Bench Press"
    assert data["sets"] == 3


@pytest.mark.asyncio
async def test_get_workout_logs(client_user, client_token, test_db):
    """Test getting workout logs"""
    # Create a workout log
    log = WorkoutLog(
        user_id=client_user.id,
        workout_date=date.today(),
        exercise_name="Squats",
        sets=4,
        reps=8,
        weight=100.0
    )
    test_db.add(log)
    await test_db.commit()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/client/workout-logs",
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["exercise_name"] == "Squats"


@pytest.mark.asyncio
async def test_create_diet_log(client_token, test_db):
    """Test creating a diet log"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/client/diet-logs",
            headers={"Authorization": f"Bearer {client_token}"},
            json={
                "meal_date": date.today().isoformat(),
                "meal_type": "breakfast",
                "food_name": "Oatmeal",
                "calories": 350.0,
                "protein_grams": 12.0,
                "carbs_grams": 55.0,
                "fat_grams": 8.0
            }
        )
    
    assert response.status_code == 201
    data = response.json()
    assert data["food_name"] == "Oatmeal"
    assert data["meal_type"] == "breakfast"


@pytest.mark.asyncio
async def test_get_diet_logs(client_user, client_token, test_db):
    """Test getting diet logs"""
    # Create a diet log
    log = DietLog(
        user_id=client_user.id,
        meal_date=date.today(),
        meal_type=MealType.LUNCH,
        food_name="Chicken Salad",
        calories=450.0,
        protein_grams=35.0
    )
    test_db.add(log)
    await test_db.commit()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/client/diet-logs",
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["food_name"] == "Chicken Salad"


@pytest.mark.asyncio
async def test_get_progress(client_user, client_token, test_db):
    """Test getting progress metrics"""
    # Create some workout and diet logs
    workout_log = WorkoutLog(
        user_id=client_user.id,
        workout_date=date.today(),
        exercise_name="Running",
        duration_minutes=45
    )
    diet_log = DietLog(
        user_id=client_user.id,
        meal_date=date.today(),
        meal_type=MealType.DINNER,
        food_name="Grilled Fish",
        calories=400.0
    )
    test_db.add(workout_log)
    test_db.add(diet_log)
    await test_db.commit()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/client/progress",
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "last_30_days" in data
    assert data["last_30_days"]["workout_sessions"] >= 1
    assert data["last_30_days"]["diet_logs"] >= 1


@pytest.mark.asyncio
async def test_update_profile(client_token, test_db):
    """Test updating user profile"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put(
            "/api/v1/client/profile",
            headers={"Authorization": f"Bearer {client_token}"},
            json={"full_name": "Updated Name"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
