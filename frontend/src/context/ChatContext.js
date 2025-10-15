/**
 * Chat Context
 * Manages WebSocket connection and chat state
 */

import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react';
import { getWebSocketUrl } from '../services/chatService';

const ChatContext = createContext();

export const useChat = () => {
    const context = useContext(ChatContext);
    if (!context) {
        throw new Error('useChat must be used within ChatProvider');
    }
    return context;
};

export const ChatProvider = ({ children }) => {
    const [ws, setWs] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const [messages, setMessages] = useState([]);
    const [activeUsers, setActiveUsers] = useState(new Set());
    const [typingUsers, setTypingUsers] = useState({});
    const [unreadCounts, setUnreadCounts] = useState({});
    const reconnectTimeout = useRef();

    // Handle incoming WebSocket messages
    const handleWebSocketMessage = useCallback((data) => {
        const { type, data: payload } = data;

        switch (type) {
            case 'message':
                // New message received
                setMessages(prev => [...prev, payload]);
                
                // Update unread count if not in active conversation
                const currentConversationId = localStorage.getItem('activeConversationId');
                if (payload.conversation_id !== parseInt(currentConversationId)) {
                    setUnreadCounts(prev => ({
                        ...prev,
                        [payload.conversation_id]: (prev[payload.conversation_id] || 0) + 1
                    }));
                }
                break;

            case 'typing':
                // Typing indicator
                const { conversation_id, user_id, is_typing } = payload;
                setTypingUsers(prev => {
                    const conversationTyping = { ...prev[conversation_id] };
                    if (is_typing) {
                        conversationTyping[user_id] = true;
                    } else {
                        delete conversationTyping[user_id];
                    }
                    return { ...prev, [conversation_id]: conversationTyping };
                });
                break;

            case 'read_receipt':
                // Message read receipt
                setMessages(prev => prev.map(msg =>
                    msg.id === payload.message_id
                        ? { ...msg, is_read: true }
                        : msg
                ));
                break;

            case 'user_status':
                // User online/offline status
                const { user_id: userId, is_online } = payload;
                setActiveUsers(prev => {
                    const newSet = new Set(prev);
                    if (is_online) {
                        newSet.add(userId);
                    } else {
                        newSet.delete(userId);
                    }
                    return newSet;
                });
                break;

            case 'error':
                console.error('WebSocket error:', payload);
                break;

            default:
                console.log('Unknown message type:', type);
        }
    }, []);

    // Connect to WebSocket
    const connect = useCallback(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            console.log('No token found, skipping WebSocket connection');
            return;
        }

        try {
            const wsUrl = getWebSocketUrl();
            const websocket = new WebSocket(wsUrl);

            websocket.onopen = () => {
                console.log('WebSocket connected');
                setIsConnected(true);
            };

            websocket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    handleWebSocketMessage(data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };

            websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            websocket.onclose = () => {
                console.log('WebSocket disconnected');
                setIsConnected(false);
                
                // Only set timeout if not already set
                if (!reconnectTimeout.current) {
                    reconnectTimeout.current = setTimeout(() => {
                        console.log('Attempting to reconnect...');
                        connect();
                        reconnectTimeout.current = null;
                    }, 3000);
                }
            };
            //     // Attempt to reconnect after 3 seconds
            //     setTimeout(() => {
            //         console.log('Attempting to reconnect...');
            //         connect();
            //     }, 3000);
            // };

            setWs(websocket);
        } catch (error) {
            console.error('Error connecting to WebSocket:', error);
        }
    }, [handleWebSocketMessage]);

    // Disconnect from WebSocket
    const disconnect = useCallback(() => {
        if (ws) {
            ws.close();
            setWs(null);
            setIsConnected(false);
        }
    }, [ws]);

    // Send typing indicator
    const sendTypingIndicator = useCallback((conversationId, isTyping) => {
        if (ws && isConnected) {
            ws.send(JSON.stringify({
                type: 'typing',
                conversation_id: conversationId,
                is_typing: isTyping
            }));
        }
    }, [ws, isConnected]);

    // Send read receipt
    const sendReadReceipt = useCallback((conversationId, messageId) => {
        if (ws && isConnected) {
            ws.send(JSON.stringify({
                type: 'read_receipt',
                conversation_id: conversationId,
                message_id: messageId
            }));
        }
    }, [ws, isConnected]);

    // Clear unread count for a conversation
    const clearUnreadCount = useCallback((conversationId) => {
        setUnreadCounts(prev => {
            const updated = { ...prev };
            delete updated[conversationId];
            return updated;
        });
    }, []);

    // Get typing users for a conversation
    const getTypingUsers = useCallback((conversationId) => {
        const typingInConversation = typingUsers[conversationId] || {};
        return Object.keys(typingInConversation).map(id => parseInt(id));
    }, [typingUsers]);

    // Connect on mount, disconnect on unmount
    useEffect(() => {
        connect();
        return () => {
            disconnect();
            if (reconnectTimeout.current) {
                clearTimeout(reconnectTimeout.current);
            }
        };
        // return () => disconnect();
    }, [connect, disconnect]);

    const value = {
        ws,
        isConnected,
        messages,
        activeUsers,
        unreadCounts,
        connect,
        disconnect,
        sendTypingIndicator,
        sendReadReceipt,
        clearUnreadCount,
        getTypingUsers,
    };

    return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};
