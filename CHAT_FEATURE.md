# In-App Chat Feature Documentation

## Overview

The in-app chat feature enables real-time communication between users within the Vibe Fitness Platform. It supports both direct (1:1) messaging and group chats, with features like typing indicators, read receipts, and active user tracking.

## Features

### Core Functionality
- ✅ Real-time messaging via WebSocket
- ✅ Direct (1:1) conversations
- ✅ Group chat conversations
- ✅ Message history with pagination
- ✅ Typing indicators
- ✅ Read receipts
- ✅ Active user tracking
- ✅ Message editing
- ✅ Message deletion
- ✅ Unread message counts
- ✅ Conversation list with last message preview

### Security Features
- ✅ JWT-based WebSocket authentication
- ✅ Role-based access control
- ✅ Conversation participant validation
- ✅ Message sender verification

## Architecture

### Backend Components

#### Database Models (`app/models/chat.py`)

**Conversation**
- Stores conversation metadata
- Supports both direct and group conversation types
- Tracks active status

**ConversationParticipant**
- Links users to conversations
- Manages admin status for group chats
- Tracks last read timestamp for read receipts

**Message**
- Stores individual chat messages
- Tracks read and edited status
- Links to conversation and sender

#### API Endpoints (`app/api/v1/chat.py`)

**REST Endpoints:**
- `POST /api/v1/chat/conversations` - Create a new conversation
- `GET /api/v1/chat/conversations` - Get all user's conversations
- `GET /api/v1/chat/conversations/{id}` - Get specific conversation with messages
- `POST /api/v1/chat/conversations/{id}/messages` - Send a message
- `PATCH /api/v1/chat/messages/{id}` - Update a message
- `DELETE /api/v1/chat/messages/{id}` - Delete a message
- `POST /api/v1/chat/conversations/{id}/participants` - Add participant to group
- `GET /api/v1/chat/users/active` - Get list of active/online users

**WebSocket Endpoint:**
- `WS /api/v1/chat/ws?token={jwt_token}` - Real-time chat connection

#### WebSocket Manager (`app/core/websocket.py`)

Manages WebSocket connections and handles:
- User connection/disconnection
- Real-time message broadcasting
- Typing indicators
- Read receipts
- Online status tracking

### Frontend Components

#### Context (`frontend/src/context/ChatContext.js`)
- Manages WebSocket connection state
- Handles incoming real-time messages
- Provides chat functionality to components

#### Components (`frontend/src/components/chat/`)

**ConversationList.js**
- Displays list of user's conversations
- Shows last message preview
- Displays unread counts
- Shows online status indicators

**ChatWindow.js**
- Main chat interface
- Message history display
- Message input with typing indicators
- Message editing/deletion

**MessageBubble.js**
- Individual message display
- Different styling for own vs. other messages
- Edit/delete actions for own messages

**NewConversationModal.js**
- Create new conversations
- Select participants
- Choose between direct or group chat

#### Service (`frontend/src/services/chatService.js`)
- API calls for chat operations
- WebSocket URL generation

#### Page (`frontend/src/pages/common/Chat.js`)
- Main chat page
- Integrates all chat components

## Usage

### Starting a Direct Conversation

1. Navigate to the Chat page
2. Click "New Conversation"
3. Select "Direct Message"
4. Choose a user
5. Click "Create Conversation"

### Creating a Group Chat

1. Navigate to the Chat page
2. Click "New Conversation"
3. Select "Group Chat"
4. Enter a group name
5. Select multiple users
6. Click "Create Conversation"

### Sending Messages

1. Select a conversation from the list
2. Type your message in the input field
3. Press Enter or click "Send"

### Editing Messages

1. Click "Edit" on your own message
2. Modify the text
3. Press Enter or click "Send"

### Real-time Features

- **Typing Indicators**: Shows when other users are typing
- **Read Receipts**: Automatically sent when viewing messages
- **Online Status**: Green indicator shows when users are online
- **Unread Counts**: Badge displays unread message count

## Database Schema

### Conversations Table
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NULL,
    conversation_type ENUM('direct', 'group') NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIMEZONE NOT NULL,
    updated_at TIMESTAMP WITH TIMEZONE NOT NULL
);
```

### Conversation Participants Table
```sql
CREATE TABLE conversation_participants (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    last_read_at TIMESTAMP WITH TIMEZONE NULL,
    created_at TIMESTAMP WITH TIMEZONE NOT NULL,
    updated_at TIMESTAMP WITH TIMEZONE NOT NULL,
    INDEX idx_conversation_user (conversation_id, user_id)
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id),
    sender_id INTEGER NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    is_edited BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIMEZONE NOT NULL,
    updated_at TIMESTAMP WITH TIMEZONE NOT NULL,
    INDEX idx_conversation_created (conversation_id, created_at)
);
```

## WebSocket Protocol

### Connection
```
WS /api/v1/chat/ws?token={jwt_token}
```

### Message Types

**Client → Server:**

```json
// Typing indicator
{
  "type": "typing",
  "conversation_id": 123,
  "is_typing": true
}

