/**
 * Chat Service
 * Handles chat-related API calls
 */

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Get authentication token
 */
const getAuthToken = () => {
    const token = localStorage.getItem('token');
    return token;
};

/**
 * Get all conversations for the current user
 */
export const getConversations = async () => {
    const token = getAuthToken();
    const response = await fetch(`${API_URL}/api/v1/chat/conversations`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        throw new Error('Failed to fetch conversations');
    }

    return response.json();
};

/**
 * Get a specific conversation with messages
 */
export const getConversation = async (conversationId, limit = 50, offset = 0) => {
    const token = getAuthToken();
    const response = await fetch(
        `${API_URL}/api/v1/chat/conversations/${conversationId}?limit=${limit}&offset=${offset}`,
        {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        }
    );

    if (!response.ok) {
        throw new Error('Failed to fetch conversation');
    }

    return response.json();
};

/**
 * Create a new conversation
 */
export const createConversation = async (conversationData) => {
    const token = getAuthToken();
    const response = await fetch(`${API_URL}/api/v1/chat/conversations`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(conversationData),
    });

    if (!response.ok) {
        throw new Error('Failed to create conversation');
    }

    return response.json();
};

/**
 * Send a message in a conversation
 */
export const sendMessage = async (conversationId, content) => {
    const token = getAuthToken();
    const response = await fetch(
        `${API_URL}/api/v1/chat/conversations/${conversationId}/messages`,
        {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ conversation_id: conversationId, content }),
        }
    );

    if (!response.ok) {
        throw new Error('Failed to send message');
    }

    return response.json();
};

/**
 * Update a message
 */
export const updateMessage = async (messageId, content) => {
    const token = getAuthToken();
    const response = await fetch(`${API_URL}/api/v1/chat/messages/${messageId}`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content }),
    });

    if (!response.ok) {
        throw new Error('Failed to update message');
    }

    return response.json();
};

/**
 * Delete a message
 */
export const deleteMessage = async (messageId) => {
    const token = getAuthToken();
    const response = await fetch(`${API_URL}/api/v1/chat/messages/${messageId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        throw new Error('Failed to delete message');
    }
};

/**
 * Add participant to a group conversation
 */
export const addParticipant = async (conversationId, userId, isAdmin = false) => {
    const token = getAuthToken();
    const response = await fetch(
        `${API_URL}/api/v1/chat/conversations/${conversationId}/participants`,
        {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId, is_admin: isAdmin }),
        }
    );

    if (!response.ok) {
        throw new Error('Failed to add participant');
    }

    return response.json();
};

/**
 * Get list of active users
 */
export const getActiveUsers = async () => {
    const token = getAuthToken();
    const response = await fetch(`${API_URL}/api/v1/chat/users/active`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        throw new Error('Failed to fetch active users');
    }

    return response.json();
};

/**
 * Get WebSocket URL for real-time chat
 */
export const getWebSocketUrl = () => {
    const baseUrl = API_URL.replace('http://', 'ws://').replace('https://', 'wss://');
    const token = getAuthToken();
    return `${baseUrl}/api/v1/chat/ws?token=${token}`;
};
