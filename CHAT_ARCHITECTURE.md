# Chat Feature Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌──────────────────┐   │
│  │ Chat Page     │  │ ChatContext   │  │ Chat Components  │   │
│  │               │  │               │  │                  │   │
│  │ - Main UI     │  │ - WebSocket   │  │ - ConversationList│  │
│  │ - State Mgmt  │  │   Manager     │  │ - ChatWindow     │   │
│  │ - User Input  │  │ - Message     │  │ - MessageBubble  │   │
│  │               │  │   Handler     │  │ - Modal          │   │
│  └───────┬───────┘  └───────┬───────┘  └──────────────────┘   │
│          │                  │                                   │
│          └──────────────────┴────────────┐                     │
│                                           │                     │
└───────────────────────────────────────────┼─────────────────────┘
                                            │
                                            │ HTTP/WebSocket
                                            │
┌───────────────────────────────────────────┼─────────────────────┐
│                         Backend (FastAPI) │                     │
├───────────────────────────────────────────┼─────────────────────┤
│                                           │                     │
│  ┌───────────────┐                       │                     │
│  │ Chat Router   │◄──────────────────────┘                     │
│  │               │                                              │
│  │ REST Endpoints:                                              │
│  │ - POST /conversations                                        │
│  │ - GET  /conversations                                        │
│  │ - GET  /conversations/{id}                                   │
│  │ - POST /conversations/{id}/messages                          │
│  │ - PATCH /messages/{id}                                       │
│  │ - DELETE /messages/{id}                                      │
│  │                                                              │
│  │ WebSocket:                                                   │
│  │ - WS /ws?token={jwt}                                         │
│  └───────┬───────┘                                              │
│          │                                                      │
│          ├──────────┬──────────────┬──────────────┐            │
│          │          │              │              │            │
│  ┌───────▼───────┐  │  ┌───────────▼─────┐  ┌────▼─────────┐  │
│  │ WebSocket     │  │  │ Chat Schemas    │  │ Auth/JWT     │  │
│  │ Manager       │  │  │                 │  │              │  │
│  │               │  │  │ - MessageCreate │  │ - Verify     │  │
│  │ - Connections │  │  │ - ConversationX │  │   Token      │  │
│  │ - Broadcast   │  │  │ - UserStatus    │  │ - Get User   │  │
│  │ - User Status │  │  │                 │  │              │  │
│  └───────────────┘  │  └─────────────────┘  └──────────────┘  │
│                     │                                           │
│                     │                                           │
│             ┌───────▼────────┐                                  │
│             │ Chat Models    │                                  │
│             │                │                                  │
│             │ - Conversation │                                  │
│             │ - Participant  │                                  │
│             │ - Message      │                                  │
│             └───────┬────────┘                                  │
│                     │                                           │
└─────────────────────┼───────────────────────────────────────────┘
                      │
                      │ SQLAlchemy (async)
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                      PostgreSQL Database                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐  │
│  │ conversations    │  │ conversation_    │  │ messages    │  │
│  │                  │  │ participants     │  │             │  │
│  │ - id            │  │                  │  │ - id        │  │
│  │ - name          │  │ - id             │  │ - conv_id   │  │
│  │ - type          │  │ - conv_id        │  │ - sender_id │  │
│  │ - is_active     │  │ - user_id        │  │ - content   │  │
│  │ - created_at    │  │ - is_admin       │  │ - is_read   │  │
│  │ - updated_at    │  │ - last_read_at   │  │ - is_edited │  │
│  │                 │  │ - created_at     │  │ - created_at│  │
│  └──────────────────┘  └──────────────────┘  └─────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Communication Flow

### 1. Initial Connection

```
User Browser                Frontend App              Backend Server              Database
     │                          │                          │                         │
     │    Open Chat Page        │                          │                         │
     ├─────────────────────────►│                          │                         │
     │                          │   WebSocket Connect      │                         │
     │                          │   ws://api/chat/ws       │                         │
     │                          ├─────────────────────────►│                         │
     │                          │                          │   Verify JWT Token      │
     │                          │                          ├────────────────────────►│
     │                          │                          │◄────────────────────────┤
     │                          │   Connection Established │                         │
     │                          │◄─────────────────────────┤                         │
     │    Show "Connected"      │                          │                         │
     │◄─────────────────────────┤                          │                         │
     │                          │   GET /conversations     │                         │
     │                          ├─────────────────────────►│   Query DB             │
     │                          │                          ├────────────────────────►│
     │                          │                          │◄────────────────────────┤
     │    Display Conversations │   Conversation List      │                         │
     │◄─────────────────────────┤◄─────────────────────────┤                         │
```

