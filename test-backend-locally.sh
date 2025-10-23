#!/bin/bash

# Test MSP Alert Intelligence Backend Locally
# This script starts the backend and runs a simple health check

set -e

echo "🚀 Starting MSP Alert Intelligence Backend..."
echo "================================================"

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Error: backend directory not found"
    exit 1
fi

cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Set environment variables for testing
export DATABASE_URL="sqlite:///./test_msp_alerts.db"
export DEBUG="true"
export KEEP_WEBHOOK_SECRET="test-secret-123"
export AWS_REGION="us-east-1"
export BEDROCK_MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"

echo ""
echo "✅ Backend configured with test environment"
echo ""
echo "📍 API will be available at: http://localhost:8000"
echo "📖 API docs will be at: http://localhost:8000/docs"
echo ""
echo "🧪 Test endpoints:"
echo "   - Health: http://localhost:8000/health"
echo "   - Alerts: http://localhost:8000/api/v1/alerts"
echo "   - Test Webhook: POST http://localhost:8000/api/v1/test/keep-webhook"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the server
python -m uvicorn main:app --reload --port 8000

