# Testing the Chat Feature - Step-by-Step Guide

This document provides detailed instructions for manually testing the chat feature.

## Test Environment Setup

### Prerequisites
- Docker and Docker Compose installed
- Two browser windows or browsers (for testing between users)
- Alternatively: one browser window + one incognito window

### Setup Steps

1. **Start the application**:
   ```bash
   cd /path/to/vibe_project
   docker compose up -d
   docker compose exec backend alembic upgrade head
   ```

2. **Wait for services to start** (30-60 seconds)

3. **Verify services are running**:
   ```bash
   docker compose ps
   # All services should show as "healthy" or "running"
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/docs

## Test Cases

### Test Case 1: User Registration and Login

**Objective**: Create test users for chat testing

**Steps**:

1. Open http://localhost:3000/signup
2. Create User 1:
   - Email: `user1@test.com`
   - Password: `Test1234!`
   - Full Name: `Test User One`
   - Role: Client
3. Click "Sign Up"
4. Login with User 1 credentials
5. ✅ **Expected**: Successful login, redirected to dashboard

6. Open a second browser (or incognito window)
7. Go to http://localhost:3000/signup
8. Create User 2:
   - Email: `user2@test.com`
   - Password: `Test1234!`
   - Full Name: `Test User Two`
   - Role: Client
9. Click "Sign Up"
10. Login with User 2 credentials
11. ✅ **Expected**: Successful login, redirected to dashboard

**Screenshot Needed**: 
- [ ] Signup page
- [ ] Successful login dashboard

---

### Test Case 2: Chat Button Visibility

**Objective**: Verify chat button appears for authenticated users

**Steps**:

1. With User 1 logged in
2. Look at bottom-right corner of the screen
3. ✅ **Expected**: See a green button labeled "💬 Chat"
4. Check button position: Should be to the left of "💬 Feedback" button
5. ✅ **Expected**: Button has online count badge if any users are online

**Screenshot Needed**:
- [ ] Chat button visible in bottom-right corner

---

### Test Case 3: Opening Chat Modal

**Objective**: Verify chat modal opens correctly

**Steps**:

1. Click the "💬 Chat" button
2. ✅ **Expected**: Modal appears centered on screen
3. ✅ **Expected**: Modal has green header with "💬 Chats"
4. ✅ **Expected**: Two tabs visible: "💬 Chats" and "👥 Online"
5. ✅ **Expected**: Close button (×) in top-right corner
6. Click anywhere outside the modal
7. ✅ **Expected**: Modal stays open (only closes via × button or back)

**Screenshot Needed**:
- [ ] Chat modal open showing tabs

---

### Test Case 4: Online Users Detection

**Objective**: Verify both users show as online

**Steps**:

1. In Browser 1 (User 1):
   - Click "💬 Chat" button
   - Click "👥 Online" tab
   - ✅ **Expected**: See "Test User Two" in the list
   - ✅ **Expected**: Green pulsing dot next to the name
   - ✅ **Expected**: "Online" status shown

2. In Browser 2 (User 2):
   - Click "💬 Chat" button
   - Click "👥 Online" tab
   - ✅ **Expected**: See "Test User One" in the list
   - ✅ **Expected**: Green pulsing dot next to the name

**Screenshot Needed**:
- [ ] Online users list showing other user

---

### Test Case 5: Starting a Direct Chat

**Objective**: Initiate a 1:1 conversation

**Steps**:

1. In Browser 1 (User 1):
   - On "👥 Online" tab
   - Click on "Test User Two"
   - ✅ **Expected**: View changes to chat conversation
   - ✅ **Expected**: Header shows "Direct Chat" or other user's name
   - ✅ **Expected**: "← Back" button visible in header
   - ✅ **Expected**: Empty state message: "No messages yet"
   - ✅ **Expected**: Message input at bottom

**Screenshot Needed**:
- [ ] Empty chat conversation view

---

### Test Case 6: Sending a Message

**Objective**: Send a message and verify it appears correctly

**Steps**:

1. In Browser 1 (User 1):
   - Type "Hello from User 1!" in the message input
   - Press Enter (or click the send button ➤)
   - ✅ **Expected**: Message appears immediately
   - ✅ **Expected**: Message aligned to right side
   - ✅ **Expected**: Green background bubble (WhatsApp style)
   - ✅ **Expected**: Timestamp shown below message
   - ✅ **Expected**: Input field cleared after sending

**Screenshot Needed**:
- [ ] Sent message appearing on right side with green bubble

---

### Test Case 7: Real-time Message Delivery

**Objective**: Verify messages appear instantly in recipient's chat

**Steps**:

1. Keep Browser 1 (User 1) chat window open with message sent

2. In Browser 2 (User 2):
   - If chat is closed, click "💬 Chat" button
   - ✅ **Expected**: New chat room appears in "💬 Chats" list
   - Click on the chat room with User 1
   - ✅ **Expected**: Message "Hello from User 1!" visible
   - ✅ **Expected**: Message aligned to left side
   - ✅ **Expected**: White background bubble
   - ✅ **Expected**: "Test User One" name shown above message
   - ✅ **Expected**: Timestamp shown

**Screenshot Needed**:
- [ ] Received message appearing on left side with white bubble
- [ ] Chat room appearing in chats list

---

### Test Case 8: Two-way Conversation

**Objective**: Test bidirectional messaging

**Steps**:

1. In Browser 2 (User 2):
   - Type "Hi! How are you?"
   - Press Enter
   - ✅ **Expected**: Message appears on right side (green)

2. In Browser 1 (User 1):
   - ✅ **Expected**: Message appears instantly on left side (white)
   - ✅ **Expected**: Shows "Test User Two" as sender

3. In Browser 1 (User 1):
   - Send: "I'm great! Ready for our workout?"

4. In Browser 2 (User 2):
   - ✅ **Expected**: Message appears instantly
   - Send: "Yes! Let's do it!"

5. Verify both browsers show the complete conversation

**Screenshot Needed**:
- [ ] Full conversation showing multiple messages from both users

---

### Test Case 9: Chat History Persistence

**Objective**: Verify messages persist after browser refresh

**Steps**:

1. In Browser 1 (User 1):
   - Note the messages in the chat
   - Refresh the browser (F5 or Ctrl+R)
   - Wait for page to reload
   - Click "💬 Chat" button
   - ✅ **Expected**: Chat room still visible in "💬 Chats" list
   - ✅ **Expected**: Last message preview shown
   - Click on the chat room
   - ✅ **Expected**: All previous messages still visible
   - ✅ **Expected**: Messages in correct order

**Screenshot Needed**:
- [ ] Chat history after refresh

---

### Test Case 10: Multiple Chat Rooms

**Objective**: Test managing multiple conversations

**Steps**:

1. Create a third user (User 3):
   - Open third browser/incognito window
   - Register as `user3@test.com`
   - Login

2. In Browser 1 (User 1):
   - Go to "👥 Online" tab
   - ✅ **Expected**: See both User 2 and User 3 online
   - Click on User 3
   - Send: "Hi User 3!"

3. Verify User 1 now has 2 chat rooms:
   - Click "← Back"
   - ✅ **Expected**: See "💬 Chats" list with 2 rooms
   - ✅ **Expected**: Both rooms show last message

4. Switch between chats:
   - Click first chat room
   - Verify messages with User 2
   - Click "← Back"
   - Click second chat room
   - Verify messages with User 3

**Screenshot Needed**:
- [ ] Multiple chat rooms in the list

---

### Test Case 11: Online/Offline Status

**Objective**: Test presence indicators

**Steps**:

1. In Browser 2 (User 2):
   - Close the browser completely (or logout)

2. In Browser 1 (User 1):
   - Click "👥 Online" tab
   - Wait 5-10 seconds
   - ✅ **Expected**: User 2 disappears from online list
   - OR ✅ **Expected**: User 2 shown as offline

3. Open Browser 2 again:
   - Login as User 2

4. In Browser 1:
   - ✅ **Expected**: User 2 reappears in online list
   - ✅ **Expected**: Green dot indicator present

**Screenshot Needed**:
- [ ] Online status indicator (green dot)

---

### Test Case 12: Mobile Responsiveness

**Objective**: Test chat UI on mobile viewport

**Steps**:

1. In Browser 1:
   - Open browser DevTools (F12)
   - Enable device toolbar (Ctrl+Shift+M)
   - Select iPhone or Android device
   - ✅ **Expected**: Chat button still visible
   - Click chat button
   - ✅ **Expected**: Modal fills entire screen
   - ✅ **Expected**: All elements properly sized for mobile
   - Send a message
   - ✅ **Expected**: Keyboard doesn't cover input
   - ✅ **Expected**: Messages properly formatted

**Screenshot Needed**:
- [ ] Mobile view of chat button
- [ ] Mobile view of chat conversation

---

### Test Case 13: Error Handling

**Objective**: Test behavior when connection is lost

**Steps**:

1. Open browser DevTools (F12)
2. Go to Network tab
3. Select "Offline" mode
4. Try sending a message
5. ✅ **Expected**: Error message appears
6. Disable offline mode
7. ✅ **Expected**: Connection restored
8. Send message again
9. ✅ **Expected**: Message sends successfully

**Screenshot Needed**:
- [ ] Error state when offline

---

### Test Case 14: Group Chat (API Only)

**Objective**: Test group chat via API

**Steps**:

1. Get User 1's auth token:
   - Open browser DevTools
   - Console tab
   - Type: `localStorage.getItem('token')`
   - Copy the token

2. Create group chat:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/chat/rooms" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Workout Buddies",
       "type": "group",
       "participant_ids": [USER2_ID, USER3_ID]
     }'
   ```

