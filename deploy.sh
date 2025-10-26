#!/bin/bash
# Auto-deployment script for staging environment

cd ~/workspace

# Kill old process
pkill -f 'python.*main.py' || true

# Wait for clean shutdown
sleep 2

# Start new process
nohup python3 main.py > app.log 2>&1 &

echo "✅ Application restarted at $(date)"

