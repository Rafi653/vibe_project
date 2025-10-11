"""
Tests for feedback endpoints
"""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select

from app.main import app
from app.models.user import User, UserRole
from app.models.feedback import Feedback, FeedbackStatus
from app.core.security import create_access_token


@pytest.fixture
async def client_user(test_db):
    """Create a test client user"""
    user = User(
        email="client@example.com",
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
async def admin_user(test_db):
    """Create a test admin user"""
    user = User(
        email="admin@example.com",
        hashed_password="hashed_password",
        full_name="Test Admin",
        role=UserRole.ADMIN,
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


@pytest.fixture
def admin_token(admin_user):
    """Create an access token for the admin user"""
    return create_access_token({"sub": admin_user.email, "user_id": admin_user.id})


@pytest.mark.asyncio
async def test_submit_feedback_authenticated(client_token, test_db):
    """Test submitting feedback as authenticated user"""
    feedback_data = {
        "message": "This is a test feedback",
        "is_anonymous": False,
        "page_url": "http://example.com/test"
    }
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/feedback/",
            json=feedback_data,
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == feedback_data["message"]
    assert data["status"] == "open"
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_submit_feedback_anonymous(test_db):
    """Test submitting feedback anonymously (no auth)"""
    feedback_data = {
        "message": "Anonymous feedback",
        "name": "John Doe",
        "email": "john@example.com",
        "is_anonymous": False,
        "page_url": "http://example.com/test"
    }
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/feedback/",
            json=feedback_data
        )
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == feedback_data["message"]
    assert data["name"] == feedback_data["name"]
    assert data["email"] == feedback_data["email"]
    assert data["status"] == "open"


@pytest.mark.asyncio
async def test_get_all_feedback_admin_only(admin_token, test_db):
    """Test that only admins can retrieve all feedback"""
    # Create some feedback first
    feedback = Feedback(
        message="Test feedback",
        is_anonymous=False,
        status=FeedbackStatus.OPEN
    )
    test_db.add(feedback)
    await test_db.commit()
    
    # Admin can access
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/feedback/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_all_feedback_non_admin_forbidden(client_token):
    """Test that non-admins cannot retrieve all feedback"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/feedback/",
            headers={"Authorization": f"Bearer {client_token}"}
        )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_feedback_status(admin_token, test_db):
    """Test updating feedback status"""
    # Create feedback
    feedback = Feedback(
        message="Test feedback for status update",
        is_anonymous=False,
        status=FeedbackStatus.OPEN
    )
    test_db.add(feedback)
    await test_db.commit()
    await test_db.refresh(feedback)
    
    # Update status
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put(
            f"/api/v1/feedback/{feedback.id}",
            json={"status": "actively_looking"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "actively_looking"
    
    # Verify in database
    result = await test_db.execute(
        select(Feedback).where(Feedback.id == feedback.id)
    )
    updated_feedback = result.scalar_one()
    assert updated_feedback.status == FeedbackStatus.ACTIVELY_LOOKING


@pytest.mark.asyncio
async def test_update_feedback_status_non_admin_forbidden(client_token, test_db):
    """Test that non-admins cannot update feedback status"""
    # Create feedback
    feedback = Feedback(
        message="Test feedback",
        is_anonymous=False,
        status=FeedbackStatus.OPEN
    )
    test_db.add(feedback)
    await test_db.commit()
    await test_db.refresh(feedback)
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put(
            f"/api/v1/feedback/{feedback.id}",
            json={"status": "resolved"},
            headers={"Authorization": f"Bearer {client_token}"}
        )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_nonexistent_feedback(admin_token):
    """Test updating a feedback that doesn't exist"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put(
            "/api/v1/feedback/99999",
            json={"status": "resolved"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_feedback_status_enum_values(admin_token, test_db):
    """Test all valid feedback status enum values"""
    # Create feedback
    feedback = Feedback(
        message="Test all statuses",
        is_anonymous=False,
        status=FeedbackStatus.OPEN
    )
    test_db.add(feedback)
    await test_db.commit()
    await test_db.refresh(feedback)
    
    valid_statuses = ["open", "actively_looking", "resolved", "cannot_work_on"]
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for status in valid_statuses:
            response = await ac.put(
                f"/api/v1/feedback/{feedback.id}",
                json={"status": status},
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == status
