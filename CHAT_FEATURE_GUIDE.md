# WhatsApp-Style In-App Chat Feature - Implementation Guide

## Overview

This guide provides instructions for deploying and using the new in-app chat feature. The chat system enables real-time messaging between users with WhatsApp-like functionality.

## Features Implemented

### Backend
- **Real-time WebSocket communication** for instant message delivery
- **Direct (1:1) and Group chat** support
- **Online presence tracking** to see who's currently online
- **Message history** with persistent storage
- **Edit and delete messages** functionality
- **Security**: Users can only access chats they're part of

### Frontend
- **Floating chat button** (similar to feedback button)
- **WhatsApp-inspired UI** with green color scheme
- **Chat rooms list** showing recent conversations
- **Online users list** to start new chats
- **Real-time message updates** via WebSocket
- **Typing indicators** support
- **Responsive design** for mobile and desktop

## Database Migration

### Upgrade to Latest Version (Add Chat Tables)

1. **Using Docker (Recommended)**:
   ```bash
   cd /path/to/vibe_project
   docker-compose exec backend alembic upgrade head
   ```

2. **Local Development**:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   alembic upgrade head
   ```

3. **Using the migration script**:
   ```bash
   cd backend
   ./scripts/db_migrate.sh upgrade
   ```

### Downgrade (Remove Chat Tables)

If you need to rollback the chat feature:

1. **Using Docker**:
   ```bash
   docker-compose exec backend alembic downgrade -1
   ```

2. **Local Development**:
   ```bash
   cd backend
   alembic downgrade -1
   ```

3. **Downgrade to specific version** (before chat feature):
   ```bash
   alembic downgrade 005_add_feedback_status
   ```

### Check Current Migration Status

```bash
# With Docker
docker-compose exec backend alembic current

# Local
cd backend && alembic current
```

### View Migration History

```bash
# With Docker
docker-compose exec backend alembic history --verbose

# Local
cd backend && alembic history --verbose
```

## Starting the Application

### Using Docker Compose (Recommended)

1. **Start all services**:
   ```bash
   docker-compose up -d
   ```

2. **Run database migrations**:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

3. **Check logs**:
   ```bash
   docker-compose logs -f
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

### Stopping the Application

```bash
docker-compose down
```

### Restarting After Changes

```bash
docker-compose down
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

## Using the Chat Feature

### For End Users

1. **Login** to your account
2. Click the **💬 Chat** button in the bottom-right corner (next to Feedback)
3. You'll see two tabs:
   - **💬 Chats**: Your existing conversations
   - **👥 Online**: Currently online users

### Starting a New Chat

1. Click the **👥 Online** tab
2. See a list of users currently online (green dot indicator)
3. Click on any user to start a direct chat
4. Type your message and press Enter or click the send button (➤)

### Group Chats

Group chat creation is currently available through the API. Future updates will add a UI button.

**API Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/chat/rooms" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fitness Group",
    "type": "group",
    "participant_ids": [2, 3, 4]
  }'
```

### Editing Messages

Currently, message editing is available through the API. Future updates will add a UI option.

### Real-time Features

- **Instant delivery**: Messages appear immediately for all participants
- **Online status**: See who's currently online with a green dot
- **Typing indicators**: Know when someone is typing (backend support ready)
- **Auto-reconnect**: WebSocket automatically reconnects if connection drops

## API Endpoints

### Chat Rooms

- `POST /api/v1/chat/rooms` - Create a new chat room
- `GET /api/v1/chat/rooms` - Get all chat rooms for current user
- `GET /api/v1/chat/rooms/{room_id}` - Get chat room with messages
- `POST /api/v1/chat/rooms/{room_id}/participants` - Add participants (group only)

### Messages

- `POST /api/v1/chat/messages` - Send a message
- `PUT /api/v1/chat/messages/{message_id}` - Edit a message
- `DELETE /api/v1/chat/messages/{message_id}` - Delete a message
- `POST /api/v1/chat/mark-read` - Mark messages as read

### Presence

- `GET /api/v1/chat/presence` - Get list of online users

### WebSocket

- `WS /api/v1/chat/ws/{user_id}` - WebSocket connection for real-time updates

Full API documentation: http://localhost:8000/api/docs

## Architecture

