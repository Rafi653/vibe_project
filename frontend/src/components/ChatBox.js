import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import chatService from '../services/chatService';
import './ChatBox.css';

function ChatBox() {
  const { user, isAuthenticated } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [activeView, setActiveView] = useState('rooms'); // 'rooms', 'chat', 'users', 'newGroup'
  const [chatRooms, setChatRooms] = useState([]);
  const [activeRoom, setActiveRoom] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [onlineUsers, setOnlineUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);
  const [isTyping, setIsTyping] = useState(false);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Connect to WebSocket when authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      chatService.connect(
        user.id,
        handleIncomingMessage,
        handlePresenceUpdate
      );

      return () => {
        chatService.disconnect();
      };
    }
  }, [isAuthenticated, user]);

  // Load chat rooms when opened
  useEffect(() => {
    if (isOpen && isAuthenticated) {
      loadChatRooms();
      loadOnlineUsers();
    }
  }, [isOpen, isAuthenticated]);

  const handleIncomingMessage = (data) => {
    if (data.type === 'message' && activeRoom && data.chat_room_id === activeRoom.id) {
      // Add message to current chat
      setMessages(prev => [...prev, data]);
      chatService.markAsRead(activeRoom.id);
    }
    // Refresh room list to update last message
    loadChatRooms();
  };

  const handlePresenceUpdate = (data) => {
    if (data.type === 'presence') {
      loadOnlineUsers();
    }
  };

  const loadChatRooms = async () => {
    try {
      const rooms = await chatService.getChatRooms();
      setChatRooms(rooms);
    } catch (err) {
      setError('Failed to load chat rooms');
    }
  };

  const loadOnlineUsers = async () => {
    try {
      const users = await chatService.getOnlineUsers();
      setOnlineUsers(users);
    } catch (err) {
      console.error('Failed to load online users:', err);
    }
  };

  const openChatRoom = async (room) => {
    setLoading(true);
    setError('');
    try {
      const roomDetails = await chatService.getChatRoom(room.id);
      setActiveRoom(roomDetails);
      setMessages(roomDetails.messages || []);
      setActiveView('chat');
      chatService.markAsRead(room.id);
    } catch (err) {
      setError('Failed to load chat');
    } finally {
      setLoading(false);
    }
  };

  const startDirectChat = async (userId) => {
    setLoading(true);
    setError('');
    try {
      const room = await chatService.createChatRoom([userId], null, 'direct');
      await openChatRoom(room);
    } catch (err) {
      setError('Failed to start chat');
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !activeRoom) return;

    const messageContent = newMessage;
    setNewMessage('');

    try {
      const message = await chatService.sendChatMessage(activeRoom.id, messageContent);
      
      // Send via WebSocket for real-time delivery
      chatService.sendMessage({
        type: 'message',
        chat_room_id: activeRoom.id,
        ...message
      });

      // Add to local messages
      setMessages(prev => [...prev, message]);
    } catch (err) {
      setError('Failed to send message');
      setNewMessage(messageContent); // Restore message on error
    }
  };

  const handleTyping = () => {
    if (!isTyping && activeRoom) {
      setIsTyping(true);
      chatService.sendMessage({
        type: 'typing',
        chat_room_id: activeRoom.id,
        user_id: user.id,
        user_name: user.full_name
      });
      
      setTimeout(() => setIsTyping(false), 3000);
    }
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
    return date.toLocaleDateString();
  };

  const getRoomName = (room) => {
    if (room.name) return room.name;
    if (room.type === 'group') return `Group (${room.participant_count})`;
    return 'Direct Chat';
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
        {onlineUsers.length > 0 && (
          <span className="online-badge">{onlineUsers.length}</span>
        )}
      </button>

      {isOpen && (
        <div className="chat-overlay" onClick={() => setIsOpen(false)}>
          <div className="chat-modal" onClick={(e) => e.stopPropagation()}>
            <div className="chat-header">
              <h2>
                {activeView === 'rooms' && '💬 Chats'}
                {activeView === 'users' && '👥 Online Users'}
                {activeView === 'chat' && getRoomName(activeRoom)}
              </h2>
              <div className="chat-header-actions">
                {activeView === 'chat' && (
                  <button 
                    className="chat-back-btn"
                    onClick={() => {
                      setActiveView('rooms');
                      setActiveRoom(null);
                      setMessages([]);
                    }}
                  >
                    ← Back
                  </button>
                )}
                <button 
                  className="chat-close"
                  onClick={() => setIsOpen(false)}
                  aria-label="Close"
                >
                  ×
                </button>
              </div>
            </div>

            {error && (
              <div className="chat-error">
                {error}
                <button onClick={() => setError('')}>×</button>
              </div>
            )}

            {/* Navigation Tabs */}
            {activeView !== 'chat' && (
              <div className="chat-tabs">
                <button 
                  className={activeView === 'rooms' ? 'active' : ''}
                  onClick={() => setActiveView('rooms')}
                >
                  💬 Chats
                </button>
                <button 
                  className={activeView === 'users' ? 'active' : ''}
                  onClick={() => setActiveView('users')}
                >
                  👥 Online ({onlineUsers.length})
                </button>
              </div>
            )}

            {/* Rooms List View */}
            {activeView === 'rooms' && (
              <div className="chat-content">
                {loading ? (
                  <div className="chat-loading">Loading...</div>
                ) : chatRooms.length === 0 ? (
                  <div className="chat-empty">
                    <p>No chats yet</p>
                    <p className="chat-empty-hint">Start a chat with online users!</p>
                  </div>
                ) : (
                  <div className="chat-rooms-list">
                    {chatRooms.map(room => (
                      <div 
                        key={room.id}
                        className="chat-room-item"
                        onClick={() => openChatRoom(room)}
                      >
                        <div className="chat-room-avatar">
                          {room.type === 'group' ? '👥' : '💬'}
                        </div>
                        <div className="chat-room-info">
                          <div className="chat-room-name">{getRoomName(room)}</div>
                          {room.last_message && (
                            <div className="chat-room-last-message">
                              {room.last_message.substring(0, 40)}
                              {room.last_message.length > 40 ? '...' : ''}
                            </div>
                          )}
                        </div>
                        {room.last_message_at && (
                          <div className="chat-room-time">
                            {formatTime(room.last_message_at)}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Online Users View */}
            {activeView === 'users' && (
              <div className="chat-content">
                {onlineUsers.length === 0 ? (
                  <div className="chat-empty">
                    <p>No users online</p>
                  </div>
                ) : (
                  <div className="chat-users-list">
                    {onlineUsers.map(onlineUser => (
                      <div 
                        key={onlineUser.user_id}
                        className="chat-user-item"
                        onClick={() => startDirectChat(onlineUser.user_id)}
                      >
                        <div className="chat-user-avatar">👤</div>
                        <div className="chat-user-info">
                          <div className="chat-user-name">{onlineUser.user_name}</div>
                          <div className="chat-user-status">
                            <span className="online-dot"></span> Online
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Chat View */}
            {activeView === 'chat' && activeRoom && (
              <>
                <div className="chat-messages">
                  {messages.length === 0 ? (
                    <div className="chat-empty">
                      <p>No messages yet</p>
                      <p className="chat-empty-hint">Start the conversation!</p>
                    </div>
                  ) : (
                    messages.map((msg, index) => (
                      <div 
                        key={msg.id || index}
                        className={`chat-message ${msg.sender_id === user.id ? 'own' : 'other'}`}
                      >
                        <div className="chat-message-content">
                          {msg.sender_id !== user.id && (
                            <div className="chat-message-sender">{msg.sender_name}</div>
                          )}
                          <div className="chat-message-text">{msg.content}</div>
                          <div className="chat-message-time">
                            {formatTime(msg.created_at)}
                            {msg.is_edited && <span className="edited-label"> (edited)</span>}
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                  <div ref={messagesEndRef} />
                </div>

                <form className="chat-input-form" onSubmit={handleSendMessage}>
                  <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => {
                      setNewMessage(e.target.value);
                      handleTyping();
                    }}
                    placeholder="Type a message..."
                    maxLength={5000}
                    disabled={loading}
                  />
                  <button 
                    type="submit" 
                    disabled={!newMessage.trim() || loading}
                    className="chat-send-btn"
                  >
                    ➤
                  </button>
                </form>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
}

export default ChatBox;