### 2. Sending a Message

```
User Browser                Frontend App              Backend Server              Database
     │                          │                          │                         │
     │    Type & Send Message   │                          │                         │
     ├─────────────────────────►│                          │                         │
     │                          │   POST /conversations/   │                         │
     │                          │   1/messages             │                         │
     │                          ├─────────────────────────►│   INSERT message       │
     │                          │                          ├────────────────────────►│
     │                          │                          │◄────────────────────────┤
     │                          │   Message Created        │                         │
     │                          │◄─────────────────────────┤                         │
     │    Message Displayed     │                          │                         │
     │◄─────────────────────────┤                          │   Broadcast via WS      │
     │                          │                          ├────────────────┐        │
     │                          │                          │                │        │
     │                          │   WS: New Message        │◄───────────────┘        │
Other Users◄──────────────────┤◄─────────────────────────┤                         │
```

### 3. Real-time Typing Indicator

```
User Browser                Frontend App              Backend Server           Other Users
     │                          │                          │                         │
     │    Start Typing          │                          │                         │
     ├─────────────────────────►│   WS: typing event       │                         │
     │                          ├─────────────────────────►│                         │
     │                          │                          │   Broadcast to          │
     │                          │                          │   conversation          │
     │                          │                          ├────────────────────────►│
     │                          │                          │   "User is typing..."   │
     │                          │                          │                         │
     │    Stop Typing (2s)      │                          │                         │
     ├─────────────────────────►│   WS: stop typing        │                         │
     │                          ├─────────────────────────►│                         │
     │                          │                          │   Broadcast             │
     │                          │                          ├────────────────────────►│
     │                          │                          │   Hide indicator        │
```

### 4. Read Receipts

```
User Browser                Frontend App              Backend Server              Database
     │                          │                          │                         │
     │    Open Conversation     │                          │                         │
     ├─────────────────────────►│   GET /conversations/1   │                         │
     │                          ├─────────────────────────►│   Query messages       │
     │                          │                          ├────────────────────────►│
     │                          │                          │◄────────────────────────┤
     │    Display Messages      │   Messages + Metadata    │                         │
     │◄─────────────────────────┤◄─────────────────────────┤                         │
     │                          │                          │                         │
     │                          │   WS: read_receipt       │                         │
     │                          ├─────────────────────────►│   UPDATE messages      │
     │                          │                          │   SET is_read=true     │
     │                          │                          ├────────────────────────►│
     │                          │                          │◄────────────────────────┤
     │                          │                          │   Broadcast to sender  │
     │                          │                          ├────────────────────────►│
Sender◄──────────────────────┤◄─────────────────────────┤   Show checkmark       │
```

## Component Interaction

### Frontend Components

```
Chat.js (Main Page)
  │
  ├─► ChatContext (WebSocket Manager)
  │     │
  │     ├─► Connect to WebSocket
  │     ├─► Handle incoming messages
  │     ├─► Manage connection state
  │     └─► Send real-time events
  │
  ├─► ConversationList
  │     │
  │     ├─► Display conversations
  │     ├─► Show unread counts
  │     ├─► Show online indicators
  │     └─► Handle selection
  │
  └─► ChatWindow
        │
        ├─► MessageBubble (multiple)
        │     └─► Display message with actions
        │
        ├─► Message Input
        │     ├─► Send typing indicators
        │     └─► Submit messages
        │
        └─► NewConversationModal
              └─► Create new conversations
```

### Backend Components

```
main.py
  │
  └─► Include chat router

chat.py (Router)
  │
  ├─► REST Endpoints
  │     ├─► Conversation CRUD
  │     ├─► Message CRUD
  │     └─► Participant management
  │
  └─► WebSocket Endpoint
        │
        └─► websocket_endpoint()
              │
              ├─► Authenticate user
              ├─► manager.connect()
              ├─► Listen for messages
              └─► manager.disconnect()

websocket.py (Manager)
  │
  ├─► active_connections: Dict[user_id, Set[WebSocket]]
  ├─► conversation_users: Dict[conv_id, Set[user_id]]
  └─► user_activity: Dict[user_id, datetime]
  │
  ├─► connect(websocket, user_id)
  ├─► disconnect(websocket, user_id)
  ├─► send_personal_message(message, user_id)
  ├─► send_to_conversation(message, conv_id)
  └─► broadcast_user_status(user_id, is_online)
```

## Data Models

### Database Relationships

