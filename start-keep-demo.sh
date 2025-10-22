#!/bin/bash

# Keep Integration Demo - Quick Start Script
# Starts all services and runs the demo

set -e

echo "🚀 Starting Keep Integration Demo"
echo "================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
BACKEND_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"

echo -e "${BLUE}📋 Demo Setup${NC}"
echo "Backend: $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"
echo ""

# Function to check if service is running
check_service() {
    local url=$1
    local name=$2
    
    if curl -s "$url/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $name is running${NC}"
        return 0
    else
        echo -e "${RED}❌ $name is not running${NC}"
        return 1
    fi
}

# Check if services are already running
echo -e "${BLUE}🔍 Checking Services${NC}"
BACKEND_RUNNING=false
FRONTEND_RUNNING=false

if check_service "$BACKEND_URL" "Backend"; then
    BACKEND_RUNNING=true
fi

if check_service "$FRONTEND_URL" "Frontend"; then
    FRONTEND_RUNNING=true
fi

# Start backend if not running
if [ "$BACKEND_RUNNING" = false ]; then
    echo -e "${YELLOW}🚀 Starting Backend...${NC}"
    echo "Please run in a separate terminal:"
    echo "cd backend && python main.py"
    echo ""
    echo "Press Enter when backend is running..."
    read -r
fi

# Start frontend if not running
if [ "$FRONTEND_RUNNING" = false ]; then
    echo -e "${YELLOW}🚀 Starting Frontend...${NC}"
    echo "Please run in a separate terminal:"
    echo "cd frontend && npm run dev"
    echo ""
    echo "Press Enter when frontend is running..."
    read -r
fi

# Verify services are running
echo -e "${BLUE}🔍 Verifying Services${NC}"
if ! check_service "$BACKEND_URL" "Backend"; then
    echo -e "${RED}❌ Backend is not running. Please start it first.${NC}"
    exit 1
fi

if ! check_service "$FRONTEND_URL" "Frontend"; then
    echo -e "${RED}❌ Frontend is not running. Please start it first.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ All services are running!${NC}"
echo ""

# Run the demo
echo -e "${BLUE}🎬 Running Keep Integration Demo${NC}"
echo "=================================="
echo ""

# Run the demo script
if [ -f "scripts/demo-keep-integration.sh" ]; then
    chmod +x scripts/demo-keep-integration.sh
    ./scripts/demo-keep-integration.sh
else
    echo -e "${RED}❌ Demo script not found${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Demo Complete!${NC}"
echo ""
echo -e "${BLUE}📊 Demo Summary${NC}"
echo "================"
echo "✅ Keep webhook integration demonstrated"
echo "✅ MSP noise reduction shown"
echo "✅ AI correlation with Bedrock highlighted"
echo "✅ SLA management configured"
echo "✅ Database integration functional"
echo "✅ Frontend dashboard live"
echo ""
echo -e "${BLUE}🎯 Next Steps${NC}"
echo "============="
echo "1. Open frontend: $FRONTEND_URL/frontend-demo.html"
echo "2. Show live alert processing"
echo "3. Demonstrate noise reduction"
echo "4. Highlight AI correlation"
echo "5. Explain Keep integration benefits"
echo ""
echo -e "${GREEN}🚀 Demo Ready for Presentation!${NC}"