3. In Browser 1:
   - Refresh chat
   - ✅ **Expected**: See "Workout Buddies" in chat list
   - ✅ **Expected**: Group icon (👥) shown
   - Open the chat
   - Send a message

4. In Browser 2 and Browser 3:
   - ✅ **Expected**: Group chat appears
   - ✅ **Expected**: All users receive messages

**Screenshot Needed**:
- [ ] Group chat in the list
- [ ] Group chat conversation

---

### Test Case 15: Concurrent Users Stress Test

**Objective**: Test with multiple simultaneous users

**Steps**:

1. Have 3-5 users online simultaneously
2. All users open chat
3. Send messages from different users rapidly
4. ✅ **Expected**: All messages delivered
5. ✅ **Expected**: No message loss
6. ✅ **Expected**: Correct message order
7. ✅ **Expected**: No duplicate messages
8. ✅ **Expected**: UI remains responsive

**Screenshot Needed**:
- [ ] Multiple users in online list

---

## Performance Tests

### Test Case 16: Message Loading Performance

**Objective**: Verify performance with many messages

**Steps**:

1. Send 50+ messages between two users
2. Close and reopen chat
3. ✅ **Expected**: Messages load within 2 seconds
4. ✅ **Expected**: Smooth scrolling
5. ✅ **Expected**: No UI lag

