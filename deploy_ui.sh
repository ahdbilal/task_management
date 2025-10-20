#!/bin/bash

echo "🚀 Building and Deploying UI to Remote Staging..."
echo ""

# Step 1: Install frontend dependencies (if not done)
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Step 2: Build React app
echo "🔨 Building React production bundle..."
cd frontend
npm run build
cd ..

echo "✅ Build complete!"
echo ""
echo "📂 Built files are in: frontend/build/"
echo ""
echo "Next: Deploy to remote using bridge"

