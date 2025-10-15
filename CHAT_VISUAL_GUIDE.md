# Chat Feature Visual Guide

This document provides visual representations of the chat UI to help understand the feature.

## UI Components Overview

### 1. Floating Chat Button (Similar to Feedback Button)

Located in the bottom-right corner of the screen:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│                                                 │
│                   Page Content                  │
│                                                 │
│                                                 │
│                                                 │
│                                                 │
│                                                 │
│                                                 │
│                                            ┌─────────┐
│                                            │💬 Chat  │ ← Click here
│                                            │  (3)    │   Badge shows
│                                            └─────────┘   online count
└─────────────────────────────────────────────────┘
```

**Button Features**:
- Green gradient (WhatsApp-style)
- Shows online user count as badge
- Fixed position (stays visible while scrolling)
- Positioned left of the Feedback button

### 2. Chat Modal - Rooms View

When you click the Chat button:

```
┌───────────────────────────────────────────────────┐
│ 💬 Chats                                    ×     │ ← Header
├───────────────────────────────────────────────────┤
│ 💬 Chats         👥 Online (5)                   │ ← Tabs
├───────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────────────────────────────────────┐     │
│  │ 💬  John Doe                    2h ago  │     │ ← Room item
│  │     Hey, are you free today?            │     │
│  └─────────────────────────────────────────┘     │
│                                                   │
│  ┌─────────────────────────────────────────┐     │
│  │ 👥  Fitness Group              10m ago  │     │
│  │     Sarah: Let's meet at 5pm            │     │
│  └─────────────────────────────────────────┘     │
│                                                   │
│  ┌─────────────────────────────────────────┐     │
│  │ 💬  Mike Chen                 Yesterday │     │
│  │     Thanks for the tips!                │     │
│  └─────────────────────────────────────────┘     │
│                                                   │
└───────────────────────────────────────────────────┘
```

**Room Item Features**:
- Avatar icon (💬 for direct, 👥 for group)
- Contact/group name
- Last message preview (truncated)
- Timestamp
- Hover effect (slides right slightly)

### 3. Chat Modal - Online Users View

When you click the "👥 Online" tab:

```
┌───────────────────────────────────────────────────┐
│ 👥 Online Users                             ×     │
├───────────────────────────────────────────────────┤
│ 💬 Chats         👥 Online (5)                   │
├───────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────────────────────────────────────┐     │
│  │ 👤  Sarah Johnson                       │     │ ← Click to chat
│  │     ● Online                            │     │   Green dot
│  └─────────────────────────────────────────┘     │
│                                                   │
│  ┌─────────────────────────────────────────┐     │
│  │ 👤  Mike Chen                           │     │
│  │     ● Online                            │     │
│  └─────────────────────────────────────────┘     │
│                                                   │
│  ┌─────────────────────────────────────────┐     │
│  │ 👤  Emily Rodriguez                     │     │
│  │     ● Online                            │     │
│  └─────────────────────────────────────────┘     │
│                                                   │
└───────────────────────────────────────────────────┘
```

**Online User Features**:
- User avatar (👤)
- Full name
- Green pulsing dot (animated)
- Click to start direct chat
- Real-time updates (users appear/disappear as they go online/offline)

### 4. Chat Conversation View

When you open a chat room:

```
┌───────────────────────────────────────────────────┐
│ ← Back  John Doe                            ×     │ ← Header with back
├───────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────────────────────┐                    │ ← Other's message
│  │ John Doe                 │                    │   (left side)
│  │ Hey! How are you?        │                    │
│  │                   10:30am│                    │
│  └──────────────────────────┘                    │
│                                                   │
│                    ┌──────────────────────────┐  │ ← Your message
│                    │ I'm great, thanks!       │  │   (right side,
│                    │ How about you?           │  │    green bubble)
│                    │ 10:32am                  │  │
│                    └──────────────────────────┘  │
│                                                   │
│  ┌──────────────────────────┐                    │
│  │ John Doe                 │                    │
│  │ Doing well! Want to      │                    │
│  │ workout together?        │                    │
│  │                   10:35am│                    │
│  └──────────────────────────┘                    │
│                                                   │
│                    ┌──────────────────────────┐  │
│                    │ Sure! When works for you?│  │
│                    │ 10:36am                  │  │
│                    └──────────────────────────┘  │
│                                                   │
├───────────────────────────────────────────────────┤
│ [Type a message...]                          [➤] │ ← Input area
└───────────────────────────────────────────────────┘
```

**Message Features**:
- WhatsApp-style layout (your messages on right with green background)
- Other's messages on left (white background)
- Sender name shown for received messages
- Timestamp below each message
- "edited" label if message was edited
- Auto-scroll to bottom when new messages arrive
- Messages persist after refresh

### 5. Mobile Responsive View

On mobile devices (< 768px width):

```
┌─────────────────┐
│ ← Back John Doe×│
├─────────────────┤
│                 │
│ ┌─────────┐     │
│ │John Doe │     │
│ │Hey!     │     │
│ │  10:30am│     │
│ └─────────┘     │
│                 │
│      ┌────────┐ │
│      │Hi back!│ │
│      │ 10:31am│ │
│      └────────┘ │
│                 │
│ ┌─────────┐     │
│ │John Doe │     │
│ │What's up│     │
│ │  10:32am│     │
│ └─────────┘     │
│                 │
│      ┌────────┐ │
│      │Nothing!│ │
│      │ 10:33am│ │
│      └────────┘ │
│                 │
├─────────────────┤
│[Type...] [➤]   │
└─────────────────┘
```

**Mobile Features**:
- Full-screen modal
- Optimized touch targets
- Smooth scrolling
- Same functionality as desktop

## Color Scheme

The chat uses WhatsApp-inspired colors:

- **Primary Green**: `#25D366` (chat button, active elements)
- **Dark Green**: `#128C7E` (header gradient end)
- **Message Bubble (Own)**: `#DCF8C6` (light green)
- **Message Bubble (Other)**: `#FFFFFF` (white)
- **Background**: `#ECE5DD` (subtle beige, WhatsApp style)
- **Online Indicator**: `#25D366` (pulsing green dot)
- **Error Red**: `#ff6b6b` to `#ff4757` (gradient)

