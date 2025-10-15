# Chat Feature Deployment Steps

This document provides step-by-step instructions to deploy the new chat feature.

## Prerequisites

- Docker and Docker Compose installed
- Repository cloned locally
- `.env` file configured (see `.env.example`)

## Step 1: Stop Existing Containers

```bash
cd /path/to/vibe_project
docker compose down
```

## Step 2: Rebuild Containers

Since we've added new dependencies and code:

```bash
docker compose build --no-cache
```

**Note**: This may take 5-10 minutes as it rebuilds both frontend and backend.

## Step 3: Start All Services

```bash
docker compose up -d
```

This starts:
- PostgreSQL database (port 5432)
- Backend API (port 8000)
- Frontend React app (port 3000)

## Step 4: Wait for Services to be Healthy

Check service status:

```bash
docker compose ps
```

Wait until all services show as "healthy" or "running". This may take 30-60 seconds.

## Step 5: Run Database Migration

Apply the new chat tables migration:

```bash
docker compose exec backend alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade 005_add_feedback_status -> 006_add_chat_tables
```

## Step 6: Verify Migration Status

Check that migration was applied:

```bash
docker compose exec backend alembic current
```

Expected output should show: `006_add_chat_tables (head)`

## Step 7: Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/api/docs

## Step 8: Test the Chat Feature

### 8.1 Create Test Users

If you don't have test users, create them:

1. Go to http://localhost:3000/signup
2. Create at least 2 users (to test chat between them)
3. Note the login credentials

### 8.2 Test Chat Functionality

**In Browser 1 (User 1)**:
1. Login at http://localhost:3000/login
2. Look for the **💬 Chat** button in the bottom-right corner
3. Click the Chat button

**In Browser 2 (or Incognito Window) (User 2)**:
1. Login with the second user
2. Click the **💬 Chat** button

**Test Real-time Messaging**:
1. In Browser 1: Click the **👥 Online** tab
2. You should see User 2 listed as online (green dot)
3. Click on User 2 to start a chat
4. Send a message: "Hello from User 1!"
5. In Browser 2: You should see the message appear instantly
6. Reply from User 2: "Hello back!"
7. Verify the message appears in Browser 1 without refresh

### 8.3 Test Features

- ✅ Direct messaging
- ✅ Real-time message delivery
- ✅ Online presence indicator
- ✅ Chat history persistence (refresh browser and check messages are still there)
- ✅ Multiple simultaneous chats
- ✅ Responsive UI on mobile viewport

## Step 9: Screenshots

Take screenshots for documentation:

1. **Chat button** (floating button in bottom-right)
2. **Chat rooms list** (shows existing conversations)
3. **Online users list** (shows who's online)
4. **Chat conversation** (showing message exchange)
5. **Mobile view** (resize browser to mobile width)

## Troubleshooting

### Issue: Backend won't start

**Check logs**:
```bash
docker compose logs backend
```

**Common fixes**:
1. Check `.env` file is configured
2. Ensure database is running: `docker compose ps postgres`
3. Check for port conflicts: `lsof -i :8000`

### Issue: Migration fails

**Check database connection**:
```bash
docker compose exec backend python -c "from app.db.base import engine; import asyncio; asyncio.run(engine.connect())"
```

**Try manual migration**:
```bash
docker compose exec backend alembic history
docker compose exec backend alembic current
docker compose exec backend alembic upgrade head --sql  # Preview SQL
docker compose exec backend alembic upgrade head
```

### Issue: WebSocket not connecting

**Check browser console for errors**:
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for WebSocket connection errors

**Verify WebSocket endpoint**:
```bash
curl http://localhost:8000/api/docs
# Look for /api/v1/chat/ws/{user_id} endpoint
```

### Issue: Messages not appearing

**Check WebSocket connection**:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Filter for "WS" (WebSocket)
4. Check connection status

**Verify backend is receiving messages**:
```bash
docker compose logs backend | grep -i websocket
```

### Issue: Users not showing as online

**Check presence endpoint**:
```bash
# Get auth token from browser localStorage
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/v1/chat/presence
```

## Rollback Instructions

If you need to rollback the chat feature:

### Option 1: Downgrade Migration Only

Keep the code but remove the database tables:

```bash
docker compose exec backend alembic downgrade -1
```

### Option 2: Full Rollback

1. Checkout previous commit:
```bash
git checkout HEAD~3  # Go back before chat feature
```

2. Rebuild and restart:
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

3. Downgrade database:
```bash
docker compose exec backend alembic downgrade 005_add_feedback_status
```

## Upgrading Again

If you rolled back and want to upgrade again:

1. Checkout the chat feature branch:
```bash
git checkout copilot/add-in-app-chat-feature-2
```

2. Rebuild containers:
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

3. Apply migration:
```bash
docker compose exec backend alembic upgrade head
```

## Production Deployment Notes

### Before Deploying to Production

1. **Review Security**:
   - Ensure JWT secret key is strong and unique
   - Configure CORS allowed origins properly
   - Set up rate limiting
   - Enable HTTPS for WebSocket connections

2. **Performance**:
   - Set up Redis for WebSocket connection management
   - Configure database connection pooling
   - Enable message pagination for large chat rooms

3. **Monitoring**:
   - Set up logging for WebSocket connections
   - Monitor database query performance
   - Track active WebSocket connections

4. **Backup**:
   - Backup database before migration
   - Test rollback procedure
   - Have maintenance window planned

### Production Migration Command

```bash
# SSH into production server
ssh user@production-server

# Navigate to app directory
cd /path/to/vibe_project

# Pull latest code
git pull origin main

# Rebuild containers
docker compose -f docker-compose.prod.yml build --no-cache

# Stop containers
docker compose -f docker-compose.prod.yml down

# Start containers
docker compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
sleep 30

# Apply migration
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Verify migration
docker compose -f docker-compose.prod.yml exec backend alembic current

# Check logs
docker compose -f docker-compose.prod.yml logs backend --tail=100
```

## Maintenance

### Regular Tasks

1. **Monitor WebSocket connections**:
```bash
docker compose exec backend ps aux | grep uvicorn
```

2. **Check database size**:
```bash
docker compose exec postgres psql -U vibe_user -d vibe_db -c "
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

3. **Clean up old messages** (if needed):
```bash
# Example: Delete messages older than 90 days
docker compose exec postgres psql -U vibe_user -d vibe_db -c "
DELETE FROM messages 
WHERE created_at < NOW() - INTERVAL '90 days';
"
```

## Support

For issues during deployment:
1. Check logs: `docker compose logs`
2. Review CHAT_FEATURE_GUIDE.md
3. Check API documentation: http://localhost:8000/api/docs
4. Create GitHub issue with error details
