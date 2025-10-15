const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_BASE_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

const chatService = {
  // Create a new conversation
  createConversation: async (conversationData) => {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/conversations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(conversationData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create conversation');
    }

    return await response.json();
  },

  // Get all conversations for current user
  getConversations: async () => {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/conversations`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch conversations');
    }

    return await response.json();
  },

  // Get a specific conversation with messages
  getConversation: async (conversationId) => {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/conversations/${conversationId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch conversation');
    }

    return await response.json();
  },

  // Get active users
  getActiveUsers: async () => {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/active-users`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch active users');
    }

    return await response.json();
  },

  // Get user presence
  getUserPresence: async (userId) => {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/presence/${userId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch user presence');
    }

    return await response.json();
  },

  // Connect to WebSocket
  connectWebSocket: (onMessage, onError) => {
    const token = localStorage.getItem('token');
    const ws = new WebSocket(`${WS_BASE_URL}/api/v1/chat/ws/${token}`);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (onMessage) {
        onMessage(data);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (onError) {
        onError(error);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return ws;
  },

  // Send a message via WebSocket
  sendMessage: (ws, conversationId, content) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'message',
        conversation_id: conversationId,
        content: content
      }));
    }
  },

  // Send typing indicator
  sendTyping: (ws, conversationId) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'typing',
        conversation_id: conversationId
      }));
    }
  },

  // Mark message as read
  markAsRead: (ws, messageId) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'read',
        message_id: messageId
      }));
    }
  },
};

export default chatService;
