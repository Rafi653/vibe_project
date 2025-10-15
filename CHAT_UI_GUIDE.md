# Chat Feature - UI Guide

## User Interface Overview

The chat feature provides a WhatsApp-inspired interface with a floating button and expandable chat window.

## UI Components

### 1. Chat Trigger Button

**Location**: Fixed position, bottom-right corner
- Position: `bottom: 100px, right: 30px`
- Above the feedback button
- Color: Green gradient (`#56ab2f` to `#a8e063`)
- Icon: 💬 Chat emoji
- State: Always visible when user is authenticated

**Visual Style**:
```
┌──────────────┐
│  💬 Chat     │  ← Green gradient button
└──────────────┘
```

### 2. Chat Window

**Dimensions**:
- Width: 400px (desktop)
- Height: 600px
- Position: Fixed, bottom-right
- Border radius: 20px
- Shadow: Large shadow for elevation

**Layout Structure**:
```
┌─────────────────────────────────────┐
│  Header (Green gradient)            │
│  ← Back   Title         ×           │
├─────────────────────────────────────┤
│  Tab: Conversations | Active Users  │
├─────────────────────────────────────┤
│                                     │
│  Content Area                       │
│  (Scrollable)                       │
│                                     │
│                                     │
├─────────────────────────────────────┤
│  Input: Type message...  [Send]     │ ← Only in chat view
└─────────────────────────────────────┘
```

### 3. Conversations View

Shows list of all user conversations:

```
┌─────────────────────────────────────┐
│  Conversations | Active Users        │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │ Direct Message                │  │
│  │ Hello, how are you?           │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Fitness Group                 │  │
│  │ See you at the gym!           │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Features**:
- Conversation name (or "Direct Message")
- Last message preview
- Clickable to open conversation
- Sorted by most recent

### 4. Active Users View

Shows currently online users:

```
┌─────────────────────────────────────┐
│  Conversations | Active Users        │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │ 🟢 John Doe                   │  │
│  │    client                     │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ 🟢 Coach Sarah                │  │
│  │    coach                      │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Features**:
- Green dot indicator for online status
- User full name
- User role (client/coach/admin)
- Clickable to start direct chat
- Current user excluded from list

### 5. Chat View (Messages)

Active conversation with messages:

```
┌─────────────────────────────────────┐
│  ← Back   Direct Message        ×   │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────┐              │
│  │ Hi there!        │              │  ← Received
│  │ 10:30 AM         │              │
│  └───────────────────┘              │
│                                     │
│              ┌───────────────────┐  │
│              │ Hello!           │  │  ← Sent
│              │ 10:31 AM         │  │
│              └───────────────────┘  │
│                                     │
│  ⋯ ⋯ ⋯ (typing...)                 │  ← Typing indicator
│                                     │
├─────────────────────────────────────┤
│  [Type a message...]  [Send]        │
└─────────────────────────────────────┘
```

**Features**:
- Message bubbles aligned left (received) or right (sent)
- Timestamps on each message
- Typing indicator animation
- Auto-scroll to latest message
- Back button to return to conversations

### 6. Message Bubbles

**Sent Messages** (Right-aligned):
- Background: Green gradient
- Color: White text
- Border radius: Rounded, except bottom-right corner
- Max width: 70% of chat window

