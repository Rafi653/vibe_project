"""
Chat API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime
import json
import logging

from app.db.base import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.chat import Conversation, ConversationParticipant, Message, ConversationType
from app.schemas.chat import (
    ConversationCreate, ConversationResponse, ConversationUpdate,
    ConversationWithMessages, ConversationListItem,
    MessageCreate, MessageResponse, MessageUpdate,
    AddParticipant, ConversationParticipantResponse,
    UserInfo, UserStatus
)
from app.core.websocket import manager
from app.core.security import decode_access_token

logger = logging.getLogger(__name__)
router = APIRouter()


# REST API Endpoints

@router.post("/conversations", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    conversation: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new conversation (direct or group chat)"""
    
    # Validate participants
    participant_ids = list(set(conversation.participant_ids + [current_user.id]))
    
    if len(participant_ids) < 2:
        raise HTTPException(status_code=400, detail="Conversation must have at least 2 participants")
    
    # For direct conversations, check if one already exists
    if conversation.conversation_type == ConversationType.DIRECT and len(participant_ids) == 2:
        # Find existing direct conversation between these users
        existing_query = select(Conversation).join(ConversationParticipant).where(
            and_(
                Conversation.conversation_type == ConversationType.DIRECT,
                ConversationParticipant.user_id.in_(participant_ids)
            )
        ).group_by(Conversation.id).having(
            func.count(ConversationParticipant.id) == 2
        )
        
        result = await db.execute(existing_query)
        existing_conversation = result.scalar_one_or_none()
        
        if existing_conversation:
            # Return existing conversation
            await db.refresh(existing_conversation, ["participants"])
            for participant in existing_conversation.participants:
                await db.refresh(participant, ["user"])
            return existing_conversation
    
    # Create new conversation
    new_conversation = Conversation(
        name=conversation.name,
        conversation_type=conversation.conversation_type,
        is_active=True
    )
    db.add(new_conversation)
    await db.flush()
    
    # Add participants
    for user_id in participant_ids:
        participant = ConversationParticipant(
            conversation_id=new_conversation.id,
            user_id=user_id,
            is_admin=(user_id == current_user.id)  # Creator is admin for group chats
        )
        db.add(participant)
        
        # Add to connection manager
        manager.add_user_to_conversation(user_id, new_conversation.id)
    
    await db.commit()
    await db.refresh(new_conversation, ["participants"])
    
    for participant in new_conversation.participants:
        await db.refresh(participant, ["user"])
    
    return new_conversation


