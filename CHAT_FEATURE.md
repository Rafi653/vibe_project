# WhatsApp-Style Chat Feature Documentation

## Overview

The Vibe Fitness Platform now includes a real-time chat feature that enables users to communicate seamlessly within the app. This feature provides WhatsApp-style messaging with real-time updates, group chats, online presence indicators, and a floating chat interface.

## Features

### ✅ Implemented

1. **Real-Time Messaging**
   - WebSocket-based instant message delivery
   - Live message updates without page refresh
   - Typing indicators to show when users are typing

2. **Direct Messaging (1:1 Chat)**
   - Private conversations between any two users
   - Automatic conversation creation/retrieval
   - Message history preserved

3. **Group Chat**
   - Create group conversations with multiple participants
   - Custom group names
   - All participants receive messages in real-time

4. **Online Presence**
   - Display active/online users
   - Real-time presence updates
   - Last seen timestamps

5. **Floating Chat Interface**
   - Similar to the feedback button
   - Non-intrusive, accessible from anywhere
   - Smooth animations and transitions
   - Mobile-responsive design

6. **Message History**
   - All messages stored in database
   - Conversations persist between sessions
   - Scroll through message history

## Architecture

### Backend Components

#### Database Models (`backend/app/models/chat.py`)

1. **Conversation**
   - Supports both direct and group conversations
   - Tracks conversation type, name, and creator
   - Many-to-many relationship with users (participants)

2. **Message**
   - Stores message content and metadata
   - Tracks sender and conversation
   - Message status (sent, delivered, read)

3. **UserPresence**
   - Tracks online/offline status
   - Records last seen timestamp
   - Real-time updates via WebSocket

#### API Endpoints (`backend/app/api/v1/chat.py`)

**WebSocket Endpoint:**
- `ws://localhost:8000/api/v1/chat/ws/{token}` - Real-time messaging connection

**REST Endpoints:**
- `POST /api/v1/chat/conversations` - Create new conversation
- `GET /api/v1/chat/conversations` - Get all user's conversations
- `GET /api/v1/chat/conversations/{id}` - Get specific conversation with messages
- `GET /api/v1/chat/active-users` - Get list of online users
- `GET /api/v1/chat/presence/{user_id}` - Get user presence status

#### WebSocket Message Types

1. **message** - Send/receive chat messages
   ```json
   {
     "type": "message",
     "conversation_id": 1,
     "content": "Hello!"
   }
   ```

2. **typing** - Indicate user is typing
   ```json
   {
     "type": "typing",
     "conversation_id": 1
   }
   ```

3. **read** - Mark message as read
   ```json
   {
     "type": "read",
     "message_id": 123
   }
   ```

4. **presence** - User online/offline updates
   ```json
   {
     "type": "presence",
     "user_id": 5,
     "is_online": true
   }
   ```

### Frontend Components

#### Chat Service (`frontend/src/services/chatService.js`)
- Handles all API calls for chat operations
- Manages WebSocket connection
- Provides methods for sending messages and typing indicators

#### ChatBox Component (`frontend/src/components/ChatBox.js`)
- Main chat interface component
- Three views: Conversations, Active Users, and Chat
- Manages WebSocket connection and message state
- Real-time message updates and presence tracking

#### Styling (`frontend/src/components/ChatBox.css`)
- WhatsApp-inspired design
- Smooth animations and transitions
- Fully responsive for mobile and desktop
- Green gradient theme (different from purple feedback button)

## Usage

### For End Users

1. **Opening Chat**
   - Click the green "💬 Chat" button in the bottom-right corner
   - The button is positioned above the feedback button

2. **Starting a Direct Chat**
   - Click "Active Users" tab to see online users
   - Click on any user to start a direct conversation
   - If a conversation already exists, it will open the existing one

3. **Sending Messages**
   - Type your message in the input field
   - Press Enter or click "Send" to send
   - Messages appear instantly for all participants

4. **Group Chats**
   - Group chats can be created via API (future: add UI button)
   - View all group conversations in the "Conversations" tab

5. **Viewing Message History**
   - Click on any conversation to view full message history
   - Scroll up to see older messages
   - Use the back button to return to conversations list

### For Developers

#### Creating a Direct Conversation

```javascript
import chatService from '../services/chatService';

const conversation = await chatService.createConversation({
  type: 'direct',
  participant_ids: [otherUserId]
});
```

#### Creating a Group Conversation

