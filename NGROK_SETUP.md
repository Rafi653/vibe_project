# ngrok Setup Guide for Public App Sharing

This guide explains how to use ngrok to expose your local Vibe Fitness Platform to the internet for testing and sharing with friends, testers, or clients.

## 📋 Table of Contents
- [What is ngrok?](#what-is-ngrok)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

## 🤔 What is ngrok?

ngrok is a tool that creates secure tunnels to your localhost, making your local development server accessible from the internet. This is perfect for:
- Sharing your app with friends or testers
- Testing webhooks from external services
- Demonstrating features to clients
- Mobile device testing
- Remote collaboration

## 📦 Prerequisites

Before setting up ngrok, ensure you have:
- The Vibe Fitness Platform running locally (see [QUICK_START.md](QUICK_START.md))
- Frontend running on `http://localhost:3000`
- Backend running on `http://localhost:8000`

## 🔧 Installation

### Option 1: Using Homebrew (macOS)
```bash
brew install ngrok/ngrok/ngrok
```

### Option 2: Using apt (Linux)
```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list && \
  sudo apt update && sudo apt install ngrok
```

### Option 3: Using Chocolatey (Windows)
```bash
choco install ngrok
```

### Option 4: Manual Download
Download from [ngrok.com/download](https://ngrok.com/download) and follow the installation instructions for your platform.

### Verify Installation
```bash
ngrok version
```

## 🚀 Quick Start

### Step 1: Get Your ngrok Auth Token

1. Sign up for a free account at [ngrok.com/signup](https://dashboard.ngrok.com/signup)
2. Get your auth token from [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Keep this token secure - don't commit it to version control

### Step 2: Configure ngrok

Create your ngrok configuration file:

```bash
# From the project root directory
cp ngrok.yml.example ngrok.yml
```

Edit `ngrok.yml` and replace `YOUR_NGROK_AUTH_TOKEN` with your actual token:

```yaml
version: "2"
authtoken: your_actual_token_here
tunnels:
  frontend:
    proto: http
    addr: 3000
    inspect: true
  backend:
    proto: http
    addr: 8000
    inspect: true
```

### Step 3: Start Your Application

**With Docker:**
```bash
docker compose up -d
```

**Without Docker:**
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Start frontend
cd frontend
npm start
```

### Step 4: Start ngrok

**Option A: Using the provided script (Recommended)**
```bash
./scripts/start-ngrok.sh
```

**Option B: Using npm (from frontend directory)**
```bash
cd frontend
npm run ngrok
```

**Option C: Manual start**
```bash
ngrok start --all --config=ngrok.yml
```

### Step 5: Note Your Public URLs

ngrok will display your public URLs. Example output:
```
Session Status                online
Account                       your@email.com
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040

Forwarding                    https://abc123.ngrok.io -> http://localhost:3000
Forwarding                    https://def456.ngrok.io -> http://localhost:8000
```

### Step 6: Update Backend CORS Configuration

Update your backend environment variables to allow the ngrok URLs:

**With Docker:**
Edit `docker-compose.yml` and add:
```yaml
backend:
  environment:
    - NGROK_FRONTEND_URL=https://abc123.ngrok.io
    - NGROK_BACKEND_URL=https://def456.ngrok.io
```

Then restart:
```bash
docker compose restart backend
```

**Without Docker:**
Edit `backend/.env`:
```env
NGROK_FRONTEND_URL=https://abc123.ngrok.io
NGROK_BACKEND_URL=https://def456.ngrok.io
```

Then restart your backend server.

### Step 7: Update Frontend API URL

Update your frontend to use the ngrok backend URL:

**With Docker:**
Edit `docker-compose.yml`:
```yaml
frontend:
  environment:
    - REACT_APP_API_URL=https://def456.ngrok.io
```

Then restart:
```bash
docker compose restart frontend
```

**Without Docker:**
Edit `frontend/.env`:
```env
REACT_APP_API_URL=https://def456.ngrok.io
```

Then restart your frontend server.

### Step 8: Share Your App!

Share your frontend ngrok URL (e.g., `https://abc123.ngrok.io`) with your testers!

## 📖 Configuration

### Basic Configuration

The `ngrok.yml` file supports various configuration options:

```yaml
version: "2"
authtoken: YOUR_NGROK_AUTH_TOKEN

# Configure multiple tunnels
tunnels:
  frontend:
    proto: http
    addr: 3000
    inspect: true
    # Optional: Custom subdomain (requires paid plan)
    # subdomain: myapp-frontend
    
  backend:
    proto: http
    addr: 8000
    inspect: true
    # Optional: Custom subdomain (requires paid plan)
    # subdomain: myapp-backend
```

### Advanced Configuration

For more control, you can add:

```yaml
tunnels:
  frontend:
    proto: http
    addr: 3000
    inspect: true
    # Request/response headers
    request_headers:
      add:
        - "X-Custom-Header: value"
    # IP restrictions (paid feature)
    # ip_restrictions:
    #   allow_cidrs:
    #     - "192.168.1.0/24"
```

## 💡 Usage Examples

### Expose Frontend Only

```bash
ngrok http 3000 --log=stdout
```

### Expose Backend Only

```bash
ngrok http 8000 --log=stdout
```

Or use npm scripts:
```bash
cd frontend
npm run ngrok:frontend  # Exposes frontend only
npm run ngrok:backend   # Exposes backend only
```

### Expose Both with Custom Subdomains (Paid Plan)

Edit `ngrok.yml`:
```yaml
tunnels:
  frontend:
    proto: http
    addr: 3000
    subdomain: vibe-app-frontend
  backend:
    proto: http
    addr: 8000
    subdomain: vibe-app-backend
```

### View Traffic Inspector

ngrok provides a web interface to inspect HTTP traffic:
- Open [http://localhost:4040](http://localhost:4040) in your browser
- View all requests and responses
- Replay requests for debugging

## 🔒 Security Considerations

### Important Security Notes

⚠️ **Never expose your app to the internet without considering security:**

1. **Authentication is Required**
   - Ensure your authentication system is working
   - Don't share credentials publicly
   - Use strong passwords for test accounts

2. **Environment Variables**
   - Never commit `ngrok.yml` with your auth token
   - Use `.env` files (already gitignored)
   - The project `.gitignore` excludes `ngrok.yml`

3. **Database Safety**
   - Use development/test data only
   - Don't expose production databases
   - Consider using a separate test database

4. **Limited Access**
   - ngrok URLs are public but hard to guess
   - Share URLs only with trusted testers
   - URLs change each time you restart ngrok (unless using paid features)

5. **Monitoring**
   - Check the ngrok inspector at http://localhost:4040
   - Monitor backend logs for suspicious activity
   - Limit exposure time

6. **Best Practices**
   - Only expose when actively testing
   - Shut down ngrok when not in use
   - Use ngrok's IP restriction feature (paid plan)
   - Consider basic auth middleware for extra protection

### Recommended Security Middleware (Optional)

For extra security, consider adding basic authentication to your frontend or backend when using ngrok. This can be done through:
- Nginx reverse proxy with basic auth
- FastAPI middleware for IP restrictions
- Environment-based feature flags

## 🐛 Troubleshooting

### ngrok Command Not Found

**Problem:** `bash: ngrok: command not found`

**Solution:**
1. Verify installation: `which ngrok`
2. Reinstall ngrok using one of the installation methods above
3. On Linux, ensure `/usr/local/bin` is in your PATH

### Invalid Auth Token

**Problem:** `ERROR: authentication failed: Your authtoken is invalid`

**Solution:**
1. Verify your token at [dashboard.ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)
2. Update `ngrok.yml` with the correct token
3. Ensure no extra spaces or quotes in the token

### CORS Errors

**Problem:** Browser shows CORS errors when accessing the app

**Solution:**
1. Ensure you've updated the backend `NGROK_FRONTEND_URL` environment variable
2. Restart the backend service after updating
3. Check the backend logs to verify the ngrok URL is in ALLOWED_ORIGINS
4. Clear browser cache and reload

### Connection Refused

**Problem:** ngrok says "connection refused"

**Solution:**
1. Verify your app is running on the specified ports:
   ```bash
   curl http://localhost:3000  # Frontend
   curl http://localhost:8000  # Backend
   ```
2. Check if ports are correct in `ngrok.yml`
3. Ensure no firewall is blocking the connections

### Frontend Can't Connect to Backend

**Problem:** Frontend loads but API calls fail

**Solution:**
1. Update `REACT_APP_API_URL` to the ngrok backend URL
2. Restart the frontend service
3. Check browser console for the actual API URL being used
4. Verify backend CORS includes the frontend ngrok URL

### Tunnel Established but App Won't Load

**Problem:** ngrok tunnel shows as established but browser shows errors

**Solution:**
1. Check ngrok inspector at http://localhost:4040
2. Look for HTTP status codes and error messages
3. Verify the local app is accessible at `http://localhost:3000` or `http://localhost:8000`
4. Check browser console for JavaScript errors

### URLs Keep Changing

**Problem:** ngrok URLs change every time you restart

**Solution:**
- Free tier generates random URLs each time
- Upgrade to paid plan for:
  - Custom subdomains
  - Reserved domains
  - Persistent URLs

### Performance Issues

**Problem:** App is slow through ngrok

**Solution:**
1. ngrok adds latency (expected behavior)
2. Check your internet connection
3. Consider using a closer ngrok region
4. Remember this is for testing only, not production

## 📚 Additional Resources

- [ngrok Documentation](https://ngrok.com/docs)
- [ngrok Pricing](https://ngrok.com/pricing) - Free tier available
- [ngrok Dashboard](https://dashboard.ngrok.com)
- [ngrok Inspector Guide](https://ngrok.com/docs/secure-tunnels/ngrok-agent/reference/config#inspect)

## 🎯 Next Steps

After setting up ngrok:
1. Test all key features through the public URL
2. Collect feedback from testers
3. Monitor the ngrok inspector for issues
4. Document any bugs or improvements needed
5. Remember to shut down ngrok when done testing

---

**Note:** ngrok is intended for development and testing purposes. For production deployments, see [DEPLOYMENT.md](DEPLOYMENT.md).