@router.get("/conversations", response_model=List[ConversationListItem])
async def get_conversations(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all conversations for the current user"""
    
    # Get conversations where user is a participant
    query = select(Conversation).join(ConversationParticipant).where(
        and_(
            ConversationParticipant.user_id == current_user.id,
            Conversation.is_active == True
        )
    ).options(
        selectinload(Conversation.participants).selectinload(ConversationParticipant.user)
    ).order_by(desc(Conversation.updated_at))
    
    result = await db.execute(query)
    conversations = result.scalars().all()
    
    # Get last message and unread count for each conversation
    conversation_list = []
    for conversation in conversations:
        # Get last message
        last_message_query = select(Message).where(
            Message.conversation_id == conversation.id
        ).options(
            selectinload(Message.sender)
        ).order_by(desc(Message.created_at)).limit(1)
        
        last_message_result = await db.execute(last_message_query)
        last_message = last_message_result.scalar_one_or_none()
        
        # Get unread count
        unread_query = select(func.count(Message.id)).where(
            and_(
                Message.conversation_id == conversation.id,
                Message.sender_id != current_user.id,
                Message.is_read == False
            )
        )
        unread_result = await db.execute(unread_query)
        unread_count = unread_result.scalar_one()
        
        conversation_item = ConversationListItem(
            **conversation.__dict__,
            participants=[ConversationParticipantResponse(**p.__dict__, user=UserInfo(**p.user.__dict__)) for p in conversation.participants],
            last_message=MessageResponse(**last_message.__dict__, sender=UserInfo(**last_message.sender.__dict__)) if last_message else None,
            unread_count=unread_count
        )
        conversation_list.append(conversation_item)
    
    return conversation_list


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a conversation with its messages"""
    
    # Verify user is a participant
    participant_query = select(ConversationParticipant).where(
        and_(
            ConversationParticipant.conversation_id == conversation_id,
            ConversationParticipant.user_id == current_user.id
        )
    )
    participant_result = await db.execute(participant_query)
    participant = participant_result.scalar_one_or_none()
    
    if not participant:
        raise HTTPException(status_code=403, detail="Not a participant of this conversation")
    
    # Get conversation
    query = select(Conversation).where(
        Conversation.id == conversation_id
    ).options(
        selectinload(Conversation.participants).selectinload(ConversationParticipant.user)
    )
    
    result = await db.execute(query)
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get messages
    messages_query = select(Message).where(
        Message.conversation_id == conversation_id
    ).options(
        selectinload(Message.sender)
    ).order_by(desc(Message.created_at)).limit(limit).offset(offset)
    
    messages_result = await db.execute(messages_query)
    messages = messages_result.scalars().all()
    
    # Get unread count
    unread_query = select(func.count(Message.id)).where(
        and_(
            Message.conversation_id == conversation_id,
            Message.sender_id != current_user.id,
            Message.is_read == False
        )
    )
    unread_result = await db.execute(unread_query)
    unread_count = unread_result.scalar_one()
    
    # Mark messages as read
    update_query = select(Message).where(
        and_(
            Message.conversation_id == conversation_id,
            Message.sender_id != current_user.id,
            Message.is_read == False
        )
    )
    update_result = await db.execute(update_query)
    unread_messages = update_result.scalars().all()
    
    for msg in unread_messages:
        msg.is_read = True
    
    # Update last_read_at
    participant.last_read_at = datetime.utcnow()
    
    await db.commit()
    
    return ConversationWithMessages(
        **conversation.__dict__,
        participants=[ConversationParticipantResponse(**p.__dict__, user=UserInfo(**p.user.__dict__)) for p in conversation.participants],
        messages=[MessageResponse(**m.__dict__, sender=UserInfo(**m.sender.__dict__)) for m in reversed(messages)],
        unread_count=unread_count
    )


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=201)
async def create_message(
    conversation_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new message in a conversation"""
    
    # Verify user is a participant
    participant_query = select(ConversationParticipant).where(
        and_(
            ConversationParticipant.conversation_id == conversation_id,
            ConversationParticipant.user_id == current_user.id
        )
    )
    participant_result = await db.execute(participant_query)
    participant = participant_result.scalar_one_or_none()
    
    if not participant:
        raise HTTPException(status_code=403, detail="Not a participant of this conversation")
    
    # Create message
    new_message = Message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=message.content,
        is_read=False
    )
    db.add(new_message)
    
    # Update conversation timestamp
    conversation_query = select(Conversation).where(Conversation.id == conversation_id)
    conversation_result = await db.execute(conversation_query)
    conversation = conversation_result.scalar_one()
    conversation.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(new_message, ["sender"])
    
    # Broadcast message to conversation participants via WebSocket
    message_data = {
        "type": "message",
        "data": {
            "id": new_message.id,
            "conversation_id": new_message.conversation_id,
            "sender_id": new_message.sender_id,
            "sender": {
                "id": current_user.id,
                "full_name": current_user.full_name,
                "email": current_user.email,
                "role": current_user.role.value
            },
            "content": new_message.content,
            "is_read": new_message.is_read,
            "is_edited": new_message.is_edited,
            "created_at": new_message.created_at.isoformat(),
            "updated_at": new_message.updated_at.isoformat()
        }
    }
    await manager.send_to_conversation(message_data, conversation_id, exclude_user_id=current_user.id)
    
    return MessageResponse(**new_message.__dict__, sender=UserInfo(**current_user.__dict__))


@router.patch("/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: int,
    message_update: MessageUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a message (only by sender)"""
    
    # Get message
    query = select(Message).where(Message.id == message_id).options(selectinload(Message.sender))
    result = await db.execute(query)
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only edit your own messages")
    
    # Update message
    message.content = message_update.content
    message.is_edited = True
    message.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(message)
    
    return MessageResponse(**message.__dict__, sender=UserInfo(**message.sender.__dict__))


@router.delete("/messages/{message_id}", status_code=204)
async def delete_message(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a message (only by sender)"""
    
    # Get message
    query = select(Message).where(Message.id == message_id)
    result = await db.execute(query)
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only delete your own messages")
    
    await db.delete(message)
    await db.commit()


@router.post("/conversations/{conversation_id}/participants", response_model=ConversationParticipantResponse, status_code=201)
async def add_participant(
    conversation_id: int,
    participant_data: AddParticipant,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Add a participant to a group conversation"""
    
    # Get conversation
    conversation_query = select(Conversation).where(Conversation.id == conversation_id)
    conversation_result = await db.execute(conversation_query)
    conversation = conversation_result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if conversation.conversation_type != ConversationType.GROUP:
        raise HTTPException(status_code=400, detail="Can only add participants to group conversations")
    
    # Verify current user is admin
    admin_query = select(ConversationParticipant).where(
        and_(
            ConversationParticipant.conversation_id == conversation_id,
            ConversationParticipant.user_id == current_user.id,
            ConversationParticipant.is_admin == True
        )
    )
    admin_result = await db.execute(admin_query)
    is_admin = admin_result.scalar_one_or_none()
    
    if not is_admin:
        raise HTTPException(status_code=403, detail="Only group admins can add participants")
    
    # Check if user is already a participant
    existing_query = select(ConversationParticipant).where(
        and_(
            ConversationParticipant.conversation_id == conversation_id,
            ConversationParticipant.user_id == participant_data.user_id
        )
    )
    existing_result = await db.execute(existing_query)
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="User is already a participant")
    
    # Add participant
    new_participant = ConversationParticipant(
        conversation_id=conversation_id,
        user_id=participant_data.user_id,
        is_admin=participant_data.is_admin
    )
    db.add(new_participant)
    await db.commit()
    await db.refresh(new_participant, ["user"])
    
    # Add to connection manager
    manager.add_user_to_conversation(participant_data.user_id, conversation_id)
    
    return ConversationParticipantResponse(**new_participant.__dict__, user=UserInfo(**new_participant.user.__dict__))


@router.get("/users/active", response_model=List[UserStatus])
async def get_active_users(
    current_user: User = Depends(get_current_active_user)
):
    """Get list of currently active/online users"""
    
    online_user_ids = manager.get_online_users()
    
    user_statuses = []
    for user_id in online_user_ids:
        user_statuses.append(UserStatus(
            user_id=user_id,
            is_online=True,
            last_seen=manager.user_activity.get(user_id)
        ))
    
    return user_statuses


# WebSocket endpoint for real-time chat
@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """WebSocket endpoint for real-time chat"""
    
    # Authenticate user from token
    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")
        
        if user_id is None:
            await websocket.close(code=1008, reason="Invalid authentication token")
            return
        
        # Verify user exists
        user_query = select(User).where(User.id == user_id)
        user_result = await db.execute(user_query)
        user = user_result.scalar_one_or_none()
        
        if not user or not user.is_active:
            await websocket.close(code=1008, reason="User not found or inactive")
            return
        
    except Exception as e:
        logger.error(f"WebSocket authentication error: {e}")
        await websocket.close(code=1008, reason="Authentication failed")
        return
    
    # Connect user
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_type = message_data.get("type")
            
            if message_type == "typing":
                # Broadcast typing indicator
                conversation_id = message_data.get("conversation_id")
                typing_data = {
                    "type": "typing",
                    "data": {
                        "conversation_id": conversation_id,
                        "user_id": user_id,
                        "is_typing": message_data.get("is_typing", False)
                    }
                }
                await manager.send_to_conversation(typing_data, conversation_id, exclude_user_id=user_id)
            
            elif message_type == "read_receipt":
                # Handle read receipt
                conversation_id = message_data.get("conversation_id")
                message_id = message_data.get("message_id")
                
                # Update message as read in database
                msg_query = select(Message).where(
                    and_(
                        Message.id == message_id,
                        Message.conversation_id == conversation_id
                    )
                )
                msg_result = await db.execute(msg_query)
                msg = msg_result.scalar_one_or_none()
                
                if msg and msg.sender_id != user_id:
                    msg.is_read = True
                    await db.commit()
                    
                    # Broadcast read receipt
                    receipt_data = {
                        "type": "read_receipt",
                        "data": {
                            "conversation_id": conversation_id,
                            "message_id": message_id,
                            "user_id": user_id
                        }
                    }
                    await manager.send_to_conversation(receipt_data, conversation_id)
            
            # Update user activity
            manager.user_activity[user_id] = datetime.utcnow()
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast_user_status(user_id, False)
        logger.info(f"User {user_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(websocket, user_id)
        await manager.broadcast_user_status(user_id, False)
