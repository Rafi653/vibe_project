/**
 * ChatWindow Component
 * Main chat interface for sending and receiving messages
 */

import React, { useState, useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import { useChat } from '../../context/ChatContext';
import { sendMessage, updateMessage, deleteMessage } from '../../services/chatService';
import './Chat.css';

const ChatWindow = ({ conversation, onClose }) => {
    const [messageText, setMessageText] = useState('');
    const [messages, setMessages] = useState([]);
    const [isTyping, setIsTyping] = useState(false);
    const [editingMessage, setEditingMessage] = useState(null);
    const messagesEndRef = useRef(null);
    const typingTimeoutRef = useRef(null);
    const { sendTypingIndicator, sendReadReceipt, getTypingUsers, clearUnreadCount } = useChat();

    const currentUserId = JSON.parse(localStorage.getItem('user'))?.id;

    useEffect(() => {
        if (conversation) {
            setMessages(conversation.messages || []);
            clearUnreadCount(conversation.id);
            localStorage.setItem('activeConversationId', conversation.id);
            
            // Send read receipts for unread messages
            conversation.messages?.forEach(msg => {
                if (!msg.is_read && msg.sender_id !== currentUserId) {
                    sendReadReceipt(conversation.id, msg.id);
                }
            });
        }
        
        return () => {
            localStorage.removeItem('activeConversationId');
        };
    }, [conversation, clearUnreadCount, currentUserId, sendReadReceipt]);

    useEffect(() => {
        // Scroll to bottom when new messages arrive
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        
        if (!messageText.trim()) return;

        try {
            if (editingMessage) {
                // Update existing message
                const updated = await updateMessage(editingMessage.id, messageText);
                setMessages(prev => prev.map(msg => msg.id === updated.id ? updated : msg));
                setEditingMessage(null);
            } else {
                // Send new message
                const newMessage = await sendMessage(conversation.id, messageText);
                setMessages(prev => [...prev, newMessage]);
            }
            
            setMessageText('');
            setIsTyping(false);
            sendTypingIndicator(conversation.id, false);
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Failed to send message');
        }
    };

    const handleTyping = (e) => {
        setMessageText(e.target.value);
        
        // Send typing indicator
        if (!isTyping) {
            setIsTyping(true);
            sendTypingIndicator(conversation.id, true);
        }

        // Clear previous timeout
        if (typingTimeoutRef.current) {
            clearTimeout(typingTimeoutRef.current);
        }

        // Stop typing indicator after 2 seconds of inactivity
        typingTimeoutRef.current = setTimeout(() => {
            setIsTyping(false);
            sendTypingIndicator(conversation.id, false);
        }, 2000);
    };

    const handleEdit = (message) => {
        setEditingMessage(message);
        setMessageText(message.content);
    };

    const handleDelete = async (messageId) => {
        if (!window.confirm('Are you sure you want to delete this message?')) return;

        try {
            await deleteMessage(messageId);
            setMessages(prev => prev.filter(msg => msg.id !== messageId));
        } catch (error) {
            console.error('Error deleting message:', error);
            alert('Failed to delete message');
        }
    };

    const cancelEdit = () => {
        setEditingMessage(null);
        setMessageText('');
    };

    const getConversationName = () => {
        if (!conversation) return '';
        
        if (conversation.conversation_type === 'group') {
            return conversation.name || 'Group Chat';
        }
        
        const otherParticipant = conversation.participants.find(
            p => p.user_id !== currentUserId
        );
        return otherParticipant ? otherParticipant.user.full_name : 'Unknown User';
    };

    const typingUserIds = getTypingUsers(conversation?.id);
    const typingParticipants = conversation?.participants.filter(
        p => typingUserIds.includes(p.user_id) && p.user_id !== currentUserId
    ) || [];

    if (!conversation) {
        return (
            <div className="chat-window">
                <div className="no-conversation-selected">
                    <p>Select a conversation to start chatting</p>
                </div>
            </div>
        );
    }

    return (
        <div className="chat-window">
            <div className="chat-header">
                <h3>{getConversationName()}</h3>
                <button onClick={onClose} className="btn-close">×</button>
            </div>
            
            <div className="messages-container">
                {messages.map((message) => (
                    <MessageBubble
                        key={message.id}
                        message={message}
                        isOwnMessage={message.sender_id === currentUserId}
                        onEdit={handleEdit}
                        onDelete={handleDelete}
                    />
                ))}
                
                {typingParticipants.length > 0 && (
                    <div className="typing-indicator">
                        <span>{typingParticipants.map(p => p.user.full_name).join(', ')} is typing...</span>
                    </div>
                )}
                
                <div ref={messagesEndRef} />
            </div>
            
            <form onSubmit={handleSendMessage} className="message-input-form">
                {editingMessage && (
                    <div className="editing-banner">
                        <span>Editing message</span>
                        <button type="button" onClick={cancelEdit} className="btn-cancel-edit">Cancel</button>
                    </div>
                )}
                <div className="message-input-container">
                    <textarea
                        value={messageText}
                        onChange={handleTyping}
                        placeholder="Type a message..."
                        className="message-input"
                        rows="3"
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSendMessage(e);
                            }
                        }}
                    />
                    <button type="submit" className="btn-send" disabled={!messageText.trim()}>
                        Send
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ChatWindow;
