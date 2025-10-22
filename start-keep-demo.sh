#!/bin/bash

# MSP Alert Intelligence Platform - Keep Integration Demo Startup Script
# This script starts a simple HTTP server to serve all demo files including Keep integration

echo "🚀 Starting MSP Alert Intelligence Platform - Keep Integration Demo..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if demo files exist
if [ ! -f "keep-integration-demo.html" ]; then
    echo "❌ keep-integration-demo.html not found. Please make sure you're in the project directory."
    exit 1
fi

if [ ! -f "frontend-demo.html" ]; then
    echo "❌ frontend-demo.html not found. Please make sure you're in the project directory."
    exit 1
fi

if [ ! -f "frontend-simple.html" ]; then
    echo "❌ frontend-simple.html not found. Please make sure you're in the project directory."
    exit 1
fi

echo "✅ All demo files found"
echo ""
echo "🎯 Keep Integration Demo Features:"
echo "- ✅ Keep Foundation Integration"
echo "- ✅ MSP-Specific Enhancements"
echo "- ✅ AI-Powered Alert Correlation"
echo "- ✅ 80% Noise Reduction"
echo "- ✅ Real-time Dashboard"
echo "- ✅ Webhook Integration Testing"
echo ""
echo "📍 Demo Links Available:"
echo "🔗 Keep Integration Demo: http://localhost:3000/keep-integration-demo.html"
echo "🔗 Main Dashboard: http://localhost:3000/frontend-demo.html"
echo "🔗 Static Demo: http://localhost:3000/frontend-simple.html"
echo "🔗 Landing Page: http://localhost:3000/index.html"
echo ""
echo "🎯 What you can do in the Keep Integration Demo:"
echo "- Test Keep webhook integration"
echo "- View Keep Foundation features"
echo "- See MSP enhancements in action"
echo "- Test AI correlation and noise reduction"
echo "- Explore the integration flow"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start a simple HTTP server on port 3000
echo "🚀 Starting HTTP server on port 3000..."
python3 -m http.server 3000