// Read receipt
{
  "type": "read_receipt",
  "conversation_id": 123,
  "message_id": 456
}
```

**Server → Client:**

```json
// New message
{
  "type": "message",
  "data": {
    "id": 789,
    "conversation_id": 123,
    "sender_id": 1,
    "sender": {
      "id": 1,
      "full_name": "John Doe",
      "email": "john@example.com",
      "role": "client"
    },
    "content": "Hello!",
    "is_read": false,
    "is_edited": false,
    "created_at": "2025-10-15T12:00:00Z",
    "updated_at": "2025-10-15T12:00:00Z"
  }
}

// Typing indicator
{
  "type": "typing",
  "data": {
    "conversation_id": 123,
    "user_id": 2,
    "is_typing": true
  }
}

// Read receipt
{
  "type": "read_receipt",
  "data": {
    "conversation_id": 123,
    "message_id": 456,
    "user_id": 2
  }
}

// User status
{
  "type": "user_status",
  "data": {
    "user_id": 2,
    "is_online": true,
    "timestamp": "2025-10-15T12:00:00Z"
  }
}
```

## API Examples

### Create a Direct Conversation
```bash
POST /api/v1/chat/conversations
Authorization: Bearer {token}
Content-Type: application/json

{
  "conversation_type": "direct",
  "participant_ids": [2],
  "name": null
}
```

### Create a Group Conversation
```bash
POST /api/v1/chat/conversations
Authorization: Bearer {token}
Content-Type: application/json

{
  "conversation_type": "group",
  "participant_ids": [2, 3, 4],
  "name": "Team Discussion"
}
```

### Send a Message
```bash
POST /api/v1/chat/conversations/1/messages
Authorization: Bearer {token}
Content-Type: application/json

{
  "conversation_id": 1,
  "content": "Hello, everyone!"
}
```

### Get Conversation with Messages
```bash
GET /api/v1/chat/conversations/1?limit=50&offset=0
Authorization: Bearer {token}
```

## Testing

### Backend Tests
Run the chat tests:
```bash
cd backend
pytest tests/test_chat.py -v
```

### Manual Testing

1. **Setup:**
   - Start the backend server
   - Start the frontend development server
   - Create at least 2 test users

2. **Test Direct Chat:**
   - Login as User 1
   - Navigate to Chat page
   - Create a new direct conversation with User 2
   - Send messages from both users
   - Verify real-time updates

3. **Test Group Chat:**
   - Create a group conversation with 3+ users
   - Send messages from different users
   - Test typing indicators
   - Verify read receipts

4. **Test Message Features:**
   - Edit your own messages
   - Delete your own messages
   - Verify you cannot edit/delete others' messages

## Deployment Considerations

### Environment Variables
Ensure these are configured in production:
```
REDIS_URL=redis://redis:6379/0  # For future scalability
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Database Migration
Apply the chat migration:
```bash
alembic upgrade head
```

### WebSocket Configuration
- Configure WebSocket proxy in production (nginx/Apache)
- Set appropriate timeouts
- Enable compression for WebSocket connections

### Scaling
For production with multiple backend instances:
- Use Redis pub/sub for message broadcasting
- Implement sticky sessions for WebSocket connections
- Consider using Socket.IO with Redis adapter

## Future Enhancements

### Planned Features
- [ ] File/image attachments
- [ ] Voice/video calls
- [ ] Message reactions (emoji)
- [ ] Message threading
- [ ] Message search
- [ ] Notification preferences
- [ ] Message forwarding
- [ ] Conversation pinning
- [ ] Message encryption (E2E)
- [ ] Delivery receipts
- [ ] Message status (sent/delivered/read)
- [ ] Offline message queue
- [ ] Push notifications
- [ ] Desktop notifications
- [ ] Audio notifications

### Performance Optimizations
- [ ] Message pagination with infinite scroll
- [ ] Virtual scrolling for large message lists
- [ ] Image lazy loading
- [ ] WebSocket reconnection with exponential backoff
- [ ] Message caching in IndexedDB

## Troubleshooting

### WebSocket Connection Issues
- Verify JWT token is valid
- Check CORS configuration
- Ensure WebSocket proxy is configured correctly
- Check browser console for errors

### Messages Not Updating in Real-time
- Check WebSocket connection status
- Verify user is authenticated
- Check network connectivity
- Inspect WebSocket frames in browser dev tools

### Database Migration Errors
- Ensure database is accessible
- Verify previous migrations are applied
- Check for conflicting table/column names
- Review migration file for syntax errors

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check browser console for errors
4. Review backend logs
5. Contact the development team

## License

This feature is part of the Vibe Fitness Platform and follows the project's license terms.
