"""
Chat endpoints for real-time messaging
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from typing import List, Dict
import time
import json

from app.core.dependencies import get_current_active_user, get_db
from app.models.user import User
from app.models.chat import ChatRoom, Message, UserPresence, ChatRoomType, MessageType, chat_participants
from app.schemas.chat import (
    ChatRoomCreate, ChatRoomResponse, ChatRoomWithMessages,
    MessageCreate, MessageResponse, MessageUpdate,
    UserPresenceResponse, ChatParticipantAdd, MarkAsReadRequest
)

router = APIRouter()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(message)
            except:
                self.disconnect(user_id)
    
    async def broadcast_to_room(self, message: str, room_participants: List[int]):
        for user_id in room_participants:
            await self.send_personal_message(message, user_id)

manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(user_id, websocket)
    
    # Update user presence to online
    presence_query = select(UserPresence).where(UserPresence.user_id == user_id)
    result = await db.execute(presence_query)
    presence = result.scalar_one_or_none()
    
    if presence:
        presence.is_online = True
        presence.last_seen = int(time.time())
    else:
        presence = UserPresence(
            user_id=user_id,
            is_online=True,
            last_seen=int(time.time())
        )
        db.add(presence)
    
    await db.commit()
    
    # Broadcast presence update
    await manager.broadcast_to_room(
        json.dumps({"type": "presence", "user_id": user_id, "is_online": True}),
        list(manager.active_connections.keys())
    )
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Handle different message types
            if message_data.get("type") == "message":
                # Broadcast message to room participants
                room_id = message_data.get("chat_room_id")
                
                # Get room participants
                stmt = select(chat_participants.c.user_id).where(
                    chat_participants.c.chat_room_id == room_id
                )
                result = await db.execute(stmt)
                participants = [row[0] for row in result]
                
                await manager.broadcast_to_room(data, participants)
            
            elif message_data.get("type") == "typing":
                # Broadcast typing indicator
                room_id = message_data.get("chat_room_id")
                stmt = select(chat_participants.c.user_id).where(
                    chat_participants.c.chat_room_id == room_id
                )
                result = await db.execute(stmt)
                participants = [row[0] for row in result if row[0] != user_id]
                
                await manager.broadcast_to_room(data, participants)
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        
        # Update user presence to offline
        presence_query = select(UserPresence).where(UserPresence.user_id == user_id)
        result = await db.execute(presence_query)
        presence = result.scalar_one_or_none()
        
        if presence:
            presence.is_online = False
            presence.last_seen = int(time.time())
            await db.commit()
        
        # Broadcast presence update
        await manager.broadcast_to_room(
            json.dumps({"type": "presence", "user_id": user_id, "is_online": False}),
            list(manager.active_connections.keys())
        )


@router.post("/rooms", response_model=ChatRoomResponse)
async def create_chat_room(
    room_data: ChatRoomCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new chat room"""
    
    # For direct chats, check if room already exists
    if room_data.type == ChatRoomType.DIRECT:
        if len(room_data.participant_ids) != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Direct chat must have exactly one other participant"
            )
        
        other_user_id = room_data.participant_ids[0]
        
        # Check if direct chat already exists
        existing_room_query = select(ChatRoom).join(
            chat_participants, ChatRoom.id == chat_participants.c.chat_room_id
        ).where(
            and_(
                ChatRoom.type == ChatRoomType.DIRECT,
                chat_participants.c.user_id.in_([current_user.id, other_user_id])
            )
        ).group_by(ChatRoom.id).having(func.count(chat_participants.c.user_id) == 2)
        
        result = await db.execute(existing_room_query)
        existing_room = result.scalar_one_or_none()
        
        if existing_room:
            return ChatRoomResponse(
                id=existing_room.id,
                name=existing_room.name,
                type=existing_room.type,
                created_by_id=existing_room.created_by_id,
                created_at=existing_room.created_at,
                updated_at=existing_room.updated_at,
                participant_count=2,
                last_message=None,
                last_message_at=None
            )
    
    # Create new chat room
    new_room = ChatRoom(
        name=room_data.name,
        type=room_data.type,
        created_by_id=current_user.id
    )
    db.add(new_room)
    await db.flush()
    
    # Add participants
    current_time = int(time.time())
    participants = [current_user.id] + room_data.participant_ids
    
    for participant_id in set(participants):  # Use set to avoid duplicates
        stmt = chat_participants.insert().values(
            chat_room_id=new_room.id,
            user_id=participant_id,
            joined_at=current_time
        )
        await db.execute(stmt)
    
    await db.commit()
    await db.refresh(new_room)
    
    return ChatRoomResponse(
        id=new_room.id,
        name=new_room.name,
        type=new_room.type,
        created_by_id=new_room.created_by_id,
        created_at=new_room.created_at,
        updated_at=new_room.updated_at,
        participant_count=len(set(participants)),
        last_message=None,
        last_message_at=None
    )


