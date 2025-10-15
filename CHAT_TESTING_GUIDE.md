# Chat Feature - Testing Guide

## Quick Test Guide

This guide helps you test the chat feature quickly and thoroughly.

## Prerequisites

1. **Backend running** on http://localhost:8000
2. **Frontend running** on http://localhost:3000
3. **Database migrated** with `alembic upgrade head`
4. **Test data seeded** (optional but recommended)

## Test Data Setup

### Seed Test Users

```bash
cd backend
python -m app.db.seed_charts
```

This creates test accounts:
- **Admin**: admin2@vibe.com / admin123
- **Coaches**: coach1@vibe.com / coach1123, coach2@vibe.com / coach2123
- **Clients**: client1@vibe.com / client1123, client2@vibe.com / client2123, etc.

## Testing Scenarios

### Scenario 1: Basic Direct Chat

**Goal**: Test 1:1 messaging between two users

**Steps**:
1. Open two browser windows (or use incognito for second)
2. Window 1: Login as `client1@vibe.com / client1123`
3. Window 2: Login as `client2@vibe.com / client2123`
4. Window 1: Click green "💬 Chat" button
5. Window 1: Click "Active Users" tab
6. Window 1: You should see client2 (and possibly others) with green dot
7. Window 1: Click on client2 to start chat
8. Window 1: Type "Hello from client1!" and press Enter
9. Window 2: Click green "💬 Chat" button
10. Window 2: You should see the conversation appear in Conversations list
11. Window 2: Click the conversation
12. Window 2: You should see "Hello from client1!" message
13. Window 2: Type "Hi back!" and send
14. Window 1: Should see "Hi back!" appear immediately

**Expected Results**:
- ✅ Active users list shows online users
- ✅ Messages appear in real-time
- ✅ Sent messages on right (green bubbles)
- ✅ Received messages on left (gray bubbles)
- ✅ Timestamps display correctly

### Scenario 2: Typing Indicators

**Goal**: Test real-time typing indicators

