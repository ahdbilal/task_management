#!/bin/bash
set -e  # Exit on any error

cd /home/ahmedbilal/workspace

echo "📦 Installing frontend dependencies..."
cd frontend && npm install --silent

echo "🔨 Building React frontend..."
npm run build

echo "🔄 Restarting backend..."
cd /home/ahmedbilal/workspace
echo "   Killing processes on port 8000..."
fuser -k 8000/tcp || true
sleep 2
nohup python3 main.py > app.log 2>&1 &

echo "✅ Deployment complete at $(date)"
echo "   Frontend: Built ✓"
echo "   Backend: Restarted ✓"