```javascript
const conversation = await chatService.createConversation({
  type: 'group',
  name: 'My Group Chat',
  participant_ids: [userId1, userId2, userId3]
});
```

#### Connecting to WebSocket

```javascript
const ws = chatService.connectWebSocket(
  (data) => {
    // Handle incoming messages
    console.log('Received:', data);
  },
  (error) => {
    console.error('WebSocket error:', error);
  }
);
```

#### Sending a Message

```javascript
chatService.sendMessage(ws, conversationId, 'Hello, world!');
```

## Database Migration

The chat feature requires new database tables. Run the migration:

```bash
cd backend
alembic upgrade head
```

Or using Docker:

```bash
docker-compose exec backend alembic upgrade head
```

This creates the following tables:
- `conversations` - Stores conversation metadata
- `messages` - Stores all chat messages
- `user_presence` - Tracks user online status
- `conversation_participants` - Many-to-many relationship table

## Testing

### Backend Tests

Run the test suite:

```bash
cd backend
pytest tests/test_chat.py -v
```

All 9 tests pass:
- ✅ Create direct conversation
- ✅ Prevent duplicate direct conversations
- ✅ Create group conversation
- ✅ Get all conversations
- ✅ Get conversation details
- ✅ Authorization checks
- ✅ Get active users
- ✅ Get user presence
- ✅ Handle missing presence data

### Frontend Testing

The frontend components follow React best practices and can be tested with:

```bash
cd frontend
npm test
```

## Security Considerations

1. **Authentication Required**
   - All chat endpoints require JWT authentication
   - WebSocket connections validated via token
   - Users can only access their own conversations

2. **Authorization**
   - Users can only view conversations they participate in
   - 403 errors returned for unauthorized access attempts

3. **Data Privacy**
   - Messages stored securely in database
   - No client-side message caching (future enhancement)
   - User presence only visible to authenticated users

## Performance

1. **WebSocket Connection Management**
   - Single WebSocket per user session
   - Automatic reconnection on disconnect
   - Efficient message broadcasting to participants only

2. **Database Queries**
   - Indexed columns for fast lookups
   - Eager loading to prevent N+1 queries
   - Pagination support (ready for high message volumes)

3. **Frontend Optimization**
   - Messages render efficiently with React
   - Smooth scrolling with refs
   - Typing indicators debounced to reduce traffic

## Known Limitations

1. **User Names in Direct Chats**
   - Currently shows "Direct Message" for all 1:1 chats
   - Future: Fetch and display other participant's name

2. **Message Status**
   - Read receipts implemented but not displayed in UI
   - Future: Show checkmarks for sent/delivered/read

3. **File/Media Sharing**
   - Not implemented in MVP
   - Database supports future media attachments

4. **Search Functionality**
   - No message search yet
   - Future: Full-text search across messages

5. **Notifications**
   - In-app visual indicators only
   - Future: Browser push notifications

## Future Enhancements

### High Priority
1. Show participant names in direct messages
2. Display read receipts with checkmarks
3. Browser push notifications for new messages
4. Message search functionality
5. User profile pictures in chat

### Medium Priority
1. File and image sharing
2. Voice messages
3. Message editing and deletion
4. Conversation archiving
5. Mute/unmute conversations

### Low Priority
1. Emoji reactions to messages
2. GIF support
3. Video calls integration
4. Chat themes/customization
5. Message forwarding

## Troubleshooting

### WebSocket Connection Issues

**Problem:** Chat not connecting
**Solution:** Check that backend is running and WebSocket URL is correct

```javascript
// frontend/.env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

### Messages Not Appearing

**Problem:** Messages sent but not received
**Solution:** 
1. Check browser console for errors
2. Verify WebSocket connection is active
3. Check user is participant in conversation

### Active Users Not Showing

**Problem:** No users in active list
**Solution:**
1. Users need to open chat at least once to register presence
2. Check `user_presence` table has entries
3. Presence updates on WebSocket connection

## API Reference

See the interactive API documentation:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

Navigate to the "chat" tag to see all chat endpoints.

## Contributing

When contributing to the chat feature:

1. Follow existing code patterns
2. Add tests for new functionality
3. Update this documentation
4. Test WebSocket connections thoroughly
5. Ensure mobile responsiveness

## Support

For issues or questions:
1. Check this documentation first
2. Review the API documentation
3. Check the test files for usage examples
4. Open an issue on GitHub with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Browser/environment details
