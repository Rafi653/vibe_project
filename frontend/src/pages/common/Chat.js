/**
 * Chat Page Component
 * Main chat interface accessible to all authenticated users
 */

import React, { useState, useEffect } from 'react';
import ConversationList from '../../components/chat/ConversationList';
import ChatWindow from '../../components/chat/ChatWindow';
import NewConversationModal from '../../components/chat/NewConversationModal';
import { useChat } from '../../context/ChatContext';
import {
    getConversations,
    getConversation,
    createConversation,
} from '../../services/chatService';
import '../../components/chat/Chat.css';

const Chat = () => {
    const [conversations, setConversations] = useState([]);
    const [activeConversation, setActiveConversation] = useState(null);
    const [showNewConversationModal, setShowNewConversationModal] = useState(false);
    const [allUsers, setAllUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const { activeUsers, isConnected } = useChat();

    useEffect(() => {
        loadConversations();
        loadUsers();
    }, []);

    const loadConversations = async () => {
        try {
            setLoading(true);
            const data = await getConversations();
            setConversations(data);
        } catch (error) {
            console.error('Error loading conversations:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadUsers = async () => {
        try {
            // Fetch all users from the API
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:8000/api/v1/users', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            
            if (response.ok) {
                const data = await response.json();
                setAllUsers(data);
            }
        } catch (error) {
            console.error('Error loading users:', error);
        }
    };

    const handleSelectConversation = async (conversationId) => {
        try {
            const conversation = await getConversation(conversationId);
            setActiveConversation(conversation);
        } catch (error) {
            console.error('Error loading conversation:', error);
            alert('Failed to load conversation');
        }
    };

    const handleCreateConversation = async (conversationData) => {
        try {
            const newConversation = await createConversation(conversationData);
            setConversations(prev => [newConversation, ...prev]);
            setShowNewConversationModal(false);
            
            // Load and select the new conversation
            const fullConversation = await getConversation(newConversation.id);
            setActiveConversation(fullConversation);
        } catch (error) {
            console.error('Error creating conversation:', error);
            alert('Failed to create conversation');
        }
    };

    return (
        <div className="page-container">
            <h1>Chat</h1>
            
            {!isConnected && (
                <div className="connection-status">
                    <span style={{ color: 'orange' }}>⚠ Connecting to chat server...</span>
                </div>
            )}
            
            <div className="chat-container">
                <div className="conversation-list">
                    <div style={{ padding: '20px', borderBottom: '1px solid #e0e0e0' }}>
                        <button
                            onClick={() => setShowNewConversationModal(true)}
                            className="btn-new-conversation"
                        >
                            + New Conversation
                        </button>
                    </div>
                    
                    {loading ? (
                        <div style={{ padding: '20px', textAlign: 'center' }}>
                            Loading conversations...
                        </div>
                    ) : (
                        <ConversationList
                            conversations={conversations}
                            onSelectConversation={handleSelectConversation}
                            activeConversationId={activeConversation?.id}
                            activeUsers={activeUsers}
                        />
                    )}
                </div>
                
                <ChatWindow
                    conversation={activeConversation}
                    onClose={() => setActiveConversation(null)}
                />
            </div>
            
            {showNewConversationModal && (
                <NewConversationModal
                    onClose={() => setShowNewConversationModal(false)}
                    onCreate={handleCreateConversation}
                    users={allUsers}
                />
            )}
        </div>
    );
};

export default Chat;
