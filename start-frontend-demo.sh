#!/bin/bash

# MSP Alert Intelligence Platform - Frontend Demo Startup Script
# This script starts a simple HTTP server to serve the frontend demo

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
echo "📍 Opening demo in browser..."
echo "📍 Demo will be available at: http://localhost:8080"
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

# Start a simple HTTP server
python3 -m http.server 8080
