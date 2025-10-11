"""
Tests for authentication endpoints
"""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base, get_db
from app.models.user import User, UserRole
from app.core.security import get_password_hash

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
async def test_user(setup_database):
    """Create a test user in the database"""
    async with TestSessionLocal() as session:
        user = User(
            email="test@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User",
            role=UserRole.CLIENT,
            is_active=True,
            is_verified=False
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest.mark.asyncio
async def test_signup_success():
    """Test successful user signup"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "password123",
                "full_name": "New User",
                "role": "client"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["full_name"] == "New User"
        assert data["user"]["role"] == "client"
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_signup_duplicate_email(test_user):
    """Test signup with duplicate email fails"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "test@example.com",
                "password": "password123",
                "full_name": "Another User",
                "role": "client"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_signup_with_coach_role():
    """Test signup with coach role"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "coach@example.com",
                "password": "password123",
                "full_name": "Coach User",
                "role": "coach"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["user"]["role"] == "coach"


@pytest.mark.asyncio
async def test_login_success(test_user):
    """Test successful login"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert data["user"]["email"] == "test@example.com"
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(test_user):
    """Test login with wrong password fails"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user():
    """Test login with non-existent user fails"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_current_user(test_user):
    """Test getting current user info with valid token"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # First login to get token
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        token = login_response.json()["access_token"]
        
        # Get current user
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"


@pytest.mark.asyncio
async def test_get_current_user_no_token():
    """Test getting current user without token fails"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/auth/me")
        
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    """Test getting current user with invalid token fails"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(test_user):
    """Test logout endpoint"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # First login to get token
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        token = login_response.json()["access_token"]
        
        # Logout
        response = await client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
