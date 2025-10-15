# Chat Feature - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          VIBE FITNESS PLATFORM                          │
│                         Chat Feature Architecture                        │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────┐         ┌──────────────────────────────┐
│         FRONTEND                 │         │         BACKEND              │
│                                  │         │                              │
│  ┌────────────────────────────┐  │         │  ┌────────────────────────┐ │
│  │    ChatBox Component       │  │         │  │   FastAPI Application  │ │
│  │  - Conversations View      │  │         │  │   - Chat Router        │ │
│  │  - Active Users View       │  │         │  │   - WebSocket Handler  │ │
│  │  - Chat View with Messages │  │         │  │   - Connection Mgr     │ │
│  └──────────┬─────────────────┘  │         │  └──────┬─────────────────┘ │
│             │                     │         │         │                   │
│  ┌──────────▼─────────────────┐  │         │  ┌──────▼─────────────────┐ │
│  │    Chat Service            │  │         │  │   Chat API Endpoints   │ │
│  │  - REST API calls          │◄─┼────────►│  │   - POST conversations │ │
│  │  - WebSocket connection    │  │   HTTP  │  │   - GET conversations  │ │
│  │  - Message handling        │◄─┼────────►│  │   - GET active-users   │ │
│  └────────────────────────────┘  │   WS    │  │   - GET presence       │ │
│                                  │         │  └──────┬─────────────────┘ │
│  React Components                │         │         │                   │
│  - useState for messages         │         │  ┌──────▼─────────────────┐ │
│  - useEffect for WebSocket       │         │  │   Database Models      │ │
│  - Context for auth              │         │  │   - Conversation       │ │
└──────────────────────────────────┘         │  │   - Message            │ │
                                             │  │   - UserPresence       │ │
                                             │  └──────┬─────────────────┘ │
                                             │         │                   │
                                             │  ┌──────▼─────────────────┐ │
                                             │  │   PostgreSQL Database  │ │
                                             │  │   - conversations      │ │
                                             │  │   - messages           │ │
                                             │  │   - user_presence      │ │
                                             │  │   - conversation_      │ │
                                             │  │     participants       │ │
                                             │  └────────────────────────┘ │
                                             └──────────────────────────────┘
```

## Data Flow Diagrams

### 1. Sending a Message

```
User Types Message → ChatBox Component → WebSocket Connection
                                               ↓
                                    Backend Connection Manager
                                               ↓
                                    Create Message in Database
                                               ↓
                                    Broadcast to Participants
                                               ↓
                              WebSocket → ChatBox Components (all participants)
                                               ↓
                                    Update UI with New Message
```

### 2. Starting a Direct Chat

```
User → Click Active User → Chat Service → POST /conversations
                                                ↓
                                    Check if conversation exists
                                                ↓
                                    Create/Return conversation
                                                ↓
                                    GET conversation with messages
                                                ↓
                                    Display chat view with history
```

### 3. Real-Time Presence Updates

```
User Opens Chat → WebSocket Connect → Update UserPresence (online=true)
                                               ↓
                                    Broadcast presence update
                                               ↓
                              All Connected Users Receive Update
                                               ↓
                                    Update Active Users List
```

## Database Schema

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DATABASE RELATIONSHIPS                           │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────────┐
│     users        │         │   conversations      │
├──────────────────┤         ├──────────────────────┤
│ id (PK)          │────┐    │ id (PK)              │
│ email            │    │    │ type                 │
│ full_name        │    │    │ name                 │
│ role             │    │    │ created_by_id (FK)   │───┐
│ ...              │    │    │ created_at           │   │
└──────────────────┘    │    │ updated_at           │   │
         │              │    └──────────────────────┘   │
         │              │              │                 │
         │              │              │                 │
         │              └──────────────┼─────────────────┘
         │                             │
         │              ┌──────────────▼────────────────────┐
         │              │  conversation_participants        │
         │              ├───────────────────────────────────┤
         │              │ conversation_id (FK, PK)          │
         └──────────────┤ user_id (FK, PK)                  │
                        └───────────────────────────────────┘
         │
         │              ┌──────────────────────┐
         └──────────────┤   messages           │
                        ├──────────────────────┤
                        │ id (PK)              │
                        │ conversation_id (FK) │
                        │ sender_id (FK)       │
                        │ content              │
                        │ status               │
                        │ created_at           │
                        └──────────────────────┘

         │              ┌──────────────────────┐
         └──────────────┤   user_presence      │
                        ├──────────────────────┤
                        │ id (PK)              │
                        │ user_id (FK, unique) │
                        │ is_online            │
                        │ last_seen            │
                        └──────────────────────┘
```

## WebSocket Message Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WEBSOCKET MESSAGE TYPES                              │
└─────────────────────────────────────────────────────────────────────────┘

