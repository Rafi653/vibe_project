/**
 * Chat service for handling API calls and WebSocket connections
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_BASE_URL = API_BASE_URL.replace('http', 'ws').replace('https', 'wss');

class ChatService {
  constructor() {
    this.ws = null;
    this.messageHandlers = [];
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  // WebSocket connection
  connect(userId, onMessage, onPresence) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      return;
    }

    this.ws = new WebSocket(`${WS_BASE_URL}/api/v1/chat/ws/${userId}`);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'presence' && onPresence) {
        onPresence(data);
      } else if (data.type === 'message' && onMessage) {
        onMessage(data);
      } else if (data.type === 'typing') {
        // Handle typing indicator
        this.messageHandlers.forEach(handler => handler(data));
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      
      // Attempt to reconnect
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        setTimeout(() => {
          console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
          this.connect(userId, onMessage, onPresence);
        }, 2000 * this.reconnectAttempts);
      }
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  sendMessage(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  addMessageHandler(handler) {
    this.messageHandlers.push(handler);
  }

  removeMessageHandler(handler) {
    this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
  }

  // REST API calls
  async createChatRoom(participantIds, name = null, type = 'direct') {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/rooms`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        participant_ids: participantIds,
        name,
        type
      })
    });

    if (!response.ok) {
      throw new Error('Failed to create chat room');
    }

    return response.json();
  }

  async getChatRooms() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/rooms`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch chat rooms');
    }

    return response.json();
  }

  async getChatRoom(roomId) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/rooms/${roomId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch chat room');
    }

    return response.json();
  }

  async sendChatMessage(chatRoomId, content, messageType = 'text') {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        chat_room_id: chatRoomId,
        content,
        message_type: messageType
      })
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    return response.json();
  }

  async updateMessage(messageId, content) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/messages/${messageId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ content })
    });

    if (!response.ok) {
      throw new Error('Failed to update message');
    }

    return response.json();
  }

  async deleteMessage(messageId) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/messages/${messageId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to delete message');
    }

    return response.json();
  }

  async getOnlineUsers() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/presence`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch online users');
    }

    return response.json();
  }

  async addParticipants(roomId, userIds) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/rooms/${roomId}/participants`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ user_ids: userIds })
    });

    if (!response.ok) {
      throw new Error('Failed to add participants');
    }

    return response.json();
  }

  async markAsRead(chatRoomId) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/mark-read`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ chat_room_id: chatRoomId })
    });

    if (!response.ok) {
      throw new Error('Failed to mark as read');
    }

    return response.json();
  }
}

export default new ChatService();
