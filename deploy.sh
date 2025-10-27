#!/bin/bash
set -e  # Exit on any error

DEPLOY_DIR="/home/ahmedbilal/staging"

cd $DEPLOY_DIR

echo "📥 Pulling latest code from main..."
git pull origin main

echo "🛑 Killing any processes on port 8000..."
echo 'claudeSONNET45' | sudo -S fuser -k -9 8000/tcp 2>/dev/null || true
echo 'claudeSONNET45' | sudo -S pkill -9 -f 'uvicorn.*8000' 2>/dev/null || true
sleep 3

echo "📦 Installing frontend dependencies..."
cd $DEPLOY_DIR/frontend && npm install --silent

echo "🔨 Building React frontend..."
npm run build

echo "📦 Installing Python dependencies..."
cd $DEPLOY_DIR
pip3 install -r requirements.txt --break-system-packages --quiet || true

echo "🚀 Starting backend from $DEPLOY_DIR..."
cd $DEPLOY_DIR
nohup python3 main.py > app.log 2>&1 &

sleep 2

echo "✅ Deployment complete at $(date)"
echo "   Server running from: $DEPLOY_DIR"
