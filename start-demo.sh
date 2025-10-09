#!/bin/bash

# MSP Alert Intelligence Platform - Demo Startup Script
# This script starts the demo backend without Docker

echo "🚀 Starting MSP Alert Intelligence Platform (Demo Mode)..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn pydantic pydantic-settings python-dotenv pyyaml

# Start the demo backend
echo "🚀 Starting demo backend server..."
echo "📍 Backend will be available at: http://localhost:8000"
echo "📍 API documentation at: http://localhost:8000/docs"
echo "📍 Health check at: http://localhost:8000/health"
echo ""
echo "🎯 Demo Features Available:"
echo "- Alert Management API"
echo "- Simulated AI Agents"
echo "- Alert Deduplication"
echo "- Alert Correlation"
echo "- Alert Enrichment"
echo "- Incident Management"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python demo_main.py