@router.get("/rooms", response_model=List[ChatRoomResponse])
async def get_chat_rooms(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all chat rooms for current user"""
    
    # Get rooms where user is a participant
    stmt = select(ChatRoom).join(
        chat_participants, ChatRoom.id == chat_participants.c.chat_room_id
    ).where(
        chat_participants.c.user_id == current_user.id
    ).order_by(desc(ChatRoom.updated_at))
    
    result = await db.execute(stmt)
    rooms = result.scalars().all()
    
    response_rooms = []
    for room in rooms:
        # Get participant count
        count_stmt = select(func.count(chat_participants.c.user_id)).where(
            chat_participants.c.chat_room_id == room.id
        )
        count_result = await db.execute(count_stmt)
        participant_count = count_result.scalar()
        
        # Get last message
        last_msg_stmt = select(Message).where(
            Message.chat_room_id == room.id
        ).order_by(desc(Message.created_at)).limit(1)
        last_msg_result = await db.execute(last_msg_stmt)
        last_message = last_msg_result.scalar_one_or_none()
        
        response_rooms.append(ChatRoomResponse(
            id=room.id,
            name=room.name,
            type=room.type,
            created_by_id=room.created_by_id,
            created_at=room.created_at,
            updated_at=room.updated_at,
            participant_count=participant_count,
            last_message=last_message.content if last_message else None,
            last_message_at=last_message.created_at if last_message else None
        ))
    
    return response_rooms


@router.get("/rooms/{room_id}", response_model=ChatRoomWithMessages)
async def get_chat_room(
    room_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get chat room details with messages"""
    
    # Verify user is a participant
    participant_stmt = select(chat_participants).where(
        and_(
            chat_participants.c.chat_room_id == room_id,
            chat_participants.c.user_id == current_user.id
        )
    )
    participant_result = await db.execute(participant_stmt)
    if not participant_result.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant of this chat room"
        )
    
    # Get room
    room_stmt = select(ChatRoom).where(ChatRoom.id == room_id)
    room_result = await db.execute(room_stmt)
    room = room_result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat room not found"
        )
    
    # Get messages
    messages_stmt = select(Message).where(
        Message.chat_room_id == room_id
    ).order_by(Message.created_at)
    messages_result = await db.execute(messages_stmt)
    messages = messages_result.scalars().all()
    
    # Get participants
    participants_stmt = select(chat_participants.c.user_id).where(
        chat_participants.c.chat_room_id == room_id
    )
    participants_result = await db.execute(participants_stmt)
    participants = [row[0] for row in participants_result]
    
    # Convert messages to response format
    message_responses = []
    for msg in messages:
        sender_stmt = select(User).where(User.id == msg.sender_id)
        sender_result = await db.execute(sender_stmt)
        sender = sender_result.scalar_one()
        
        message_responses.append(MessageResponse(
            id=msg.id,
            chat_room_id=msg.chat_room_id,
            sender_id=msg.sender_id,
            sender_name=sender.full_name,
            content=msg.content,
            message_type=msg.message_type,
            is_edited=msg.is_edited,
            created_at=msg.created_at,
            updated_at=msg.updated_at
        ))
    
    return ChatRoomWithMessages(
        id=room.id,
        name=room.name,
        type=room.type,
        created_by_id=room.created_by_id,
        created_at=room.created_at,
        updated_at=room.updated_at,
        participant_count=len(participants),
        last_message=messages[-1].content if messages else None,
        last_message_at=messages[-1].created_at if messages else None,
        messages=message_responses,
        participants=participants
    )


