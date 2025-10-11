"""
Tests for service layer functions
"""

import pytest
from fastapi import HTTPException

from app.models.user import User, UserRole
from app.services.auth_service import AuthService
from app.schemas.auth import UserSignup, UserLogin
from app.core.security import verify_password


@pytest.mark.asyncio
async def test_signup_user_success(test_db):
    """Test successful user signup"""
    signup_data = UserSignup(
        email="newuser@example.com",
        password="password123",
        full_name="New User",
        role=UserRole.CLIENT
    )
    
    result = await AuthService.signup_user(test_db, signup_data)
    
    assert result.user.email == "newuser@example.com"
    assert result.user.full_name == "New User"
    assert result.user.role == "client"
    assert result.access_token is not None


@pytest.mark.asyncio
async def test_signup_user_duplicate_email(test_db):
    """Test creating a user with duplicate email fails"""
    signup_data1 = UserSignup(
        email="duplicate@example.com",
        password="password123",
        full_name="First User",
        role=UserRole.CLIENT
    )
    
    # Create first user
    await AuthService.signup_user(test_db, signup_data1)
    
    signup_data2 = UserSignup(
        email="duplicate@example.com",
        password="password456",
        full_name="Second User",
        role=UserRole.CLIENT
    )
    
    # Try to create second user with same email
    with pytest.raises(HTTPException) as exc_info:
        await AuthService.signup_user(test_db, signup_data2)
    
    assert exc_info.value.status_code == 400
    assert "already registered" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
async def test_login_user_success(test_db):
    """Test successful user login"""
    # Create a user
    signup_data = UserSignup(
        email="logintest@example.com",
        password="password123",
        full_name="Login Test User",
        role=UserRole.CLIENT
    )
    await AuthService.signup_user(test_db, signup_data)
    
    # Login the user
    login_data = UserLogin(
        email="logintest@example.com",
        password="password123"
    )
    result = await AuthService.login_user(test_db, login_data)
    
    assert result.user.email == "logintest@example.com"
    assert result.access_token is not None


@pytest.mark.asyncio
async def test_login_user_wrong_password(test_db):
    """Test login with wrong password"""
    # Create a user
    signup_data = UserSignup(
        email="wrongpass@example.com",
        password="password123",
        full_name="Wrong Pass User",
        role=UserRole.CLIENT
    )
    await AuthService.signup_user(test_db, signup_data)
    
    # Try to login with wrong password
    login_data = UserLogin(
        email="wrongpass@example.com",
        password="wrongpassword"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await AuthService.login_user(test_db, login_data)
    
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_login_user_nonexistent(test_db):
    """Test login with non-existent user"""
    login_data = UserLogin(
        email="nonexistent@example.com",
        password="password123"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await AuthService.login_user(test_db, login_data)
    
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_user_by_email(test_db):
    """Test getting a user by email"""
    # Create a user
    signup_data = UserSignup(
        email="getbyemail@example.com",
        password="password123",
        full_name="Get By Email User",
        role=UserRole.CLIENT
    )
    result = await AuthService.signup_user(test_db, signup_data)
    
    # Get the user by email
    fetched_user = await AuthService.get_user_by_email(test_db, "getbyemail@example.com")
    
    assert fetched_user is not None
    assert fetched_user.email == "getbyemail@example.com"
    assert fetched_user.id == result.user.id


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(test_db):
    """Test getting a non-existent user by email"""
    # Try to get non-existent user
    user = await AuthService.get_user_by_email(test_db, "notfound@example.com")
    
    assert user is None


@pytest.mark.asyncio
async def test_signup_user_different_roles(test_db):
    """Test creating users with different roles"""
    # Create client
    client_data = UserSignup(
        email="client@example.com",
        password="password123",
        full_name="Client User",
        role=UserRole.CLIENT
    )
    client = await AuthService.signup_user(test_db, client_data)
    assert client.user.role == "client"
    
    # Create coach
    coach_data = UserSignup(
        email="coach@example.com",
        password="password123",
        full_name="Coach User",
        role=UserRole.COACH
    )
    coach = await AuthService.signup_user(test_db, coach_data)
    assert coach.user.role == "coach"
    
    # Create admin
    admin_data = UserSignup(
        email="admin@example.com",
        password="password123",
        full_name="Admin User",
        role=UserRole.ADMIN
    )
    admin = await AuthService.signup_user(test_db, admin_data)
    assert admin.user.role == "admin"
