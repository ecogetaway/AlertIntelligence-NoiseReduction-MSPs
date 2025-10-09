#!/bin/bash

# MSP Alert Intelligence Platform - Safe Demo Startup Script
# This script finds an available port and starts the frontend demo

echo "🚀 Starting MSP Alert Intelligence Platform - Frontend Demo..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if the demo file exists
if [ ! -f "frontend-demo.html" ]; then
    echo "❌ frontend-demo.html not found. Please make sure you're in the project directory."
    exit 1
fi

echo "✅ Frontend demo file found"

# Function to find an available port
find_available_port() {
    local port=3000
    while lsof -ti:$port > /dev/null 2>&1; do
        port=$((port + 1))
        if [ $port -gt 9999 ]; then
            echo "❌ No available ports found in range 3000-9999"
            exit 1
        fi
    done
    echo $port
}

# Find an available port
PORT=$(find_available_port)
echo "📍 Using port: $PORT"

echo ""
echo "🎯 Demo Features:"
echo "- ✅ Interactive Alert Dashboard"
echo "- ✅ Real-time Alert Management"
echo "- ✅ AI Agent Status Display"
echo "- ✅ Alert Filtering and Search"
echo "- ✅ Incident Management"
echo "- ✅ Analytics Dashboard"
echo "- ✅ Responsive Design"
echo ""
echo "📍 Demo will be available at: http://localhost:$PORT"
echo "📍 Direct link: http://localhost:$PORT/frontend-demo.html"
echo ""
echo "🎯 What you can do in the demo:"
echo "- View alerts with different severities and statuses"
echo "- Filter alerts by severity, status, and source"
echo "- Acknowledge, suppress, and resolve alerts"
echo "- View AI-powered enrichments and correlations"
echo "- Check incident management"
echo "- View analytics and AI processing metrics"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the HTTP server
echo "🚀 Starting HTTP server on port $PORT..."
python3 -m http.server $PORT
