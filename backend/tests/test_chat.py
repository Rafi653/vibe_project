"""
Tests for chat endpoints
"""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select

from app.main import app
from app.models.user import User, UserRole
from app.models.chat import Conversation, Message, UserPresence, ConversationType, MessageStatus
from app.core.security import create_access_token


@pytest.fixture
async def client_user(test_db):
    """Create a test client user"""
    user = User(
        email="client1@example.com",
        hashed_password="hashed_password",
        full_name="Test Client 1",
        role=UserRole.CLIENT,
        is_active=True,
        is_verified=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def client_user_2(test_db):
    """Create a second test client user"""
    user = User(
        email="client2@example.com",
        hashed_password="hashed_password",
        full_name="Test Client 2",
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
    """Create a test client token"""
    return create_access_token(data={"sub": client_user.email, "user_id": client_user.id})


@pytest.fixture
def client_token_2(client_user_2):
    """Create a test client token for second user"""
    return create_access_token(data={"sub": client_user_2.email, "user_id": client_user_2.id})


@pytest.mark.asyncio
async def test_create_direct_conversation(test_db, client_user, client_user_2, client_token):
    """Test creating a direct conversation"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/chat/conversations",
            json={
                "type": "direct",
                "participant_ids": [client_user_2.id]
            },
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "direct"
    assert client_user.id in data["participant_ids"]
    assert client_user_2.id in data["participant_ids"]


@pytest.mark.asyncio
async def test_create_duplicate_direct_conversation(test_db, client_user, client_user_2, client_token):
    """Test that creating a duplicate direct conversation returns the existing one"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create first conversation
        response1 = await ac.post(
            "/api/v1/chat/conversations",
            json={
                "type": "direct",
                "participant_ids": [client_user_2.id]
            },
            headers={"Authorization": f"Bearer {client_token}"}
        )
        
        # Try to create same conversation again
        response2 = await ac.post(
            "/api/v1/chat/conversations",
            json={
                "type": "direct",
                "participant_ids": [client_user_2.id]
            },
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    
    # Should return the same conversation
    data1 = response1.json()
    data2 = response2.json()
    assert data1["id"] == data2["id"]


@pytest.mark.asyncio
async def test_create_group_conversation(test_db, client_user, client_user_2, client_token):
    """Test creating a group conversation"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/chat/conversations",
            json={
                "type": "group",
                "name": "Test Group",
                "participant_ids": [client_user_2.id]
            },
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "group"
    assert data["name"] == "Test Group"
    assert client_user.id in data["participant_ids"]
    assert client_user_2.id in data["participant_ids"]


@pytest.mark.asyncio
async def test_get_conversations(test_db, client_user, client_user_2, client_token):
    """Test getting all conversations for a user"""
    # Create a conversation first
    conversation = Conversation(
        type=ConversationType.DIRECT,
        created_by_id=client_user.id
    )
    conversation.participants = [client_user, client_user_2]
    test_db.add(conversation)
    await test_db.commit()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/chat/conversations",
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(conv["id"] == conversation.id for conv in data)


@pytest.mark.asyncio
async def test_get_conversation_detail(test_db, client_user, client_user_2, client_token):
    """Test getting a specific conversation with messages"""
    # Create a conversation with a message
    conversation = Conversation(
        type=ConversationType.DIRECT,
        created_by_id=client_user.id
    )
    conversation.participants = [client_user, client_user_2]
    test_db.add(conversation)
    await test_db.flush()
    
    message = Message(
        conversation_id=conversation.id,
        sender_id=client_user.id,
        content="Test message",
        status=MessageStatus.SENT
    )
    test_db.add(message)
    await test_db.commit()
    await test_db.refresh(conversation)
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            f"/api/v1/chat/conversations/{conversation.id}",
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conversation.id
    assert len(data["messages"]) == 1
    assert data["messages"][0]["content"] == "Test message"


@pytest.mark.asyncio
async def test_get_conversation_unauthorized(test_db, client_user, client_user_2, client_token, client_token_2):
    """Test that users can't access conversations they're not part of"""
    # Create a conversation without client_user_2
    conversation = Conversation(
        type=ConversationType.DIRECT,
        created_by_id=client_user.id
    )
    conversation.participants = [client_user]
    test_db.add(conversation)
    await test_db.commit()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            f"/api/v1/chat/conversations/{conversation.id}",
            headers={"Authorization": f"Bearer {client_token_2}"}
        )
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_active_users(test_db, client_user, client_user_2, client_token):
    """Test getting active users"""
    # Create presence for client_user_2
    presence = UserPresence(
        user_id=client_user_2.id,
        is_online=True,
        last_seen="2025-10-15T12:00:00"
    )
    test_db.add(presence)
    await test_db.commit()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/chat/active-users",
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "online_users" in data
    assert any(user["id"] == client_user_2.id for user in data["online_users"])


@pytest.mark.asyncio
async def test_get_user_presence(test_db, client_user, client_user_2, client_token):
    """Test getting presence for a specific user"""
    # Create presence for client_user_2
    presence = UserPresence(
        user_id=client_user_2.id,
        is_online=True,
        last_seen="2025-10-15T12:00:00"
    )
    test_db.add(presence)
    await test_db.commit()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            f"/api/v1/chat/presence/{client_user_2.id}",
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == client_user_2.id
    assert data["is_online"] is True


@pytest.mark.asyncio
async def test_get_user_presence_not_found(test_db, client_user, client_user_2, client_token):
    """Test getting presence for a user without presence record"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            f"/api/v1/chat/presence/{client_user_2.id}",
            headers={"Authorization": f"Bearer {client_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == client_user_2.id
    assert data["is_online"] is False
    assert data["last_seen"] is None
