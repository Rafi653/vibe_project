"""
WebSocket connection manager for real-time chat
"""

from typing import Dict, Set, Optional
from fastapi import WebSocket
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time chat"""
    
    def __init__(self):
        # Map of user_id to set of WebSocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # Map of conversation_id to set of user_ids
        self.conversation_users: Dict[int, Set[int]] = {}
        # Map of user_id to last activity timestamp
        self.user_activity: Dict[int, datetime] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a user's WebSocket"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        self.user_activity[user_id] = datetime.utcnow()
        
        logger.info(f"User {user_id} connected. Total connections: {len(self.active_connections[user_id])}")
        
        # Broadcast user online status
        await self.broadcast_user_status(user_id, True)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """Disconnect a user's WebSocket"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            
            # Remove user from active connections if no more connections
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                logger.info(f"User {user_id} fully disconnected")
            else:
                logger.info(f"User {user_id} connection removed. Remaining: {len(self.active_connections[user_id])}")
    
    def is_user_online(self, user_id: int) -> bool:
        """Check if a user is currently online"""
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0
    
    def get_online_users(self) -> Set[int]:
        """Get set of all online user IDs"""
        return set(self.active_connections.keys())
    
    async def send_personal_message(self, message: dict, user_id: int):
        """Send a message to a specific user (all their connections)"""
        if user_id in self.active_connections:
            message_text = json.dumps(message)
            dead_connections = set()
            
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message_text)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")
                    dead_connections.add(connection)
            
            # Clean up dead connections
            for connection in dead_connections:
                self.active_connections[user_id].discard(connection)
    
    async def send_to_conversation(self, message: dict, conversation_id: int, exclude_user_id: Optional[int] = None):
        """Send a message to all users in a conversation"""
        if conversation_id in self.conversation_users:
            for user_id in self.conversation_users[conversation_id]:
                if exclude_user_id is None or user_id != exclude_user_id:
                    await self.send_personal_message(message, user_id)
    
    async def broadcast_user_status(self, user_id: int, is_online: bool):
        """Broadcast user online/offline status to all connected users"""
        status_message = {
            "type": "user_status",
            "data": {
                "user_id": user_id,
                "is_online": is_online,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        # Send to all online users
        for online_user_id in list(self.active_connections.keys()):
            if online_user_id != user_id:
                await self.send_personal_message(status_message, online_user_id)
    
    def add_user_to_conversation(self, user_id: int, conversation_id: int):
        """Add a user to a conversation's user list"""
        if conversation_id not in self.conversation_users:
            self.conversation_users[conversation_id] = set()
        self.conversation_users[conversation_id].add(user_id)
    
    def remove_user_from_conversation(self, user_id: int, conversation_id: int):
        """Remove a user from a conversation's user list"""
        if conversation_id in self.conversation_users:
            self.conversation_users[conversation_id].discard(user_id)
            
            # Clean up empty conversation
            if not self.conversation_users[conversation_id]:
                del self.conversation_users[conversation_id]
    
    def get_conversation_online_users(self, conversation_id: int) -> Set[int]:
        """Get set of online users in a conversation"""
        if conversation_id not in self.conversation_users:
            return set()
        
        conversation_users = self.conversation_users[conversation_id]
        online_users = self.get_online_users()
        return conversation_users.intersection(online_users)


# Global connection manager instance
manager = ConnectionManager()
