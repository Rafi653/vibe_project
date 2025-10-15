"""
Tests for chat endpoints
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.user import User, UserRole
from app.models.chat import Conversation, ConversationParticipant, Message, ConversationType
from app.core.security import get_password_hash


@pytest.fixture
async def test_users(test_db):
    """Create test users in the database"""
    async with test_db as session:
        user1 = User(
            email="user1@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="User One",
            role=UserRole.CLIENT,
            is_active=True,
            is_verified=True
        )
        user2 = User(
            email="user2@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="User Two",
            role=UserRole.CLIENT,
            is_active=True,
            is_verified=True
        )
        user3 = User(
            email="user3@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="User Three",
            role=UserRole.COACH,
            is_active=True,
            is_verified=True
        )
        session.add_all([user1, user2, user3])
        await session.commit()
        await session.refresh(user1)
        await session.refresh(user2)
        await session.refresh(user3)
        return [user1, user2, user3]


@pytest.fixture
async def auth_token(test_users):
    """Get authentication token for user1"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "user1@example.com",
                "password": "password123"
            }
        )
        data = response.json()
        return data["access_token"]


@pytest.mark.asyncio
async def test_create_direct_conversation(auth_token, test_users):
    """Test creating a direct conversation"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/chat/conversations",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "conversation_type": "direct",
                "participant_ids": [test_users[1].id],
                "name": None
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["conversation_type"] == "direct"
        assert len(data["participants"]) == 2


@pytest.mark.asyncio
async def test_create_group_conversation(auth_token, test_users):
    """Test creating a group conversation"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/chat/conversations",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "conversation_type": "group",
                "participant_ids": [test_users[1].id, test_users[2].id],
                "name": "Test Group"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["conversation_type"] == "group"
        assert data["name"] == "Test Group"
        assert len(data["participants"]) == 3


@pytest.mark.asyncio
async def test_get_conversations(auth_token):
    """Test getting all conversations"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/v1/chat/conversations",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_send_message(auth_token, test_users, test_db):
    """Test sending a message"""
    # Create a conversation first
    async with test_db as session:
        conversation = Conversation(
            conversation_type=ConversationType.DIRECT,
            is_active=True
        )
        session.add(conversation)
        await session.flush()
        
        participant1 = ConversationParticipant(
            conversation_id=conversation.id,
            user_id=test_users[0].id,
            is_admin=False
        )
        participant2 = ConversationParticipant(
            conversation_id=conversation.id,
            user_id=test_users[1].id,
            is_admin=False
        )
        session.add_all([participant1, participant2])
        await session.commit()
        await session.refresh(conversation)
        conversation_id = conversation.id
    
    # Send a message
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            f"/api/v1/chat/conversations/{conversation_id}/messages",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "conversation_id": conversation_id,
                "content": "Hello, this is a test message"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "Hello, this is a test message"
        assert data["conversation_id"] == conversation_id


@pytest.mark.asyncio
async def test_get_conversation_with_messages(auth_token, test_users, test_db):
    """Test getting a conversation with messages"""
    # Create conversation with messages
    async with test_db as session:
        conversation = Conversation(
            conversation_type=ConversationType.DIRECT,
            is_active=True
        )
        session.add(conversation)
        await session.flush()
        
        participant1 = ConversationParticipant(
            conversation_id=conversation.id,
            user_id=test_users[0].id,
            is_admin=False
        )
        participant2 = ConversationParticipant(
            conversation_id=conversation.id,
            user_id=test_users[1].id,
            is_admin=False
        )
        session.add_all([participant1, participant2])
        await session.flush()
        
        message = Message(
            conversation_id=conversation.id,
            sender_id=test_users[0].id,
            content="Test message",
            is_read=False
        )
        session.add(message)
        await session.commit()
        conversation_id = conversation.id
    
    # Get conversation
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get(
            f"/api/v1/chat/conversations/{conversation_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == conversation_id
        assert len(data["messages"]) > 0


@pytest.mark.asyncio
async def test_update_message(auth_token, test_users, test_db):
    """Test updating a message"""
    # Create a message first
    async with test_db as session:
        conversation = Conversation(
            conversation_type=ConversationType.DIRECT,
            is_active=True
        )
        session.add(conversation)
        await session.flush()
        
        participant = ConversationParticipant(
            conversation_id=conversation.id,
            user_id=test_users[0].id,
            is_admin=False
        )
        session.add(participant)
        await session.flush()
        
        message = Message(
            conversation_id=conversation.id,
            sender_id=test_users[0].id,
            content="Original message",
            is_read=False
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)
        message_id = message.id
    
    # Update the message
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.patch(
            f"/api/v1/chat/messages/{message_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"content": "Updated message"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Updated message"
        assert data["is_edited"] == True


@pytest.mark.asyncio
async def test_delete_message(auth_token, test_users, test_db):
    """Test deleting a message"""
    # Create a message first
    async with test_db as session:
        conversation = Conversation(
            conversation_type=ConversationType.DIRECT,
            is_active=True
        )
        session.add(conversation)
        await session.flush()
        
        participant = ConversationParticipant(
            conversation_id=conversation.id,
            user_id=test_users[0].id,
            is_admin=False
        )
        session.add(participant)
        await session.flush()
        
        message = Message(
            conversation_id=conversation.id,
            sender_id=test_users[0].id,
            content="Message to delete",
            is_read=False
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)
        message_id = message.id
    
    # Delete the message
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.delete(
            f"/api/v1/chat/messages/{message_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_active_users(auth_token):
    """Test getting list of active users"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/v1/chat/users/active",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_unauthorized_access(test_users):
    """Test that unauthorized users cannot access chat endpoints"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/chat/conversations")
        
        assert response.status_code == 401
