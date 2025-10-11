"""
Tests for booking endpoints
"""

import pytest
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.user import User, UserRole
from app.models.booking import Booking, BookingStatus
from app.core.security import create_access_token


@pytest.fixture
async def coach_user(test_db):
    """Create a test coach user with profile"""
    user = User(
        email="testcoach@example.com",
        hashed_password="hashed_password",
        full_name="Test Coach",
        role=UserRole.COACH,
        is_active=True,
        is_verified=True,
        strengths="Strength Training, Weight Loss",
        specialties="Powerlifting, CrossFit",
        experience="10 years",
        available_slots=10
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def client_user(test_db):
    """Create a test client user"""
    user = User(
        email="client1@example.com",
        hashed_password="hashed_password",
        full_name="Test Client",
        role=UserRole.CLIENT,
        is_active=True,
        is_verified=True,
        age=30,
        height=175.0,
        weight=80.0,
        target_goals="Build muscle"
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
async def booking(test_db, coach_user, client_user):
    """Create a test booking"""
    booking = Booking(
        coach_id=coach_user.id,
        client_id=client_user.id,
        slot_number=1,
        scheduled_at=datetime.now(timezone.utc) + timedelta(days=7),
        status=BookingStatus.PENDING,
        notes="Test session"
    )
    test_db.add(booking)
    await test_db.commit()
    await test_db.refresh(booking)
    return booking


class TestGetAvailableCoaches:
    """Tests for getting available coaches"""
    
    async def test_get_coaches_success(self, test_db, coach_user, client_user):
        """Test getting list of available coaches"""
        token = create_access_token({"sub": client_user.email, "user_id": client_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/v1/bookings/coaches",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        assert response.status_code == 200
        coaches = response.json()
        assert len(coaches) >= 1
        coach_data = next((c for c in coaches if c["coach_id"] == coach_user.id), None)
        assert coach_data is not None
        assert coach_data["coach_name"] == "Test Coach"
        assert coach_data["strengths"] == "Strength Training, Weight Loss"
        assert coach_data["available_slots"] == 10
    
    async def test_get_coaches_unauthorized(self, test_db):
        """Test getting coaches without authentication"""
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/bookings/coaches")
        
        assert response.status_code == 401


class TestGetCoachAvailability:
    """Tests for getting specific coach availability"""
    
    async def test_get_coach_availability_success(self, test_db, coach_user, client_user):
        """Test getting specific coach's availability"""
        token = create_access_token({"sub": client_user.email, "user_id": client_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.get(
                f"/api/v1/bookings/coaches/{coach_user.id}",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        assert response.status_code == 200
        coach_data = response.json()
        assert coach_data["coach_id"] == coach_user.id
        assert coach_data["coach_name"] == "Test Coach"
        assert coach_data["strengths"] == "Strength Training, Weight Loss"
        assert coach_data["available_slots"] == 10
    
    async def test_get_coach_availability_not_found(self, test_db, client_user):
        """Test getting non-existent coach"""
        token = create_access_token({"sub": client_user.email, "user_id": client_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/v1/bookings/coaches/9999",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        assert response.status_code == 404


class TestBookTrainingSlot:
    """Tests for booking training slots"""
    
    async def test_book_slot_success(self, test_db, coach_user, client_user):
        """Test successful slot booking"""
        token = create_access_token({"sub": client_user.email, "user_id": client_user.id})
        
        scheduled_time = datetime.now(timezone.utc) + timedelta(days=7)
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/bookings/book",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "coach_id": coach_user.id,
                    "slot_number": 1,
                    "scheduled_at": scheduled_time.isoformat(),
                    "notes": "First training session"
                }
            )
        
        assert response.status_code == 201
        booking_data = response.json()
        assert booking_data["coach_id"] == coach_user.id
        assert booking_data["client_id"] == client_user.id
        assert booking_data["slot_number"] == 1
        assert booking_data["status"] == "pending"
        
        # Verify coach's available slots decreased
        await test_db.refresh(coach_user)
        assert coach_user.available_slots == 9
    
    async def test_book_slot_duplicate(self, test_db, coach_user, client_user, booking):
        """Test booking same slot twice"""
        token = create_access_token({"sub": client_user.email, "user_id": client_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/bookings/book",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "coach_id": coach_user.id,
                    "slot_number": 1,
                    "notes": "Duplicate booking"
                }
            )
        
        assert response.status_code == 400
        assert "already booked" in response.json()["detail"]
    
    async def test_book_slot_coach_not_found(self, test_db, client_user):
        """Test booking with non-existent coach"""
        token = create_access_token({"sub": client_user.email, "user_id": client_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/bookings/book",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "coach_id": 9999,
                    "slot_number": 1
                }
            )
        
        assert response.status_code == 404
    
    async def test_book_slot_coach_cannot_book(self, test_db, coach_user):
        """Test that coaches cannot book slots"""
        token = create_access_token({"sub": coach_user.email, "user_id": coach_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/bookings/book",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "coach_id": coach_user.id,
                    "slot_number": 1
                }
            )
        
        assert response.status_code == 403


class TestGetMyBookings:
    """Tests for getting user's bookings"""
    
    async def test_client_get_bookings(self, test_db, client_user, booking):
        """Test client getting their bookings"""
        token = create_access_token({"sub": client_user.email, "user_id": client_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/v1/bookings/my-bookings",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        assert response.status_code == 200
        bookings = response.json()
        assert len(bookings) >= 1
        assert bookings[0]["client_id"] == client_user.id
        assert bookings[0]["coach_name"] == "Test Coach"
    
    async def test_coach_get_bookings(self, test_db, coach_user, booking):
        """Test coach getting their bookings"""
        token = create_access_token({"sub": coach_user.email, "user_id": coach_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/v1/bookings/my-bookings",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        assert response.status_code == 200
        bookings = response.json()
        assert len(bookings) >= 1
        assert bookings[0]["coach_id"] == coach_user.id
        assert bookings[0]["client_name"] == "Test Client"


class TestUpdateBooking:
    """Tests for updating bookings"""
    
    async def test_coach_confirm_booking(self, test_db, coach_user, booking):
        """Test coach confirming a booking"""
        token = create_access_token({"sub": coach_user.email, "user_id": coach_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.put(
                f"/api/v1/bookings/bookings/{booking.id}",
                headers={"Authorization": f"Bearer {token}"},
                json={"status": "confirmed"}
            )
        
        assert response.status_code == 200
        booking_data = response.json()
        assert booking_data["status"] == "confirmed"
    
    async def test_client_cancel_booking(self, test_db, client_user, coach_user, booking):
        """Test client canceling a booking"""
        token = create_access_token({"sub": client_user.email, "user_id": client_user.id})
        
        # Store initial available slots
        initial_slots = coach_user.available_slots
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.put(
                f"/api/v1/bookings/bookings/{booking.id}",
                headers={"Authorization": f"Bearer {token}"},
                json={"status": "cancelled"}
            )
        
        assert response.status_code == 200
        booking_data = response.json()
        assert booking_data["status"] == "cancelled"
        
        # Verify coach's available slots increased
        await test_db.refresh(coach_user)
        assert coach_user.available_slots == initial_slots + 1
    
    async def test_client_cannot_confirm_booking(self, test_db, client_user, booking):
        """Test that clients cannot confirm bookings"""
        token = create_access_token({"sub": client_user.email, "user_id": client_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.put(
                f"/api/v1/bookings/bookings/{booking.id}",
                headers={"Authorization": f"Bearer {token}"},
                json={"status": "confirmed"}
            )
        
        assert response.status_code == 403
    
    async def test_update_booking_not_found(self, test_db, coach_user):
        """Test updating non-existent booking"""
        token = create_access_token({"sub": coach_user.email, "user_id": coach_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.put(
                "/api/v1/bookings/bookings/9999",
                headers={"Authorization": f"Bearer {token}"},
                json={"status": "confirmed"}
            )
        
        assert response.status_code == 404


class TestCoachBookings:
    """Tests for coach booking endpoints"""
    
    async def test_coach_get_own_bookings(self, test_db, coach_user, booking):
        """Test coach getting their own bookings"""
        token = create_access_token({"sub": coach_user.email, "user_id": coach_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/v1/bookings/coach/bookings",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        assert response.status_code == 200
        bookings = response.json()
        assert len(bookings) >= 1
        assert all(b["coach_id"] == coach_user.id for b in bookings)


class TestAdminBookings:
    """Tests for admin booking endpoints"""
    
    async def test_admin_get_all_bookings(self, test_db, admin_user, booking):
        """Test admin getting all bookings"""
        token = create_access_token({"sub": admin_user.email, "user_id": admin_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/v1/bookings/admin/bookings",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        assert response.status_code == 200
        bookings = response.json()
        assert len(bookings) >= 1
    
    async def test_admin_get_coach_calendar(self, test_db, admin_user, coach_user, booking):
        """Test admin getting specific coach's calendar"""
        token = create_access_token({"sub": admin_user.email, "user_id": admin_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.get(
                f"/api/v1/bookings/admin/coaches/{coach_user.id}/bookings",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        assert response.status_code == 200
        bookings = response.json()
        assert len(bookings) >= 1
        assert all(b["coach_id"] == coach_user.id for b in bookings)
    
    async def test_non_admin_cannot_access_admin_endpoints(self, test_db, client_user):
        """Test that non-admins cannot access admin endpoints"""
        token = create_access_token({"sub": client_user.email, "user_id": client_user.id})
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/v1/bookings/admin/bookings",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        assert response.status_code == 403