```
User ─────┬────────────► WorkoutLog
          ├────────────► DietLog
          ├────────────► WorkoutPlan
          ├────────────► DietPlan
          ├────────────► Booking (as coach)
          ├────────────► Booking (as client)
          ├────────────► Message (as sender)
          └────────────► ConversationParticipant
                            │
                            │
Conversation ──┬───────────┘
               ├───────────► ConversationParticipant (many)
               └───────────► Message (many)
```

### Conversation Types

```
ConversationType (Enum)
  ├─► DIRECT
  │     └─► Exactly 2 participants
  │         └─► No name required
  │
  └─► GROUP
        └─► 2+ participants
            └─► Name required
            └─► Admin permissions
```

## State Management

### Frontend State (ChatContext)

```javascript
{
  // WebSocket connection
  ws: WebSocket | null,
  isConnected: boolean,
  
  // Messages
  messages: Message[],
  
  // Active users
  activeUsers: Set<number>,
  
  // Typing indicators
  typingUsers: {
    [conversationId]: {
      [userId]: boolean
    }
  },
  
  // Unread counts
  unreadCounts: {
    [conversationId]: number
  }
}
```

### Backend State (WebSocket Manager)

```python
{
  # Active WebSocket connections
  active_connections: {
    user_id: Set[WebSocket]
  },
  
  # Users in each conversation
  conversation_users: {
    conversation_id: Set[user_id]
  },
  
  # Last activity timestamp
  user_activity: {
    user_id: datetime
  }
}
```

## Security Flow

### Authentication

```
1. User logs in → Receives JWT token
2. Token stored in localStorage
3. HTTP requests include: Authorization: Bearer {token}
4. WebSocket connects with: ws://api/chat/ws?token={token}
5. Server verifies token before accepting connection
6. Expired tokens are rejected
```

### Authorization

```
┌─────────────────────────────────────────────┐
│ User attempts to:                           │
│ - Send message                              │
│ - View conversation                         │
│ - Edit/delete message                       │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│ Server checks:                               │
│ 1. Is user authenticated? (JWT valid)       │
│ 2. Is user participant in conversation?     │
│ 3. Is user the message sender? (for edit)   │
│ 4. Is user admin? (for group management)    │
└──────────────┬───────────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
    Allow         Deny
        │             │
        ▼             ▼
  Process      Return 403
  Request      Forbidden
```

## Performance Considerations

### Message Pagination

```
┌─────────────────────────────────────────┐
│ GET /conversations/1?limit=50&offset=0  │
│                                         │
│ Returns:                                │
│ - 50 most recent messages               │
│ - Ordered by created_at DESC            │
│                                         │
│ For older messages:                     │
│ - Increment offset: offset=50           │
│ - Load more on scroll                   │
└─────────────────────────────────────────┘
```

### WebSocket Optimization

```
┌───────────────────────────────────────────┐
│ Connection Management:                    │
│                                           │
│ - Each user can have multiple connections │
│   (multiple browser tabs)                 │
│                                           │
│ - Messages sent to all user connections   │
│                                           │
│ - Dead connections cleaned up             │
│   automatically                           │
│                                           │
│ - Reconnection with exponential backoff   │
└───────────────────────────────────────────┘
```

## Scalability Strategy

### Future: Redis for Multi-instance Deployment

```
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Backend      │   │  Backend      │   │  Backend      │
│  Instance 1   │   │  Instance 2   │   │  Instance 3   │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────▼───────┐
                    │     Redis     │
                    │   Pub/Sub     │
                    └───────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
│  Connected    │   │  Connected    │   │  Connected    │
│   Users       │   │   Users       │   │   Users       │
│   1-1000      │   │  1001-2000    │   │  2001-3000    │
└───────────────┘   └───────────────┘   └───────────────┘
```

## Monitoring & Debugging

### Key Metrics to Track

```
┌──────────────────────────────────────┐
│ WebSocket Metrics:                   │
│ - Active connections                 │
│ - Connection duration                │
│ - Messages per second                │
│ - Reconnection rate                  │
│                                      │
│ Database Metrics:                    │
│ - Query response time                │
│ - Number of active conversations     │
│ - Total messages                     │
│ - Average conversation size          │
│                                      │
│ Application Metrics:                 │
│ - CPU usage                          │
│ - Memory usage                       │
│ - Network bandwidth                  │
│ - Error rate                         │
└──────────────────────────────────────┘
```

---

This architecture is designed for:
- ✅ Real-time performance
- ✅ Scalability
- ✅ Security
- ✅ Maintainability
- ✅ Extensibility