---

### Test Case 17: WebSocket Reconnection

**Objective**: Test automatic reconnection

**Steps**:

1. Open chat and connect
2. Stop backend: `docker compose stop backend`
3. ✅ **Expected**: Connection lost indicator (check console)
4. Start backend: `docker compose start backend`
5. Wait 5-10 seconds
6. ✅ **Expected**: Reconnects automatically
7. Send a message
8. ✅ **Expected**: Message delivered successfully

---

## Security Tests

### Test Case 18: Authentication Required

**Objective**: Verify unauthenticated users cannot access chat

**Steps**:

1. Logout from the application
2. Try to access http://localhost:8000/api/v1/chat/rooms
3. ✅ **Expected**: 401 Unauthorized error
4. ✅ **Expected**: Chat button not visible when logged out

---

### Test Case 19: Authorization Check

**Objective**: Verify users can only access their own chats

**Steps**:

1. As User 1, note a chat room ID
2. Logout and login as User 3 (who is not in that chat)
3. Try to access the room via API:
   ```bash
   curl http://localhost:8000/api/v1/chat/rooms/{room_id} \
     -H "Authorization: Bearer USER3_TOKEN"
   ```
4. ✅ **Expected**: 403 Forbidden error

---

## Test Summary Checklist

After completing all tests, verify:

- [ ] Chat button visible and functional
- [ ] Modal opens and closes correctly
- [ ] Online users detected properly
- [ ] Direct chats work
- [ ] Messages send and receive in real-time
- [ ] Chat history persists
- [ ] Multiple chat rooms supported
- [ ] Online/offline status accurate
- [ ] Mobile responsive
- [ ] Error handling works
- [ ] Group chats functional (API)
- [ ] Performance acceptable
- [ ] Security measures in place
- [ ] All screenshots captured

## Screenshots to Provide

Create a folder with these screenshots:

1. `01_chat_button.png` - Floating chat button in corner
2. `02_chat_modal_rooms.png` - Chat rooms list view
3. `03_online_users.png` - Online users list
4. `04_empty_chat.png` - Empty chat state
5. `05_sent_message.png` - Message sent (right side, green)
6. `06_received_message.png` - Message received (left side, white)
7. `07_conversation.png` - Full conversation between users
8. `08_chat_history.png` - Chat persisted after refresh
9. `09_multiple_rooms.png` - Multiple chat rooms in list
10. `10_mobile_view.png` - Mobile responsive view
11. `11_group_chat.png` - Group chat (if tested)
12. `12_error_state.png` - Error handling

## Reporting Issues

If you find any issues during testing, please report with:

1. **Test Case Number**: Which test case failed
2. **Steps to Reproduce**: Detailed steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happened
5. **Screenshots**: Visual evidence
6. **Browser/Device**: Browser version and device type
7. **Console Errors**: Any JavaScript errors (F12 → Console)
8. **Network Errors**: Any API errors (F12 → Network)

## Success Criteria

The chat feature is considered successfully tested when:

- ✅ All 19 test cases pass
- ✅ All screenshots captured
- ✅ No blocking issues found
- ✅ Performance is acceptable
- ✅ Security measures verified
- ✅ Works on desktop and mobile
- ✅ Real-time messaging confirmed
- ✅ Data persistence verified