@router.post("/messages", response_model=MessageResponse)
async def send_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Send a message to a chat room"""
    
    # Verify user is a participant
    participant_stmt = select(chat_participants).where(
        and_(
            chat_participants.c.chat_room_id == message_data.chat_room_id,
            chat_participants.c.user_id == current_user.id
        )
    )
    participant_result = await db.execute(participant_stmt)
    if not participant_result.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant of this chat room"
        )
    
    # Create message
    new_message = Message(
        chat_room_id=message_data.chat_room_id,
        sender_id=current_user.id,
        content=message_data.content,
        message_type=message_data.message_type
    )
    db.add(new_message)
    
    # Update room updated_at
    room_stmt = select(ChatRoom).where(ChatRoom.id == message_data.chat_room_id)
    room_result = await db.execute(room_stmt)
    room = room_result.scalar_one()
    room.updated_at = new_message.created_at
    
    await db.commit()
    await db.refresh(new_message)
    
    return MessageResponse(
        id=new_message.id,
        chat_room_id=new_message.chat_room_id,
        sender_id=new_message.sender_id,
        sender_name=current_user.full_name,
        content=new_message.content,
        message_type=new_message.message_type,
        is_edited=new_message.is_edited,
        created_at=new_message.created_at,
        updated_at=new_message.updated_at
    )


@router.put("/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: int,
    message_update: MessageUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a message (edit)"""
    
    # Get message
    msg_stmt = select(Message).where(Message.id == message_id)
    msg_result = await db.execute(msg_stmt)
    message = msg_result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    if message.sender_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own messages"
        )
    
    message.content = message_update.content
    message.is_edited = True
    await db.commit()
    await db.refresh(message)
    
    return MessageResponse(
        id=message.id,
        chat_room_id=message.chat_room_id,
        sender_id=message.sender_id,
        sender_name=current_user.full_name,
        content=message.content,
        message_type=message.message_type,
        is_edited=message.is_edited,
        created_at=message.created_at,
        updated_at=message.updated_at
    )


@router.delete("/messages/{message_id}")
async def delete_message(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a message"""
    
    # Get message
    msg_stmt = select(Message).where(Message.id == message_id)
    msg_result = await db.execute(msg_stmt)
    message = msg_result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    if message.sender_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own messages"
        )
    
    await db.delete(message)
    await db.commit()
    
    return {"message": "Message deleted successfully"}


@router.get("/presence", response_model=List[UserPresenceResponse])
async def get_online_users(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of online users"""
    
    stmt = select(UserPresence, User).join(
        User, UserPresence.user_id == User.id
    ).where(UserPresence.is_online == True)
    
    result = await db.execute(stmt)
    online_users = result.all()
    
    return [
        UserPresenceResponse(
            user_id=presence.user_id,
            user_name=user.full_name,
            is_online=presence.is_online,
            last_seen=presence.last_seen
        )
        for presence, user in online_users
    ]


@router.post("/rooms/{room_id}/participants", response_model=ChatRoomResponse)
async def add_participants(
    room_id: int,
    participant_data: ChatParticipantAdd,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Add participants to a chat room (group chat only)"""
    
    # Get room
    room_stmt = select(ChatRoom).where(ChatRoom.id == room_id)
    room_result = await db.execute(room_stmt)
    room = room_result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat room not found"
        )
    
    if room.type != ChatRoomType.GROUP:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only add participants to group chats"
        )
    
    # Verify current user is a participant
    participant_stmt = select(chat_participants).where(
        and_(
            chat_participants.c.chat_room_id == room_id,
            chat_participants.c.user_id == current_user.id
        )
    )
    participant_result = await db.execute(participant_stmt)
    if not participant_result.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant of this chat room"
        )
    
    # Add new participants
    current_time = int(time.time())
    for user_id in participant_data.user_ids:
        # Check if already a participant
        existing_stmt = select(chat_participants).where(
            and_(
                chat_participants.c.chat_room_id == room_id,
                chat_participants.c.user_id == user_id
            )
        )
        existing_result = await db.execute(existing_stmt)
        if not existing_result.first():
            stmt = chat_participants.insert().values(
                chat_room_id=room_id,
                user_id=user_id,
                joined_at=current_time
            )
            await db.execute(stmt)
    
    await db.commit()
    
    # Get updated participant count
    count_stmt = select(func.count(chat_participants.c.user_id)).where(
        chat_participants.c.chat_room_id == room_id
    )
    count_result = await db.execute(count_stmt)
    participant_count = count_result.scalar()
    
    return ChatRoomResponse(
        id=room.id,
        name=room.name,
        type=room.type,
        created_by_id=room.created_by_id,
        created_at=room.created_at,
        updated_at=room.updated_at,
        participant_count=participant_count,
        last_message=None,
        last_message_at=None
    )


@router.post("/mark-read")
async def mark_as_read(
    mark_read: MarkAsReadRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark messages as read in a chat room"""
    
    # Update last_read_at
    stmt = chat_participants.update().where(
        and_(
            chat_participants.c.chat_room_id == mark_read.chat_room_id,
            chat_participants.c.user_id == current_user.id
        )
    ).values(last_read_at=int(time.time()))
    
    await db.execute(stmt)
    await db.commit()
    
    return {"message": "Messages marked as read"}
