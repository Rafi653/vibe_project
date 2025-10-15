"""
Chat endpoints - for real-time messaging
"""

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from typing import List, Optional, Dict
from datetime import datetime

from app.db.base import get_db
from app.core.dependencies import get_current_user
from app.core.security import decode_access_token
from app.models.user import User
from app.models.chat import Conversation, Message, UserPresence, ConversationType, MessageStatus
from app.schemas.chat import (
    ConversationCreate,
    ConversationResponse,
    ConversationDetail,
    MessageCreate,
    MessageResponse,
    UserPresenceResponse,
    ActiveUsersResponse,
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

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except Exception:
                self.disconnect(user_id)

    async def broadcast_to_conversation(self, message: dict, conversation_id: int, db: AsyncSession):
        """Broadcast message to all participants in a conversation"""
        from sqlalchemy.orm import selectinload
        
        result = await db.execute(
            select(Conversation)
            .options(selectinload(Conversation.participants))
            .where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if conversation:
            for participant in conversation.participants:
                await self.send_personal_message(message, participant.id)

    async def broadcast_presence(self, user_id: int, is_online: bool):
        """Broadcast user presence to all connected users"""
        message = {
            "type": "presence",
            "user_id": user_id,
            "is_online": is_online
        }
        for user_id_conn in list(self.active_connections.keys()):
            await self.send_personal_message(message, user_id_conn)


manager = ConnectionManager()


@router.websocket("/ws/{token}")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    WebSocket endpoint for real-time chat
    
    Connect using: ws://localhost:8000/api/v1/chat/ws/{token}
    """
    # Authenticate user from token
    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    user_id = payload.get("user_id")
    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Connect user
    await manager.connect(user_id, websocket)
    
    # Update user presence to online
    result = await db.execute(
        select(UserPresence).where(UserPresence.user_id == user_id)
    )
    presence = result.scalar_one_or_none()
    
    if presence:
        presence.is_online = True
        presence.last_seen = datetime.utcnow().isoformat()
    else:
        presence = UserPresence(
            user_id=user_id,
            is_online=True,
            last_seen=datetime.utcnow().isoformat()
        )
        db.add(presence)
    
    await db.commit()
    await manager.broadcast_presence(user_id, True)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle different message types
            if data.get("type") == "message":
                # Create new message
                conversation_id = data.get("conversation_id")
                content = data.get("content")
                
                if conversation_id and content:
                    message = Message(
                        conversation_id=conversation_id,
                        sender_id=user_id,
                        content=content,
                        status=MessageStatus.SENT
                    )
                    db.add(message)
                    await db.commit()
                    await db.refresh(message)
                    
                    # Broadcast to conversation participants
                    response = {
                        "type": "message",
                        "message": {
                            "id": message.id,
                            "conversation_id": message.conversation_id,
                            "sender_id": message.sender_id,
                            "content": message.content,
                            "status": message.status.value,
                            "created_at": message.created_at.isoformat(),
                            "updated_at": message.updated_at.isoformat(),
                        }
                    }
                    await manager.broadcast_to_conversation(response, conversation_id, db)
            
            elif data.get("type") == "typing":
                # Broadcast typing indicator
                conversation_id = data.get("conversation_id")
                if conversation_id:
                    typing_message = {
                        "type": "typing",
                        "conversation_id": conversation_id,
                        "user_id": user_id
                    }
                    await manager.broadcast_to_conversation(typing_message, conversation_id, db)
            
            elif data.get("type") == "read":
                # Mark messages as read
                message_id = data.get("message_id")
                if message_id:
                    result = await db.execute(
                        select(Message).where(Message.id == message_id)
                    )
                    message = result.scalar_one_or_none()
                    if message:
                        message.status = MessageStatus.READ
                        await db.commit()
                        
                        # Notify sender
                        read_message = {
                            "type": "read",
                            "message_id": message_id,
                            "conversation_id": message.conversation_id
                        }
                        await manager.send_personal_message(read_message, message.sender_id)
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        
        # Update user presence to offline
        result = await db.execute(
            select(UserPresence).where(UserPresence.user_id == user_id)
        )
        presence = result.scalar_one_or_none()
        if presence:
            presence.is_online = False
            presence.last_seen = datetime.utcnow().isoformat()
            await db.commit()
        
        await manager.broadcast_presence(user_id, False)


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new conversation (direct or group)
    
    - **type**: Conversation type (direct or group)
    - **name**: Name for group conversations
    - **participant_ids**: List of user IDs to include
    """
    # For direct messages, check if conversation already exists
    if conversation_data.type == ConversationType.DIRECT:
        if len(conversation_data.participant_ids) != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Direct conversations must have exactly one other participant"
            )
        
        other_user_id = conversation_data.participant_ids[0]
        
        # Check if conversation already exists between these users
        # Using subquery to find conversations with both users
        from sqlalchemy.orm import selectinload
        from app.models.chat import conversation_participants
        
        result = await db.execute(
            select(Conversation)
            .options(selectinload(Conversation.participants))
            .where(Conversation.type == ConversationType.DIRECT)
        )
        conversations = result.scalars().all()
        
        # Check each conversation to see if it has both users
        for conv in conversations:
            participant_ids = [p.id for p in conv.participants]
            if current_user.id in participant_ids and other_user_id in participant_ids:
                # Return existing conversation
                return ConversationResponse(
                    id=conv.id,
                    type=conv.type,
                    name=conv.name,
                    created_by_id=conv.created_by_id,
                    created_at=conv.created_at,
                    updated_at=conv.updated_at,
                    participant_ids=participant_ids
                )
    
    # Create new conversation
    conversation = Conversation(
        type=conversation_data.type,
        name=conversation_data.name,
        created_by_id=current_user.id
    )
    
    db.add(conversation)
    await db.flush()  # Flush to get the conversation ID
    
    # Add participants using the association table
    participant_ids = list(set([current_user.id] + conversation_data.participant_ids))
    
    from app.models.chat import conversation_participants
    
    for participant_id in participant_ids:
        await db.execute(
            conversation_participants.insert().values(
                conversation_id=conversation.id,
                user_id=participant_id
            )
        )
    
    await db.commit()
    await db.refresh(conversation)
    
    return ConversationResponse(
        id=conversation.id,
        type=conversation.type,
        name=conversation.name,
        created_by_id=conversation.created_by_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        participant_ids=participant_ids
    )


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all conversations for the current user
    """
    from sqlalchemy.orm import selectinload
    from app.models.chat import conversation_participants
    
    # Get all conversations where user is a participant
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.participants))
        .join(conversation_participants)
        .where(conversation_participants.c.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
    )
    conversations = result.scalars().unique().all()
    
    response = []
    for conv in conversations:
        # Get last message
        last_msg_result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conv.id)
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        last_message = last_msg_result.scalar_one_or_none()
        
        response.append(ConversationResponse(
            id=conv.id,
            type=conv.type,
            name=conv.name,
            created_by_id=conv.created_by_id,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            participant_ids=[p.id for p in conv.participants],
            last_message=MessageResponse(
                id=last_message.id,
                conversation_id=last_message.conversation_id,
                sender_id=last_message.sender_id,
                content=last_message.content,
                status=last_message.status,
                created_at=last_message.created_at,
                updated_at=last_message.updated_at
            ) if last_message else None
        ))
    
    return response


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific conversation with messages
    """
    from sqlalchemy.orm import selectinload
    
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.participants))
        .where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Check if user is a participant
    participant_ids = [p.id for p in conversation.participants]
    if current_user.id not in participant_ids:
        raise HTTPException(status_code=403, detail="Not authorized to access this conversation")
    
    # Get messages
    messages_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    messages = messages_result.scalars().all()
    
    return ConversationDetail(
        id=conversation.id,
        type=conversation.type,
        name=conversation.name,
        created_by_id=conversation.created_by_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        participant_ids=participant_ids,
        messages=[
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                sender_id=msg.sender_id,
                content=msg.content,
                status=msg.status,
                created_at=msg.created_at,
                updated_at=msg.updated_at
            ) for msg in messages
        ]
    )


@router.get("/active-users", response_model=ActiveUsersResponse)
async def get_active_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of currently active (online) users
    """
    result = await db.execute(
        select(User, UserPresence)
        .join(UserPresence, User.id == UserPresence.user_id)
        .where(UserPresence.is_online == True)
    )
    
    online_users = []
    for user, presence in result.all():
        online_users.append({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role.value
        })
    
    return ActiveUsersResponse(online_users=online_users)


@router.get("/presence/{user_id}", response_model=UserPresenceResponse)
async def get_user_presence(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get presence information for a specific user
    """
    result = await db.execute(
        select(UserPresence).where(UserPresence.user_id == user_id)
    )
    presence = result.scalar_one_or_none()
    
    if not presence:
        # Return default offline status
        return UserPresenceResponse(
            user_id=user_id,
            is_online=False,
            last_seen=None
        )
    
    return UserPresenceResponse(
        user_id=presence.user_id,
        is_online=presence.is_online,
        last_seen=presence.last_seen
    )
