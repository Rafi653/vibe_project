# ngrok Quick Reference

Quick commands for sharing your Vibe Fitness Platform with ngrok.

## 🚀 Quick Start (3 Steps)

```bash
# 1. Install ngrok
brew install ngrok/ngrok/ngrok  # macOS
# Or see NGROK_SETUP.md for other platforms

# 2. Configure (first time only)
cp ngrok.yml.example ngrok.yml
# Edit ngrok.yml and add your auth token from https://dashboard.ngrok.com

# 3. Start sharing!
./scripts/start-ngrok.sh
```

## 📋 Common Commands

### Start ngrok with both tunnels
```bash
./scripts/start-ngrok.sh
```

### Start only frontend tunnel
```bash
cd frontend
npm run ngrok:frontend
```

### Start only backend tunnel
```bash
cd frontend
npm run ngrok:backend
```

### View ngrok web interface
```bash
# After starting ngrok, open:
open http://localhost:4040
```

## ⚙️ Configuration Checklist

After getting your ngrok URLs:

### 1. Update Backend CORS

**Docker:**
```yaml
# docker-compose.yml
backend:
  environment:
    - NGROK_FRONTEND_URL=https://your-frontend-url.ngrok.io
    - NGROK_BACKEND_URL=https://your-backend-url.ngrok.io
```

**Local:**
```env
# backend/.env
NGROK_FRONTEND_URL=https://your-frontend-url.ngrok.io
NGROK_BACKEND_URL=https://your-backend-url.ngrok.io
```

### 2. Update Frontend API URL

**Docker:**
```yaml
# docker-compose.yml
frontend:
  environment:
    - REACT_APP_API_URL=https://your-backend-url.ngrok.io
```

**Local:**
```env
# frontend/.env
REACT_APP_API_URL=https://your-backend-url.ngrok.io
```

### 3. Restart Services

**Docker:**
```bash
docker compose restart backend frontend
```

**Local:**
```bash
# Restart both backend and frontend servers
```

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ngrok: command not found` | Install ngrok (see installation commands above) |
| `authentication failed` | Add your auth token to `ngrok.yml` |
| CORS errors in browser | Update `NGROK_FRONTEND_URL` in backend and restart |
| Frontend can't connect to API | Update `REACT_APP_API_URL` in frontend and restart |
| Connection refused | Ensure app is running on ports 3000 and 8000 |

## 🔒 Security Reminder

- ✅ Only use with test/development data
- ✅ Share URLs only with trusted testers
- ✅ Shut down ngrok when not testing
- ✅ Monitor traffic via http://localhost:4040
- ❌ Never expose production databases
- ❌ Don't commit `ngrok.yml` with your token

## 📚 Full Documentation

For complete setup, advanced configuration, and detailed troubleshooting:
- **[NGROK_SETUP.md](NGROK_SETUP.md)** - Complete guide

## 🎯 Example Workflow

```bash
# 1. Start your app
docker compose up -d

# 2. Start ngrok in another terminal
./scripts/start-ngrok.sh

# 3. Note your URLs from ngrok output
# Frontend: https://abc123.ngrok.io
# Backend:  https://def456.ngrok.io

# 4. Update backend CORS (docker-compose.yml or .env)
# Add NGROK_FRONTEND_URL and NGROK_BACKEND_URL

# 5. Update frontend API URL (docker-compose.yml or .env)
# Set REACT_APP_API_URL to backend ngrok URL

# 6. Restart services
docker compose restart backend frontend

# 7. Share frontend URL with testers!
# https://abc123.ngrok.io
```

---

**Happy Sharing! 🎉**
