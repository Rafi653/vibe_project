#!/bin/bash

# Script to start ngrok tunnels for Vibe Fitness Platform
# This script helps expose the application for public testing and sharing

set -e

echo "🚀 Starting ngrok tunnels for Vibe Fitness Platform..."
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed!"
    echo ""
    echo "Please install ngrok:"
    echo "  macOS:   brew install ngrok/ngrok/ngrok"
    echo "  Linux:   curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok"
    echo "  Windows: choco install ngrok"
    echo ""
    echo "Or download from: https://ngrok.com/download"
    exit 1
fi

# Check if ngrok config exists
if [ ! -f "ngrok.yml" ]; then
    echo "⚠️  ngrok.yml not found in the current directory"
    echo "Creating a template ngrok.yml..."
    cat > ngrok.yml << 'EOF'
version: "2"
authtoken: YOUR_NGROK_AUTH_TOKEN
tunnels:
  frontend:
    proto: http
    addr: 3000
    inspect: true
  backend:
    proto: http
    addr: 8000
    inspect: true
EOF
    echo "✅ Created ngrok.yml template"
    echo ""
fi

# Check if auth token is configured
if grep -q "YOUR_NGROK_AUTH_TOKEN" ngrok.yml; then
    echo "⚠️  Warning: ngrok auth token not configured!"
    echo ""
    echo "To set up your ngrok auth token:"
    echo "  1. Sign up at https://dashboard.ngrok.com/signup"
    echo "  2. Get your auth token from https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "  3. Replace 'YOUR_NGROK_AUTH_TOKEN' in ngrok.yml with your token"
    echo ""
    echo "Continuing without auth token (limited features)..."
    echo ""
fi

echo "📡 Starting tunnels..."
echo ""
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo ""

# Start ngrok with all configured tunnels
ngrok start --all --config=ngrok.yml

# Note: This will run in foreground. Press Ctrl+C to stop.
