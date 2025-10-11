"""
Tests for dependency functions
"""

import pytest
from fastapi import HTTPException
from jose import jwt

from app.models.user import User, UserRole
from app.core.dependencies import get_current_user, get_current_active_user, require_coach, require_admin
from app.core.security import create_access_token
from app.core.config import settings


@pytest.fixture
async def active_client_user(test_db):
    """Create an active client user"""
    user = User(
        email="activeclient@example.com",
        hashed_password="hashed",
        full_name="Active Client",
        role=UserRole.CLIENT,
        is_active=True,
        is_verified=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def inactive_user(test_db):
    """Create an inactive user"""
    user = User(
        email="inactive@example.com",
        hashed_password="hashed",
        full_name="Inactive User",
        role=UserRole.CLIENT,
        is_active=False,
        is_verified=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def coach_user(test_db):
    """Create a coach user"""
    user = User(
        email="depcoach@example.com",
        hashed_password="hashed",
        full_name="Dep Coach",
        role=UserRole.COACH,
        is_active=True,
        is_verified=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def admin_user(test_db):
    """Create an admin user"""
    user = User(
        email="depadmin@example.com",
        hashed_password="hashed",
        full_name="Dep Admin",
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.mark.asyncio
async def test_get_current_user_valid_token(test_db, active_client_user):
    """Test getting current user with valid token"""
    token = create_access_token({
        "sub": active_client_user.email,
        "user_id": active_client_user.id
    })
    
    user = await get_current_user(token, test_db)
    
    assert user.id == active_client_user.id
    assert user.email == active_client_user.email


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(test_db):
    """Test getting current user with invalid token raises exception"""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user("invalid_token", test_db)
    
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_expired_token(test_db, active_client_user):
    """Test getting current user with token for non-existent user"""
    token = create_access_token({
        "sub": "nonexistent@example.com",
        "user_id": 99999
    })
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token, test_db)
    
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_active_user_active(test_db, active_client_user):
    """Test getting active user succeeds for active user"""
    token = create_access_token({
        "sub": active_client_user.email,
        "user_id": active_client_user.id
    })
    
    user = await get_current_user(token, test_db)
    active_user = await get_current_active_user(user)
    
    assert active_user.id == active_client_user.id
    assert active_user.is_active is True


@pytest.mark.asyncio
async def test_get_current_user_inactive(test_db, inactive_user):
    """Test getting current user fails for inactive user"""
    token = create_access_token({
        "sub": inactive_user.email,
        "user_id": inactive_user.id
    })
    
    # get_current_user already checks for inactive users
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token, test_db)
    
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_require_coach_with_coach(test_db, coach_user):
    """Test require_coach succeeds for coach user"""
    token = create_access_token({
        "sub": coach_user.email,
        "user_id": coach_user.id
    })
    
    user = await get_current_user(token, test_db)
    coach = await require_coach(user)
    
    assert coach.id == coach_user.id
    assert coach.role == UserRole.COACH


@pytest.mark.asyncio
async def test_require_coach_with_admin(test_db, admin_user):
    """Test require_coach succeeds for admin user"""
    token = create_access_token({
        "sub": admin_user.email,
        "user_id": admin_user.id
    })
    
    user = await get_current_user(token, test_db)
    admin = await require_coach(user)
    
    assert admin.id == admin_user.id
    assert admin.role == UserRole.ADMIN


@pytest.mark.asyncio
async def test_require_coach_with_client(test_db, active_client_user):
    """Test require_coach fails for client user"""
    token = create_access_token({
        "sub": active_client_user.email,
        "user_id": active_client_user.id
    })
    
    user = await get_current_user(token, test_db)
    
    with pytest.raises(HTTPException) as exc_info:
        await require_coach(user)
    
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_require_admin_with_admin(test_db, admin_user):
    """Test require_admin succeeds for admin user"""
    token = create_access_token({
        "sub": admin_user.email,
        "user_id": admin_user.id
    })
    
    user = await get_current_user(token, test_db)
    admin = await require_admin(user)
    
    assert admin.id == admin_user.id
    assert admin.role == UserRole.ADMIN


@pytest.mark.asyncio
async def test_require_admin_with_coach(test_db, coach_user):
    """Test require_admin fails for coach user"""
    token = create_access_token({
        "sub": coach_user.email,
        "user_id": coach_user.id
    })
    
    user = await get_current_user(token, test_db)
    
    with pytest.raises(HTTPException) as exc_info:
        await require_admin(user)
    
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_require_admin_with_client(test_db, active_client_user):
    """Test require_admin fails for client user"""
    token = create_access_token({
        "sub": active_client_user.email,
        "user_id": active_client_user.id
    })
    
    user = await get_current_user(token, test_db)
    
    with pytest.raises(HTTPException) as exc_info:
        await require_admin(user)
    
    assert exc_info.value.status_code == 403
