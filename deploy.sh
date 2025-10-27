#!/bin/bash
set -e

cd /home/ahmedbilal/workspace

echo "📦 Installing frontend dependencies..."
cd frontend && npm install --silent

echo "🔨 Building React frontend..."
npm run build

echo "🔄 Restarting backend..."
cd /home/ahmedbilal/workspace

# Install/update Python dependencies
pip3 install -r requirements.txt --break-system-packages --quiet || true

# Kill ALL processes on port 8000 using sudo (works for all users)
echo "🛑 Killing old processes on port 8000..."
echo 'claudeSONNET45' | sudo -S fuser -k -9 8000/tcp 2>/dev/null || true
echo 'claudeSONNET45' | sudo -S pkill -9 -f 'uvicorn.*8000' 2>/dev/null || true

sleep 5

# Start new backend
echo "🚀 Starting new backend..."
nohup python3 main.py > app.log 2>&1 &

sleep 3

echo "✅ Deployment complete at $(date)"

