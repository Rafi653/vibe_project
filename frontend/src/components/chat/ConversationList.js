/**
 * ConversationList Component
 * Displays list of conversations
 */

import React from 'react';
import './Chat.css';

const ConversationList = ({ conversations, onSelectConversation, activeConversationId, activeUsers }) => {
    const getConversationName = (conversation, currentUserId) => {
        if (conversation.conversation_type === 'group') {
            return conversation.name || 'Group Chat';
        }
        
        // For direct conversations, show the other participant's name
        const otherParticipant = conversation.participants.find(
            p => p.user_id !== currentUserId
        );
        return otherParticipant ? otherParticipant.user.full_name : 'Unknown User';
    };

    const formatLastMessageTime = (timestamp) => {
        if (!timestamp) return '';
        
        const date = new Date(timestamp);
        const now = new Date();
        const diffInMs = now - date;
        const diffInHours = diffInMs / (1000 * 60 * 60);
        
        if (diffInHours < 24) {
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        } else {
            return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
        }
    };

    const isUserOnline = (conversation, currentUserId) => {
        if (conversation.conversation_type === 'direct') {
            const otherParticipant = conversation.participants.find(
                p => p.user_id !== currentUserId
            );
            return otherParticipant ? activeUsers.has(otherParticipant.user_id) : false;
        }
        return false;
    };

    const currentUserId = JSON.parse(localStorage.getItem('user'))?.id;

    return (
        <div className="conversation-list">
            <h3>Conversations</h3>
            {conversations.length === 0 ? (
                <p className="no-conversations">No conversations yet</p>
            ) : (
                <div className="conversations">
                    {conversations.map((conversation) => (
                        <div
                            key={conversation.id}
                            className={`conversation-item ${activeConversationId === conversation.id ? 'active' : ''}`}
                            onClick={() => onSelectConversation(conversation.id)}
                        >
                            <div className="conversation-avatar">
                                {getConversationName(conversation, currentUserId)[0]}
                                {isUserOnline(conversation, currentUserId) && (
                                    <span className="online-indicator"></span>
                                )}
                            </div>
                            <div className="conversation-info">
                                <div className="conversation-header">
                                    <span className="conversation-name">
                                        {getConversationName(conversation, currentUserId)}
                                    </span>
                                    {conversation.last_message && (
                                        <span className="conversation-time">
                                            {formatLastMessageTime(conversation.last_message.created_at)}
                                        </span>
                                    )}
                                </div>
                                <div className="conversation-preview">
                                    {conversation.last_message ? (
                                        <>
                                            <span className="last-message-content">
                                                {conversation.last_message.content.substring(0, 40)}
                                                {conversation.last_message.content.length > 40 ? '...' : ''}
                                            </span>
                                            {conversation.unread_count > 0 && (
                                                <span className="unread-badge">{conversation.unread_count}</span>
                                            )}
                                        </>
                                    ) : (
                                        <span className="no-messages">No messages yet</span>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ConversationList;