**Received Messages** (Left-aligned):
- Background: Light gray (#f0f0f0)
- Color: Dark text
- Border radius: Rounded, except bottom-left corner
- Max width: 70% of chat window

### 7. Empty States

**No Conversations**:
```
┌─────────────────────────────────────┐
│                                     │
│         No conversations yet        │
│                                     │
│    Start chatting with active       │
│         users!                      │
│                                     │
└─────────────────────────────────────┘
```

**No Active Users**:
```
┌─────────────────────────────────────┐
│                                     │
│         No users online             │
│                                     │
└─────────────────────────────────────┘
```

## Color Scheme

### Primary Colors
- **Green Gradient**: `#56ab2f` → `#a8e063`
- **Text on Green**: White
- **Sent Messages**: Green gradient
- **Received Messages**: `#f0f0f0` (light gray)

### Status Colors
- **Online Indicator**: `#4caf50` (green)
- **Typing Indicator**: `#999` (gray)

### Neutrals
- **Background**: White
- **Text**: `#333` (dark gray)
- **Secondary Text**: `#666` (medium gray)
- **Borders**: `#f0f0f0` (light gray)

## Responsive Behavior

### Desktop (> 768px)
- Window width: 400px
- Window height: 600px
- Fixed positioning
- Full feature set

### Mobile (≤ 768px)
- Window width: calc(100vw - 20px)
- Window height: calc(100vh - 20px)
- Positioned 10px from edges
- Max height: 700px
- Same features, optimized layout

## Interactions

### Hover Effects
1. **Buttons**: Slight upward movement, enhanced shadow
2. **Conversations/Users**: Background color change to `#f9f9f9`
3. **Chat button**: Upward translation, darker gradient

### Click Actions
1. **Chat Button**: Open/close chat window
2. **Conversation Item**: Open conversation view
3. **User Item**: Start/open direct message
4. **Send Button**: Send message (or press Enter)
5. **Back Button**: Return to conversations list
6. **Close Button (×)**: Close chat window

### Animations
1. **Window Open**: Slide up from bottom with fade-in
2. **Messages**: Fade in from bottom
3. **Typing Indicator**: Bouncing dots
4. **Scroll**: Smooth auto-scroll to latest message

## Accessibility

### Keyboard Support
- **Enter**: Send message
- **Escape**: Close chat (future enhancement)
- **Tab**: Navigate through elements

### ARIA Labels
- `aria-label="Open Chat"` on trigger button
- `aria-label="Close Chat"` on close button
- `aria-label="Submit Feedback"` maintained on feedback button

### Focus Management
- Input field auto-focused when entering chat view
- Proper tab order through interactive elements

## Z-Index Hierarchy

```
Chat Window:      z-index: 1000
Chat Button:      z-index: 999
Feedback Button:  z-index: 999
```

## Positioning

```
Screen Layout (Bottom-Right Corner):

                              ┌─────────────────┐
                              │                 │
                              │  Chat Window    │
                              │    (when open)  │
                              │                 │
                              │                 │
                              └─────────────────┘
                              ┌──────────────┐
                              │ 💬 Chat      │  ← 100px from bottom
                              └──────────────┘
                              ┌──────────────┐
                              │ 💬 Feedback  │  ← 30px from bottom
                              └──────────────┘
                              └──────────────→ 30px from right
```

## User Flow

### Starting a Direct Chat
1. User clicks "💬 Chat" button
2. Chat window opens to Conversations view
3. User clicks "Active Users" tab
4. User sees list of online users (excluding self)
5. User clicks on a user
6. Chat view opens with that user
7. User can type and send messages

### Viewing Conversations
1. User clicks "💬 Chat" button
2. Chat window opens to Conversations view
3. User sees list of all conversations
4. User clicks on a conversation
5. Chat view opens with message history
6. User can continue conversation

### Sending Messages
1. User in chat view
2. User types message in input field
3. Typing indicator shows to other participants (real-time)
4. User presses Enter or clicks Send
5. Message appears immediately (green bubble, right side)
6. Other participants receive message instantly

## Performance Notes

### Optimizations
- Messages rendered with React keys for efficient updates
- Scroll position managed with refs
- WebSocket connection reused for all chat operations
- Typing indicators debounced to reduce traffic

### Loading States
- Empty states for zero conversations/users
- Graceful handling of connection issues
- Automatic reconnection on WebSocket disconnect

## Browser Compatibility

Tested and verified on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile Safari (iOS 14+)
- ✅ Chrome Mobile (Android)

## Tips for Users

1. **Finding Users**: Check "Active Users" tab to see who's online
2. **Quick Reply**: Press Enter to send messages quickly
3. **Mobile**: Swipe down to close keyboard while viewing messages
4. **Multiple Conversations**: Switch between conversations from main list
5. **Back Button**: Use ← Back button to return to conversations without closing chat

## Tips for Developers

1. **Styling**: Green theme distinguishes from purple feedback button
2. **WebSocket**: Connection managed at component level
3. **State**: All messages and conversations in component state
4. **Real-time**: WebSocket handlers update state immediately
5. **Testing**: Use test users from seed data to test multi-user chat
