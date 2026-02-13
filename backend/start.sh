#!/bin/bash

# Backend Startup Script for Cloud Security Threat Predictor

echo "🚀 Starting Cloud Security Backend..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating it now..."
    python3 -m venv venv
    echo "✅ Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
fi

# Verify FastAPI is installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ FastAPI not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Start uvicorn server
echo "✅ Starting FastAPI server on http://localhost:8000..."
echo "📝 Press CTRL+C to stop the server"
echo ""
python -m uvicorn app.main:app --reload
