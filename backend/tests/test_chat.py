"""
Tests for chat endpoints
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.models.chat import ChatRoom, Message, UserPresence, ChatRoomType, MessageType


@pytest.mark.asyncio
async def test_create_direct_chat_room(
    async_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test creating a direct chat room"""
    # Create another user to chat with
    other_user = User(
        email="other@example.com",
        hashed_password="hashed",
        full_name="Other User",
        role=UserRole.CLIENT,
        is_active=True
    )
    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)
    
    # Create direct chat
    response = await async_client.post(
        "/api/v1/chat/rooms",
        json={
            "participant_ids": [other_user.id],
            "type": "direct"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "direct"
    assert data["participant_count"] == 2


@pytest.mark.asyncio
async def test_create_group_chat_room(
    async_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test creating a group chat room"""
    # Create other users
    user1 = User(
        email="user1@example.com",
        hashed_password="hashed",
        full_name="User One",
        role=UserRole.CLIENT,
        is_active=True
    )
    user2 = User(
        email="user2@example.com",
        hashed_password="hashed",
        full_name="User Two",
        role=UserRole.CLIENT,
        is_active=True
    )
    db_session.add_all([user1, user2])
    await db_session.commit()
    await db_session.refresh(user1)
    await db_session.refresh(user2)
    
    # Create group chat
    response = await async_client.post(
        "/api/v1/chat/rooms",
        json={
            "participant_ids": [user1.id, user2.id],
            "name": "Test Group",
            "type": "group"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "group"
    assert data["name"] == "Test Group"
    assert data["participant_count"] == 3  # Creator + 2 participants


@pytest.mark.asyncio
async def test_get_chat_rooms(
    async_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test getting user's chat rooms"""
    # Create a chat room first
    other_user = User(
        email="other@example.com",
        hashed_password="hashed",
        full_name="Other User",
        role=UserRole.CLIENT,
        is_active=True
    )
    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)
    
    await async_client.post(
        "/api/v1/chat/rooms",
        json={
            "participant_ids": [other_user.id],
            "type": "direct"
        },
        headers=auth_headers
    )
    
    # Get chat rooms
    response = await async_client.get(
        "/api/v1/chat/rooms",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["type"] == "direct"


@pytest.mark.asyncio
async def test_send_message(
    async_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test sending a message"""
    # Create a chat room
    other_user = User(
        email="other@example.com",
        hashed_password="hashed",
        full_name="Other User",
        role=UserRole.CLIENT,
        is_active=True
    )
    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)
    
    room_response = await async_client.post(
        "/api/v1/chat/rooms",
        json={
            "participant_ids": [other_user.id],
            "type": "direct"
        },
        headers=auth_headers
    )
    room_id = room_response.json()["id"]
    
    # Send message
    response = await async_client.post(
        "/api/v1/chat/messages",
        json={
            "chat_room_id": room_id,
            "content": "Hello, World!",
            "message_type": "text"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Hello, World!"
    assert data["sender_id"] == test_user.id
    assert data["message_type"] == "text"


@pytest.mark.asyncio
async def test_get_chat_room_with_messages(
    async_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test getting chat room with messages"""
    # Create a chat room
    other_user = User(
        email="other@example.com",
        hashed_password="hashed",
        full_name="Other User",
        role=UserRole.CLIENT,
        is_active=True
    )
    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)
    
    room_response = await async_client.post(
        "/api/v1/chat/rooms",
        json={
            "participant_ids": [other_user.id],
            "type": "direct"
        },
        headers=auth_headers
    )
    room_id = room_response.json()["id"]
    
    # Send a message
    await async_client.post(
        "/api/v1/chat/messages",
        json={
            "chat_room_id": room_id,
            "content": "Test message",
            "message_type": "text"
        },
        headers=auth_headers
    )
    
    # Get room with messages
    response = await async_client.get(
        f"/api/v1/chat/rooms/{room_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == room_id
    assert len(data["messages"]) > 0
    assert data["messages"][0]["content"] == "Test message"


@pytest.mark.asyncio
async def test_update_message(
    async_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test updating a message"""
    # Create room and send message
    other_user = User(
        email="other@example.com",
        hashed_password="hashed",
        full_name="Other User",
        role=UserRole.CLIENT,
        is_active=True
    )
    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)
    
    room_response = await async_client.post(
        "/api/v1/chat/rooms",
        json={
            "participant_ids": [other_user.id],
            "type": "direct"
        },
        headers=auth_headers
    )
    room_id = room_response.json()["id"]
    
    msg_response = await async_client.post(
        "/api/v1/chat/messages",
        json={
            "chat_room_id": room_id,
            "content": "Original message",
            "message_type": "text"
        },
        headers=auth_headers
    )
    message_id = msg_response.json()["id"]
    
    # Update message
    response = await async_client.put(
        f"/api/v1/chat/messages/{message_id}",
        json={"content": "Updated message"},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated message"
    assert data["is_edited"] == True


@pytest.mark.asyncio
async def test_delete_message(
    async_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test deleting a message"""
    # Create room and send message
    other_user = User(
        email="other@example.com",
        hashed_password="hashed",
        full_name="Other User",
        role=UserRole.CLIENT,
        is_active=True
    )
    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)
    
    room_response = await async_client.post(
        "/api/v1/chat/rooms",
        json={
            "participant_ids": [other_user.id],
            "type": "direct"
        },
        headers=auth_headers
    )
    room_id = room_response.json()["id"]
    
    msg_response = await async_client.post(
        "/api/v1/chat/messages",
        json={
            "chat_room_id": room_id,
            "content": "Message to delete",
            "message_type": "text"
        },
        headers=auth_headers
    )
    message_id = msg_response.json()["id"]
    
    # Delete message
    response = await async_client.delete(
        f"/api/v1/chat/messages/{message_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_online_users(
    async_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test getting online users"""
    response = await async_client.get(
        "/api/v1/chat/presence",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_cannot_send_message_to_non_participant_room(
    async_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test that non-participants cannot send messages"""
    # Create two other users
    user1 = User(
        email="user1@example.com",
        hashed_password="hashed",
        full_name="User One",
        role=UserRole.CLIENT,
        is_active=True
    )
    user2 = User(
        email="user2@example.com",
        hashed_password="hashed",
        full_name="User Two",
        role=UserRole.CLIENT,
        is_active=True
    )
    db_session.add_all([user1, user2])
    await db_session.commit()
    await db_session.refresh(user1)
    await db_session.refresh(user2)
    
    # Create a room between user1 and user2 (not including test_user)
    from app.models.chat import ChatRoom, chat_participants
    import time
    
    room = ChatRoom(
        type=ChatRoomType.DIRECT,
        created_by_id=user1.id
    )
    db_session.add(room)
    await db_session.flush()
    
    current_time = int(time.time())
    stmt1 = chat_participants.insert().values(
        chat_room_id=room.id,
        user_id=user1.id,
        joined_at=current_time
    )
    stmt2 = chat_participants.insert().values(
        chat_room_id=room.id,
        user_id=user2.id,
        joined_at=current_time
    )
    await db_session.execute(stmt1)
    await db_session.execute(stmt2)
    await db_session.commit()
    await db_session.refresh(room)
    
    # Try to send message (should fail)
    response = await async_client.post(
        "/api/v1/chat/messages",
        json={
            "chat_room_id": room.id,
            "content": "Unauthorized message",
            "message_type": "text"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_mark_messages_as_read(
    async_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test marking messages as read"""
    # Create a chat room
    other_user = User(
        email="other@example.com",
        hashed_password="hashed",
        full_name="Other User",
        role=UserRole.CLIENT,
        is_active=True
    )
    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)
    
    room_response = await async_client.post(
        "/api/v1/chat/rooms",
        json={
            "participant_ids": [other_user.id],
            "type": "direct"
        },
        headers=auth_headers
    )
    room_id = room_response.json()["id"]
    
    # Mark as read
    response = await async_client.post(
        "/api/v1/chat/mark-read",
        json={"chat_room_id": room_id},
        headers=auth_headers
    )
    
    assert response.status_code == 200
