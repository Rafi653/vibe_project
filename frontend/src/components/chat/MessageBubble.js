/**
 * MessageBubble Component
 * Displays a single chat message
 */

import React from 'react';
import './Chat.css';

const MessageBubble = ({ message, isOwnMessage, onEdit, onDelete }) => {
    const formatTime = (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    return (
        <div className={`message-bubble ${isOwnMessage ? 'own-message' : 'other-message'}`}>
            <div className="message-header">
                <span className="message-sender">{message.sender.full_name}</span>
                <span className="message-time">{formatTime(message.created_at)}</span>
            </div>
            <div className="message-content">
                {message.content}
                {message.is_edited && <span className="edited-indicator"> (edited)</span>}
            </div>
            {isOwnMessage && (
                <div className="message-actions">
                    <button onClick={() => onEdit(message)} className="btn-edit">Edit</button>
                    <button onClick={() => onDelete(message.id)} className="btn-delete">Delete</button>
                </div>
            )}
        </div>
    );
};

export default MessageBubble;
