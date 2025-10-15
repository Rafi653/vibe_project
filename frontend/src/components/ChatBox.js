import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import chatService from '../services/chatService';
import './ChatBox.css';

function ChatBox() {
  const { user, isAuthenticated } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [view, setView] = useState('conversations'); // 'conversations', 'chat', 'new', 'users'
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [activeUsers, setActiveUsers] = useState([]);
  const [ws, setWs] = useState(null);
  const [typing, setTyping] = useState({});
  const messagesEndRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  // Initialize WebSocket connection
  useEffect(() => {
    if (isAuthenticated && isOpen) {
      const websocket = chatService.connectWebSocket(
        (data) => handleWebSocketMessage(data),
        (error) => console.error('WebSocket error:', error)
      );
      setWs(websocket);

      return () => {
        if (websocket) {
          websocket.close();
        }
      };
    }
  }, [isAuthenticated, isOpen]);

  // Load conversations when opened
  useEffect(() => {
    if (isOpen && isAuthenticated) {
      loadConversations();
      loadActiveUsers();
    }
  }, [isOpen, isAuthenticated]);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleWebSocketMessage = (data) => {
    if (data.type === 'message') {
      // Add new message to current conversation
      if (activeConversation && data.message.conversation_id === activeConversation.id) {
        setMessages(prev => [...prev, data.message]);
      }
      // Update conversation list
      loadConversations();
    } else if (data.type === 'typing') {
      // Show typing indicator
      if (activeConversation && data.conversation_id === activeConversation.id) {
        setTyping(prev => ({ ...prev, [data.user_id]: true }));
        // Clear typing after 3 seconds
        if (typingTimeoutRef.current) {
          clearTimeout(typingTimeoutRef.current);
        }
        typingTimeoutRef.current = setTimeout(() => {
          setTyping(prev => ({ ...prev, [data.user_id]: false }));
        }, 3000);
      }
    } else if (data.type === 'presence') {
      // Update user presence
      loadActiveUsers();
    }
  };

  const loadConversations = async () => {
    try {
      const data = await chatService.getConversations();
      setConversations(data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  };

  const loadActiveUsers = async () => {
    try {
      const data = await chatService.getActiveUsers();
      setActiveUsers(data.online_users);
    } catch (error) {
      console.error('Failed to load active users:', error);
    }
  };

  const openConversation = async (conversation) => {
    try {
      const data = await chatService.getConversation(conversation.id);
      setActiveConversation(data);
      setMessages(data.messages);
      setView('chat');
    } catch (error) {
      console.error('Failed to load conversation:', error);
    }
  };

  const startDirectChat = async (userId) => {
    try {
      const conversationData = {
        type: 'direct',
        participant_ids: [userId]
      };
      const conversation = await chatService.createConversation(conversationData);
      openConversation(conversation);
    } catch (error) {
      console.error('Failed to create conversation:', error);
    }
  };

  const sendMessage = () => {
    if (newMessage.trim() && ws && activeConversation) {
      chatService.sendMessage(ws, activeConversation.id, newMessage);
      setNewMessage('');
    }
  };

  const handleTyping = () => {
    if (ws && activeConversation) {
      chatService.sendTyping(ws, activeConversation.id);
    }
  };

  const getConversationName = (conversation) => {
    if (conversation.type === 'group') {
      return conversation.name || 'Group Chat';
    }
    // For direct messages, show the other participant's name
    const otherParticipant = conversation.participant_ids.find(id => id !== user.id);
    // We'd need to fetch user details, for now just show "Direct Message"
    return 'Direct Message';
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <>
      <button 
        className="chat-trigger"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Open Chat"
      >
        💬 Chat
      </button>

      {isOpen && (
        <div className="chat-container">
          <div className="chat-window">
            {/* Header */}
            <div className="chat-header">
              {view === 'chat' && (
                <button 
                  className="chat-back-button"
                  onClick={() => {
                    setView('conversations');
                    setActiveConversation(null);
                  }}
                >
                  ← Back
                </button>
              )}
              <h3>
                {view === 'conversations' && 'Messages'}
                {view === 'chat' && getConversationName(activeConversation)}
                {view === 'users' && 'Active Users'}
              </h3>
              <button 
                className="chat-close"
                onClick={() => setIsOpen(false)}
                aria-label="Close Chat"
              >
                ×
              </button>
            </div>

            {/* Navigation Tabs */}
            {view !== 'chat' && (
              <div className="chat-tabs">
                <button 
                  className={`chat-tab ${view === 'conversations' ? 'active' : ''}`}
                  onClick={() => setView('conversations')}
                >
                  Conversations
                </button>
                <button 
                  className={`chat-tab ${view === 'users' ? 'active' : ''}`}
                  onClick={() => {
                    setView('users');
                    loadActiveUsers();
                  }}
                >
                  Active Users ({activeUsers.length})
                </button>
              </div>
            )}

            {/* Content */}
            <div className="chat-content">
              {/* Conversations List */}
              {view === 'conversations' && (
                <div className="conversations-list">
                  {conversations.length === 0 ? (
                    <div className="empty-state">
                      <p>No conversations yet</p>
                      <p>Start chatting with active users!</p>
                    </div>
                  ) : (
                    conversations.map(conv => (
                      <div 
                        key={conv.id}
                        className="conversation-item"
                        onClick={() => openConversation(conv)}
                      >
                        <div className="conversation-info">
                          <strong>{getConversationName(conv)}</strong>
                          {conv.last_message && (
                            <p className="last-message">{conv.last_message.content}</p>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* Active Users List */}
              {view === 'users' && (
                <div className="users-list">
                  {activeUsers.length === 0 ? (
                    <div className="empty-state">
                      <p>No users online</p>
                    </div>
                  ) : (
                    activeUsers
                      .filter(u => u.id !== user.id)
                      .map(u => (
                        <div 
                          key={u.id}
                          className="user-item"
                          onClick={() => startDirectChat(u.id)}
                        >
                          <div className="user-info">
                            <div className="user-status online"></div>
                            <div>
                              <strong>{u.full_name}</strong>
                              <p className="user-role">{u.role}</p>
                            </div>
                          </div>
                        </div>
                      ))
                  )}
                </div>
              )}

              {/* Chat View */}
              {view === 'chat' && activeConversation && (
                <>
                  <div className="messages-list">
                    {messages.map(msg => (
                      <div 
                        key={msg.id}
                        className={`message ${msg.sender_id === user.id ? 'sent' : 'received'}`}
                      >
                        <div className="message-content">
                          <p>{msg.content}</p>
                          <span className="message-time">
                            {new Date(msg.created_at).toLocaleTimeString([], { 
                              hour: '2-digit', 
                              minute: '2-digit' 
                            })}
                          </span>
                        </div>
                      </div>
                    ))}
                    {Object.values(typing).some(t => t) && (
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    )}
                    <div ref={messagesEndRef} />
                  </div>

                  <div className="message-input-container">
                    <input
                      type="text"
                      value={newMessage}
                      onChange={(e) => {
                        setNewMessage(e.target.value);
                        handleTyping();
                      }}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          sendMessage();
                        }
                      }}
                      placeholder="Type a message..."
                      className="message-input"
                    />
                    <button 
                      onClick={sendMessage}
                      className="send-button"
                      disabled={!newMessage.trim()}
                    >
                      Send
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default ChatBox;
