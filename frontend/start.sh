#!/bin/bash

# Frontend Startup Script for Cloud Security Threat Predictor

echo "🚀 Starting Cloud Security Frontend..."

# Navigate to frontend directory
cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start Vite dev server
echo "✅ Starting Vite dev server on http://localhost:5173..."
npm run dev
