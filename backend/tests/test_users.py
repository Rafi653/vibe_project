"""
Tests for user endpoints
"""

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.user import User, UserRole
from app.core.security import create_access_token


@pytest.fixture
async def test_user(test_db):
    """Create a test user"""
    user = User(
        email="user@example.com",
        hashed_password="hashed_password",
        full_name="Test User",
        role=UserRole.CLIENT,
        is_active=True,
        is_verified=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def admin_user(test_db):
    """Create a test admin user"""
    user = User(
        email="adminuser@example.com",
        hashed_password="hashed_password",
        full_name="Admin User",
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
def user_token(test_user):
    """Create an access token for the test user"""
    return create_access_token({"sub": test_user.email, "user_id": test_user.id})


@pytest.fixture
def admin_token(admin_user):
    """Create an access token for the admin user"""
    return create_access_token({"sub": admin_user.email, "user_id": admin_user.id})


@pytest.mark.asyncio
async def test_get_my_profile(user_token, test_user):
    """Test getting current user's profile"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["full_name"] == "Test User"


@pytest.mark.asyncio
async def test_get_my_profile_unauthorized():
    """Test getting profile without authentication"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/users/me")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_user_stats_client(user_token, test_user):
    """Test getting user statistics as a client"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/users/stats",
            headers={"Authorization": f"Bearer {user_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == test_user.id
    assert data["role"] == "client"
    assert "workout_count" in data
    assert "diet_logs" in data


@pytest.mark.asyncio
async def test_get_user_stats_admin(admin_token, admin_user):
    """Test getting user statistics as an admin"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/users/stats",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == admin_user.id
    assert data["role"] == "admin"
    assert "total_users" in data
    assert "active_coaches" in data
    assert "active_clients" in data


@pytest.mark.asyncio
async def test_list_all_users_as_admin(admin_token, test_user):
    """Test listing all users as admin"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/users/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_list_all_users_as_non_admin(user_token):
    """Test that non-admins cannot list all users"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/users/admin/users",
            headers={"Authorization": f"Bearer {user_token}"}
        )
    
    assert response.status_code == 403