### Backend Stack
- **FastAPI** for REST API endpoints
- **WebSocket** for real-time communication
- **SQLAlchemy** for database ORM
- **PostgreSQL** for data persistence
- **Alembic** for database migrations

### Frontend Stack
- **React 19** for UI components
- **Native WebSocket API** (no external dependencies)
- **CSS3** for WhatsApp-inspired styling

### Database Schema

**Tables Created**:
1. `chat_rooms` - Stores chat room information
2. `messages` - Stores all chat messages
3. `chat_participants` - Junction table for room members
4. `user_presence` - Tracks online/offline status

## Security Considerations

### Current Implementation
- ✅ JWT authentication required for all endpoints
- ✅ Users can only access chats they're participants in
- ✅ Users can only edit/delete their own messages
- ✅ WebSocket connection authenticated by user ID
- ✅ SQL injection protected by SQLAlchemy ORM

### Future Enhancements
- 🔄 End-to-end encryption for messages
- 🔄 Rate limiting for message sending
- 🔄 Message retention policies
- 🔄 File upload virus scanning

## Testing

### Running Backend Tests

```bash
# With Docker
docker-compose exec backend pytest tests/test_chat.py -v

# Local
cd backend
pytest tests/test_chat.py -v
```

### Manual Testing Checklist

- [ ] Login with two different users in different browsers
- [ ] Check that both users show as online
- [ ] Start a direct chat from one user
- [ ] Send messages back and forth
- [ ] Verify messages appear instantly
- [ ] Check that chat history persists after refresh
- [ ] Test offline behavior (close one browser)
- [ ] Verify user goes offline in the other browser
- [ ] Test responsive design on mobile viewport

## Troubleshooting

### WebSocket Connection Issues

**Problem**: Chat doesn't connect or messages don't appear in real-time

**Solutions**:
1. Check that backend is running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Verify WebSocket URL in browser console
4. Ensure no firewall is blocking WebSocket connections
5. Check that JWT token is valid

### Migration Errors

**Problem**: `alembic upgrade head` fails

**Solutions**:
1. Check database is running: `docker-compose ps postgres`
2. Verify connection string in `.env`
3. Check migration files are present
4. Try running migrations one at a time: `alembic upgrade +1`
5. Check for conflicting migrations: `alembic current`

### Chat UI Not Appearing

**Problem**: Chat button doesn't show up

**Solutions**:
1. Ensure you're logged in (chat only shows for authenticated users)
2. Check browser console for JavaScript errors
3. Clear browser cache and reload
4. Verify frontend is running: `docker-compose ps frontend`

### Messages Not Persisting

**Problem**: Messages disappear after refresh

**Solutions**:
1. Check database migrations are applied: `alembic current`
2. Verify database connection
3. Check backend logs for errors
4. Ensure messages are being saved: Check `/api/v1/chat/rooms/{id}` endpoint

## Performance Considerations

### Optimization Tips

1. **Message Pagination**: Currently loads all messages. For high-traffic rooms, implement pagination:
   ```python
   # Future enhancement
   @router.get("/rooms/{room_id}/messages")
   async def get_messages(room_id: int, skip: int = 0, limit: int = 50):
       # Paginated query
   ```

2. **WebSocket Scaling**: Current implementation uses in-memory connection manager. For production:
   - Use Redis for pub/sub across multiple servers
   - Implement connection pooling

3. **Database Indexes**: Already added on frequently queried columns. Monitor and add more as needed.

## Future Enhancements

### Planned Features
- [ ] Group chat creation from UI
- [ ] Message search functionality
- [ ] File and image sharing
- [ ] Voice messages
- [ ] Read receipts (✓✓)
- [ ] Message reactions (emoji)
- [ ] Push notifications
- [ ] Chat export functionality
- [ ] Admin moderation tools
- [ ] Message deletion for everyone
- [ ] Disappearing messages
- [ ] Chat themes

## Support

For issues or questions:
1. Check this guide first
2. Review API documentation: http://localhost:8000/api/docs
3. Check backend logs: `docker-compose logs backend`
4. Review frontend console for errors
5. Create a GitHub issue with:
   - Error messages
   - Steps to reproduce
   - Screenshots if applicable

## Version History

- **v1.0.0** (2025-10-15)
  - Initial release
  - Direct and group chat support
  - Real-time messaging via WebSocket
  - Online presence tracking
  - WhatsApp-style floating UI
