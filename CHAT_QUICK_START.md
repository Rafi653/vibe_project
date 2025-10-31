# Chat Feature - Quick Start Guide

## Prerequisites

Before testing the chat feature, ensure you have:
- Python 3.8+ installed
- Node.js 14+ installed
- PostgreSQL database running
- Redis (optional, for future scalability)

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## Testing the Chat Feature

### Step 1: Create Test Users

1. Open `http://localhost:3000/signup` in your browser
2. Create at least 2 test users:
   - User 1: `user1@test.com` / `password123`
   - User 2: `user2@test.com` / `password123`

### Step 2: Test Direct Messaging

**In Browser Window 1 (User 1):**
1. Login as `user1@test.com`
2. Navigate to Chat page (click "Chat" in navigation)
3. Click "New Conversation"
4. Select "Direct Message"
5. Choose User 2 from the list
6. Click "Create Conversation"
7. Type a message and press Enter

**In Browser Window 2 (User 2) - Incognito/Private mode:**
1. Login as `user2@test.com`
2. Navigate to Chat page
3. You should see the conversation from User 1
4. Click on the conversation
5. You should see User 1's message in real-time
6. Reply to the message

**Expected Results:**
- Messages appear instantly in both windows
- Typing indicators show when the other user is typing
- Green online indicator shows next to active users
- Unread count badge appears on conversation list
- Read receipts mark messages as read

### Step 3: Test Group Chat

**In Browser Window 1 (User 1):**
1. Click "New Conversation"
2. Select "Group Chat"
3. Enter a group name (e.g., "Team Chat")
4. Select User 2 and any other users
5. Click "Create Conversation"
6. Send a message to the group

**In Browser Window 2 (User 2):**
1. The group conversation should appear automatically
2. Click on it to view messages
3. Send a message to the group

**Expected Results:**
- All participants see the group conversation
- Messages are visible to all members
- Group name is displayed in the chat header
- Multiple users can chat simultaneously

### Step 4: Test Message Features

**Edit a Message:**
1. Click "Edit" on one of your messages
2. Modify the text
3. Press Enter
4. The message should update with "(edited)" indicator

**Delete a Message:**
1. Click "Delete" on one of your messages
2. Confirm deletion
3. The message should disappear

**Expected Results:**
- Only your own messages have Edit/Delete buttons
- Edited messages show the "(edited)" indicator
- Deleted messages are removed from the conversation

### Step 5: Verify Real-time Features

**Typing Indicators:**
1. In one browser window, start typing a message
2. In the other browser window, you should see "User is typing..." indicator
3. The indicator disappears after 2 seconds of inactivity

**Online Status:**
1. With both users logged in, verify green indicators appear
2. Close one browser window
3. The other user should see the online status change (may take a few seconds)

**Unread Counts:**
1. Have User 1 send messages
2. In User 2's window, stay on a different conversation
3. An unread count badge should appear on the conversation
4. Click the conversation - the badge should disappear

## Troubleshooting

### WebSocket Connection Issues

**Symptom:** Messages don't appear in real-time

**Solution:**
1. Check browser console for errors
2. Verify backend is running
3. Look for "WebSocket connected" message in console
4. Ensure JWT token is valid (try logging out and back in)

### Messages Not Sending

**Symptom:** Error when trying to send messages

**Solution:**
1. Check network tab in browser dev tools
2. Verify API endpoint is reachable
3. Check backend logs for errors
4. Ensure you're a participant in the conversation

### Database Connection Errors

**Symptom:** Backend fails to start or migrations fail

**Solution:**
1. Verify PostgreSQL is running
2. Check DATABASE_URL in backend/.env
3. Ensure database exists
4. Try running migrations again: `alembic upgrade head`

### CORS Errors

**Symptom:** API requests fail with CORS errors

**Solution:**
1. Verify ALLOWED_ORIGINS in backend/app/core/config.py
2. Ensure frontend URL is included
3. Restart the backend server

## API Testing with cURL

You can also test the API directly with cURL:

### Login and Get Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user1@test.com","password":"password123"}'
```

Save the `access_token` from the response.

### Get Conversations
```bash
curl http://localhost:8000/api/v1/chat/conversations \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create a Conversation
```bash
curl -X POST http://localhost:8000/api/v1/chat/conversations \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"conversation_type":"direct","participant_ids":[2],"name":null}'
```

### Send a Message
```bash
curl -X POST http://localhost:8000/api/v1/chat/conversations/1/messages \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":1,"content":"Hello from cURL!"}'
```

## Browser Developer Tools

### Monitoring WebSocket Connection

1. Open browser Developer Tools (F12)
2. Go to Network tab
3. Filter by "WS" (WebSocket)
4. Click on the WebSocket connection
5. View Messages tab to see real-time communication

### Checking Console Logs

The chat feature logs useful information:
- "WebSocket connected" - Connection established
- "WebSocket disconnected" - Connection lost
- "User {id} connected" - User came online
- Message type logs for debugging

## Performance Testing

### Load Testing Conversations

Create multiple conversations to test performance:
```bash
# Create 10 test users and conversations
for i in {1..10}; do
  # Create user
  curl -X POST http://localhost:8000/api/v1/auth/signup \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"test${i}@test.com\",\"password\":\"password123\",\"full_name\":\"Test User ${i}\",\"role\":\"client\"}"
done
```

### Message Load Testing

Send multiple messages rapidly to test real-time performance:
1. Open multiple browser windows
2. Send messages from different users simultaneously
3. Verify all messages arrive in real-time
4. Check for any lag or delays

## Next Steps

After successfully testing:
1. Review the full documentation in CHAT_FEATURE.md
2. Customize the UI/styling as needed
3. Configure for production deployment
4. Set up monitoring and logging
5. Consider adding file attachments feature
6. Implement push notifications

## Support

If you encounter issues not covered here:
1. Check CHAT_FEATURE.md for detailed documentation
2. Review backend logs: Check terminal running uvicorn
3. Check frontend logs: Browser console (F12)
4. Review the code comments for implementation details

## Video Tutorial (Coming Soon)

A video walkthrough of these steps will be available soon.

---

**Happy Chatting! 🚀**