## Interactions

### Button Hover Effects

```
Normal:     [💬 Chat]
            │
            ↓ Hover
Hover:      [💬 Chat] ← Lifts up slightly
            with enhanced shadow
```

### Message Typing

```
1. User types: [Hello!_]
2. Press Enter or click ➤
3. Message sends immediately
4. Appears in other user's chat instantly
5. Clears input field
```

### Real-time Updates

```
User 1                          User 2
┌──────────┐                   ┌──────────┐
│          │ ─── Message ───>  │          │
│ Sends    │    (WebSocket)    │ Receives │
│ instantly│                   │ instantly│
└──────────┘                   └──────────┘
     ↑                              ↓
     │                              │
     └──────── Confirmation ────────┘
```

### Presence Updates

```
User logs in
    ↓
WebSocket connects
    ↓
Presence set to "online"
    ↓
Broadcast to all connected users
    ↓
Green dot appears in other users' lists
    ↓
User logs out
    ↓
Presence set to "offline"
    ↓
Green dot disappears
```

## User Flow Diagrams

### Starting a New Chat

```
1. Login
   ↓
2. See 💬 Chat button (bottom-right)
   ↓
3. Click button
   ↓
4. Modal opens with tabs
   ↓
5. Click "👥 Online" tab
   ↓
6. See list of online users
   ↓
7. Click on a user
   ↓
8. Chat window opens
   ↓
9. Type and send message
   ↓
10. See message appear instantly
```

### Continuing Existing Chat

```
1. Login
   ↓
2. Click 💬 Chat button
   ↓
3. See "💬 Chats" list
   ↓
4. Click on existing chat
   ↓
5. See chat history
   ↓
6. Continue conversation
```

## Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: New line (not implemented yet, future enhancement)
- **Escape**: Close chat modal (not implemented yet, future enhancement)

## Accessibility Features

- **ARIA Labels**: All buttons have aria-label attributes
- **Keyboard Navigation**: Tab through elements
- **Screen Reader Support**: Semantic HTML structure
- **Color Contrast**: Meets WCAG AA standards
- **Focus Indicators**: Visible focus states on all interactive elements

## Error States

### No Internet Connection

```
┌───────────────────────────────────┐
│ ⚠️  Connection Lost              │
│ Trying to reconnect...            │
└───────────────────────────────────┘
```

### Failed to Send Message

```
┌───────────────────────────────────┐
│ ❌ Failed to send message         │
│ Please try again        [Retry]   │
└───────────────────────────────────┘
```

### Empty States

**No Chats Yet**:
```
┌───────────────────────────────┐
│                               │
│       📭                      │
│    No chats yet               │
│                               │
│ Start a chat with online      │
│ users!                        │
│                               │
└───────────────────────────────┘
```

**No Online Users**:
```
┌───────────────────────────────┐
│                               │
│       👥                      │
│    No users online            │
│                               │
│ Check back later              │
│                               │
└───────────────────────────────┘
```

## Animation Effects

1. **Modal Slide Up**: Modal slides up from bottom when opening
2. **Button Hover**: Slight lift effect with shadow enhancement
3. **Message Appear**: New messages fade in smoothly
4. **Online Dot Pulse**: Green dot gently pulses
5. **Room Item Hover**: Slides right 5px on hover

## Technical Implementation Notes

### WebSocket Events

```
Client ──[Connect]──> Server
       <─[Connected]──

Client ──[Send Message]──> Server
       <─[Message ACK]────

Server ──[New Message]───> Client
Server ──[Presence Update]─> Client
Server ──[Typing Indicator]─> Client
```

### State Management

The chat component manages these states:
- `isOpen`: Modal visibility
- `activeView`: Current view (rooms/users/chat)
- `chatRooms`: List of chat rooms
- `activeRoom`: Currently open room
- `messages`: Messages in active room
- `onlineUsers`: List of online users
- `newMessage`: Text input value
- `loading`: Loading state
- `error`: Error message

## Best Practices for Users

1. **Keep messages concise**: Better for mobile viewing
2. **Use proper grammar**: Makes communication clearer
3. **Respect response times**: Not everyone is always available
4. **Use group chats wisely**: Avoid spamming
5. **Be professional**: Remember this is a fitness coaching platform

## Future UI Enhancements (Planned)

- [ ] Message reactions (emoji)
- [ ] Rich text formatting (bold, italic)
- [ ] File/image attachments
- [ ] Voice messages
- [ ] Read receipts (✓✓)
- [ ] Message search
- [ ] Chat themes
- [ ] Notification badges
- [ ] Sound notifications
- [ ] Desktop notifications