**Steps**:
1. Continue from Scenario 1 (two users in a chat)
2. Window 1: Start typing a message (don't send yet)
3. Window 2: Watch the bottom of the chat area
4. Window 2: Should see "⋯ ⋯ ⋯" typing indicator with bouncing dots
5. Window 1: Stop typing for 3 seconds
6. Window 2: Typing indicator should disappear

**Expected Results**:
- ✅ Typing indicator appears when user types
- ✅ Indicator disappears after 3 seconds of no typing
- ✅ Animation is smooth

### Scenario 3: Presence Updates

**Goal**: Test online/offline presence tracking

**Steps**:
1. Window 1: Login as client1@vibe.com
2. Window 2: Login as client2@vibe.com
3. Window 1: Open chat, go to Active Users
4. Window 1: Verify client2 is in the list with green dot
5. Window 2: Close the chat window (click ×)
6. Window 1: Keep Active Users tab open
7. Wait a few seconds
8. Window 2: Reopen chat window
9. Window 1: Should see client2 reappear in active users

**Expected Results**:
- ✅ Users appear in active list when chat is open
- ✅ Green dot indicates online status
- ✅ Real-time presence updates work

### Scenario 4: Multiple Conversations

**Goal**: Test managing multiple conversations

**Steps**:
1. Login as client1@vibe.com
2. Open chat
3. Start conversation with client2
4. Send message "Hello client2"
5. Click back button
6. Click Active Users tab
7. Start conversation with coach1
8. Send message "Hello coach"
9. Click back button
10. You should see both conversations in the list
11. Click on client2 conversation
12. Verify message history is preserved
13. Click back, then click coach1 conversation
14. Verify separate message history

**Expected Results**:
- ✅ Multiple conversations maintained separately
- ✅ Each conversation shows last message
- ✅ Message history persists between views
- ✅ Back button returns to conversation list

### Scenario 5: Group Chat (API Test)

**Goal**: Test group conversation creation

**Steps**:
1. Login as client1@vibe.com
2. Get the user token from localStorage (browser console)
3. Use API testing tool (Postman, curl, or browser console):

```javascript
// In browser console (while logged in as client1)
const token = localStorage.getItem('token');
const response = await fetch('http://localhost:8000/api/v1/chat/conversations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    type: 'group',
    name: 'Fitness Squad',
    participant_ids: [2, 3, 4] // User IDs of coach1, coach2, etc.
  })
});
const data = await response.json();
console.log(data);
```

4. Refresh chat window
5. New group should appear in conversations
6. Send message to group
7. Login as one of the group members
8. Verify they see the group and message

**Expected Results**:
- ✅ Group conversation created successfully
- ✅ All participants can see the group
- ✅ Messages broadcast to all members

### Scenario 6: Message History Persistence

**Goal**: Verify messages are saved

**Steps**:
1. Login as client1@vibe.com
2. Start chat with client2
3. Send several messages
4. Close chat window (click ×)
5. Logout
6. Login again as client1@vibe.com
7. Open chat
8. Click on conversation with client2
9. Verify all previous messages are still there

**Expected Results**:
- ✅ All messages preserved after closing chat
- ✅ Messages persist after logout/login
- ✅ Messages in correct order with timestamps

### Scenario 7: Authorization Test

**Goal**: Verify users can't access others' conversations

**Steps**:
1. Login as client1@vibe.com
2. Create conversation with client2 (note the conversation ID)
3. Logout
4. Login as client3@vibe.com
5. Try to access client1's conversation via API:

```javascript
const token = localStorage.getItem('token');
const conversationId = 1; // ID from client1's conversation
const response = await fetch(`http://localhost:8000/api/v1/chat/conversations/${conversationId}`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
console.log(response.status); // Should be 403
```

**Expected Results**:
- ✅ 403 Forbidden error returned
- ✅ User cannot access other users' conversations
- ✅ Security working as intended

### Scenario 8: UI Responsiveness

**Goal**: Test responsive design

**Steps**:
1. Open chat on desktop browser
2. Resize browser to mobile width (< 768px)
3. Verify chat window adjusts to full width
4. Test all functionality on mobile view
5. Verify buttons are easily tappable
6. Check scrolling works smoothly

**Expected Results**:
- ✅ Chat window responsive to screen size
- ✅ All features work on mobile
- ✅ Touch targets appropriately sized
- ✅ No horizontal scrolling

### Scenario 9: Performance Test

**Goal**: Test with many messages

**Steps**:
1. Login as two different users
2. Open chat between them
3. Send 50+ messages rapidly
4. Verify chat scrolls smoothly
5. Check typing is responsive
6. Verify no lag in message delivery

**Expected Results**:
- ✅ Messages render quickly
- ✅ Scrolling remains smooth
- ✅ No memory leaks
- ✅ WebSocket connection stable

### Scenario 10: Error Handling

**Goal**: Test error scenarios

**Steps**:
1. Login as client1@vibe.com
2. Open chat
3. Open browser DevTools (F12)
4. Go to Network tab
5. Set throttling to "Offline"
6. Try to send a message
7. Set back to "Online"
8. Verify message sends when back online

**Expected Results**:
- ✅ Graceful handling of offline state
- ✅ Connection recovers when back online
- ✅ Messages queue and send when possible
- ✅ User informed of connection status

## Automated Testing

### Backend Tests

Run all chat tests:
```bash
cd backend
pytest tests/test_chat.py -v
```

Run with coverage:
```bash
pytest tests/test_chat.py --cov=app.api.v1.chat --cov-report=html
```

### Individual Test Commands

Test conversation creation:
```bash
pytest tests/test_chat.py::test_create_direct_conversation -v
```

Test authorization:
```bash
pytest tests/test_chat.py::test_get_conversation_unauthorized -v
```

Test presence:
```bash
pytest tests/test_chat.py::test_get_active_users -v
```

## API Testing with curl

### Get Active Users
```bash
# First, login and get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"client1@vibe.com","password":"client1123"}' \
  | jq -r '.access_token')