CLIENT → SERVER:
┌────────────────────────────────────────────────────────────────┐
│ Message Type: "message"                                        │
│ {                                                              │
│   "type": "message",                                           │
│   "conversation_id": 1,                                        │
│   "content": "Hello!"                                          │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘
                              ↓
                    Store in Database
                              ↓
SERVER → CLIENTS (in conversation):
┌────────────────────────────────────────────────────────────────┐
│ {                                                              │
│   "type": "message",                                           │
│   "message": {                                                 │
│     "id": 123,                                                 │
│     "conversation_id": 1,                                      │
│     "sender_id": 5,                                            │
│     "content": "Hello!",                                       │
│     "status": "sent",                                          │
│     "created_at": "2025-10-15T12:00:00"                        │
│   }                                                            │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘

CLIENT → SERVER:
┌────────────────────────────────────────────────────────────────┐
│ Message Type: "typing"                                         │
│ {                                                              │
│   "type": "typing",                                            │
│   "conversation_id": 1                                         │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘
                              ↓
SERVER → CLIENTS (in conversation):
┌────────────────────────────────────────────────────────────────┐
│ {                                                              │
│   "type": "typing",                                            │
│   "conversation_id": 1,                                        │
│   "user_id": 5                                                 │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘

ON CONNECT/DISCONNECT:
┌────────────────────────────────────────────────────────────────┐
│ SERVER → ALL CLIENTS:                                          │
│ {                                                              │
│   "type": "presence",                                          │
│   "user_id": 5,                                                │
│   "is_online": true/false                                      │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

```
App
 └── AuthProvider
      └── ChatBox (floating, always rendered when authenticated)
           ├── WebSocket Connection
           ├── State Management
           │    ├── conversations
           │    ├── messages
           │    ├── activeUsers
           │    └── typing indicators
           │
           └── Views (conditional rendering)
                ├── Conversations List View
                │    └── ConversationItem (×N)
                │         ├── conversation name
                │         └── last message preview
                │
                ├── Active Users View
                │    └── UserItem (×N)
                │         ├── online indicator
                │         ├── user name
                │         └── user role
                │
                └── Chat View
                     ├── Message List (scrollable)
                     │    └── MessageBubble (×N)
                     │         ├── content
                     │         ├── timestamp
                     │         └── status
                     │
                     ├── Typing Indicator (conditional)
                     │
                     └── Message Input
                          ├── text input
                          └── send button
```

## Security Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       AUTHENTICATION FLOW                               │
└─────────────────────────────────────────────────────────────────────────┘

1. User Login
   ├── POST /api/v1/auth/login
   └── Receive JWT Token → Store in localStorage

2. Open Chat
   ├── Retrieve token from localStorage
   └── Include in Authorization header

3. WebSocket Connection
   ├── ws://localhost:8000/api/v1/chat/ws/{token}
   ├── Backend validates token
   ├── Extract user_id from token
   └── Accept or reject connection

4. API Requests
   ├── Include Authorization: Bearer {token}
   ├── Middleware validates token
   ├── Extract current_user
   └── Check permissions

5. Authorization Checks
   ├── Only conversation participants can access messages
   ├── Users can only see their own conversations
   └── All chat endpoints require authentication
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PRODUCTION DEPLOYMENT                           │
└─────────────────────────────────────────────────────────────────────────┘

                          ┌─────────────────┐
                          │   Load Balancer │
                          └────────┬────────┘
                                   │
              ┌────────────────────┴────────────────────┐
              │                                         │
    ┌─────────▼─────────┐                   ┌─────────▼─────────┐
    │  Frontend Server  │                   │  Backend Instance │
    │  (Nginx + React)  │                   │  (FastAPI + WS)   │
    └───────────────────┘                   └─────────┬─────────┘
                                                      │
                                            ┌─────────▼─────────┐
                                            │  PostgreSQL DB    │
                                            │  - Persistence    │
                                            │  - Replication    │
                                            └───────────────────┘

    For Multi-Instance (Scaling):
    ┌───────────────────────────────────────────────────────────┐
    │  Redis (Optional)                                         │
    │  - WebSocket connection state sharing                     │
    │  - Message queue for cross-instance communication         │
    └───────────────────────────────────────────────────────────┘
```

## Performance Considerations

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        OPTIMIZATION POINTS                              │
└─────────────────────────────────────────────────────────────────────────┘

DATABASE:
├── Indexes on foreign keys (conversation_id, sender_id, user_id)
├── Eager loading with selectinload (prevent N+1)
├── Efficient queries with proper JOINs
└── Pagination ready (for future large message volumes)

WEBSOCKET:
├── Single connection per user
├── Targeted message broadcasting (only to participants)
├── Automatic cleanup on disconnect
└── Connection pooling

FRONTEND:
├── React key-based rendering (efficient updates)
├── Ref-based scrolling (no re-renders)
├── Debounced typing indicators
└── Conditional rendering (only show active view)

NETWORK:
├── WebSocket for real-time (no polling)
├── REST for initial data load
├── Minimal payload size
└── Compression enabled (future)
```

## Monitoring & Debugging

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     MONITORING POINTS                                   │
└─────────────────────────────────────────────────────────────────────────┘

Backend Logs:
├── WebSocket connections/disconnections
├── Message send/receive events
├── Database query performance
└── Error traces with stack

Frontend Console:
├── WebSocket connection status
├── Message send/receive events
├── State updates (development mode)
└── Error logging

Database Metrics:
├── Active conversations count
├── Messages per conversation
├── Online users count
└── Query performance

Application Metrics:
├── Active WebSocket connections
├── Messages per second
├── Average response time
└── Error rate
```

## Future Enhancements Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PLANNED ENHANCEMENTS                                │
└─────────────────────────────────────────────────────────────────────────┘

Media Support:
├── File upload endpoint
├── S3/CDN integration
├── Thumbnail generation
└── Media gallery in chat

Push Notifications:
├── Service Worker registration
├── Push notification subscription
├── Backend notification service
└── Notification preferences

Advanced Features:
├── Message search (ElasticSearch integration)
├── Voice messages (WebRTC)
├── Video calls (WebRTC)
└── Message encryption (E2E)

Scalability:
├── Redis for WebSocket state
├── Message queue (RabbitMQ/Redis)
├── Read replicas for database
└── CDN for media files
```

## Legend

```
Symbols Used:
─────  Connection/Flow
│      Vertical connection
├──    Branch connection
└──    Terminal connection
◄─►    Bidirectional flow
▼      Downward flow
(PK)   Primary Key
(FK)   Foreign Key
×N     Multiple instances
```