# Then get active users
curl -X GET http://localhost:8000/api/v1/chat/active-users \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Create Conversation
```bash
curl -X POST http://localhost:8000/api/v1/chat/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "type": "direct",
    "participant_ids": [2]
  }' | jq
```

### Get Conversations
```bash
curl -X GET http://localhost:8000/api/v1/chat/conversations \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Get Specific Conversation
```bash
curl -X GET http://localhost:8000/api/v1/chat/conversations/1 \
  -H "Authorization: Bearer $TOKEN" | jq
```

## WebSocket Testing

Test WebSocket connection with wscat:

```bash
# Install wscat
npm install -g wscat

# Connect (replace TOKEN with actual JWT)
wscat -c "ws://localhost:8000/api/v1/chat/ws/YOUR_JWT_TOKEN_HERE"

# Once connected, send a message
{"type":"message","conversation_id":1,"content":"Test message"}

# Send typing indicator
{"type":"typing","conversation_id":1}

# Mark message as read
{"type":"read","message_id":1}
```

## Browser Console Testing

### Check WebSocket Connection
```javascript
// Open chat, then in console:
console.log('WS State:', window.ws?.readyState);
// 0 = CONNECTING, 1 = OPEN, 2 = CLOSING, 3 = CLOSED
```

### Manually Send Message
```javascript
// Get the WebSocket instance (hack for testing)
const ws = window.ws; // May need to expose this
ws.send(JSON.stringify({
  type: 'message',
  conversation_id: 1,
  content: 'Test from console'
}));
```

### Check Active Conversations
```javascript
const token = localStorage.getItem('token');
fetch('http://localhost:8000/api/v1/chat/conversations', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(data => console.table(data));
```

## Common Issues & Solutions

### Issue: Chat button not appearing
**Solution**: Ensure user is authenticated. Check `isAuthenticated` in browser console.

### Issue: No active users showing
**Solution**: Open chat in another browser/user. Presence requires WebSocket connection.

### Issue: Messages not appearing
**Solution**: 
1. Check browser console for errors
2. Verify WebSocket connection is open
3. Check backend logs for errors

### Issue: "Conversation not found" error
**Solution**: Ensure you're a participant in that conversation. Check authorization.

### Issue: WebSocket connection fails
**Solution**:
1. Verify backend is running
2. Check REACT_APP_WS_URL is correct
3. Ensure token is valid

## Test Checklist

Before marking feature as complete, verify:

- [ ] Direct messaging works between two users
- [ ] Group chat can be created and used
- [ ] Typing indicators show in real-time
- [ ] Online presence updates correctly
- [ ] Messages persist after logout
- [ ] Multiple conversations work independently
- [ ] Authorization prevents unauthorized access
- [ ] Mobile responsive design works
- [ ] Performance is good with many messages
- [ ] Error handling is graceful
- [ ] All backend tests pass
- [ ] No console errors in browser
- [ ] WebSocket connection is stable

## Load Testing

For production readiness, consider:

1. **Concurrent Users**: Test with 10+ simultaneous users
2. **Message Volume**: Send 100+ messages rapidly
3. **Connection Stability**: Keep WebSocket open for 1+ hour
4. **Memory Leaks**: Monitor browser memory usage
5. **Database Performance**: Check query times under load

## Reporting Issues

When reporting issues, include:
1. Steps to reproduce
2. Expected vs actual behavior
3. Browser and version
4. Backend logs (if applicable)
5. Frontend console errors (if any)
6. Screenshots or video

---

**Happy Testing!** 🎉

For more information, see:
- [CHAT_FEATURE.md](CHAT_FEATURE.md) - Complete documentation
- [CHAT_UI_GUIDE.md](CHAT_UI_GUIDE.md) - UI component guide
- [DELIVERY_SUMMARY.md](DELIVERY_SUMMARY.md) - Implementation summary
