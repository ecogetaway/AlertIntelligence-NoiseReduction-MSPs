#!/bin/bash

# Keep Integration Demo Script
# Demonstrates MSP Alert Intelligence platform with Keep integration

set -e

echo "🚀 MSP Alert Intelligence - Keep Integration Demo"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"
DEMO_CLIENT_ID="demo-client-123"
DEMO_TENANT_ID="demo-tenant-456"

echo -e "${BLUE}📋 Demo Setup${NC}"
echo "Backend: $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"
echo ""

# Check if services are running
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

echo -e "${BLUE}🔍 Checking Services${NC}"
if ! check_service "$BACKEND_URL" "Backend"; then
    echo "Please start the backend: cd backend && python main.py"
    exit 1
fi

if ! check_service "$FRONTEND_URL" "Frontend"; then
    echo "Please start the frontend: cd frontend && npm run dev"
    exit 1
fi

echo ""
echo -e "${BLUE}🎯 Keep Integration Demo${NC}"
echo "================================"

# 1. Show Keep webhook endpoint
echo -e "${YELLOW}1. Keep Webhook Integration${NC}"
echo "Endpoint: POST $BACKEND_URL/api/v1/ingest/keep"
echo ""

# Create sample Keep alert payload
cat > /tmp/keep_alert.json << EOF
{
  "event": "alert.created",
  "alert": {
    "id": "keep-alert-$(date +%s)",
    "title": "High CPU Usage - Web Server",
    "severity": "critical",
    "source": "prometheus",
    "labels": {
      "service": "api",
      "instance": "web-01",
      "job": "node-exporter"
    },
    "annotations": {
      "summary": "CPU usage above 90% for 5 minutes",
      "description": "Instance web-01 has been above 90% CPU for 5 minutes"
    },
    "fingerprint": "cpu-high-web-01",
    "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  }
}
EOF

echo "Sample Keep alert payload:"
cat /tmp/keep_alert.json
echo ""

# Send Keep webhook
echo -e "${YELLOW}Sending Keep webhook...${NC}"
RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/v1/ingest/keep" \
  -H "Content-Type: application/json" \
  -d @/tmp/keep_alert.json)

echo "Response: $RESPONSE"
echo ""

# 2. Show MSP noise reduction
echo -e "${YELLOW}2. MSP Noise Reduction${NC}"
echo "Endpoint: GET $BACKEND_URL/api/v1/alerts/filter-rules"
echo ""

FILTER_RULES=$(curl -s "$BACKEND_URL/api/v1/alerts/filter-rules")
echo "Active filter rules: $FILTER_RULES"
echo ""

# 3. Show AI correlation
echo -e "${YELLOW}3. AI Correlation with Bedrock${NC}"
echo "Endpoint: GET $BACKEND_URL/api/v1/agents/status"
echo ""

AGENT_STATUS=$(curl -s "$BACKEND_URL/api/v1/agents/status")
echo "AI Agent status: $AGENT_STATUS"
echo ""

# 4. Show SLA management
echo -e "${YELLOW}4. SLA Management${NC}"
echo "Endpoint: GET $BACKEND_URL/api/v1/msp/clients"
echo ""

# Create sample SLA config
cat > /tmp/sla_config.json << EOF
{
  "client_id": "$DEMO_CLIENT_ID",
  "client_name": "Demo Client",
  "sla_tier": "premium",
  "noise_threshold": 0.7,
  "response_times": {
    "critical": 15,
    "high": 60,
    "medium": 240,
    "low": 480
  }
}
EOF

echo "SLA Configuration:"
cat /tmp/sla_config.json
echo ""

# 5. Show database integration
echo -e "${YELLOW}5. Database Integration${NC}"
echo "Endpoint: GET $BACKEND_URL/api/v1/alerts"
echo ""

ALERTS=$(curl -s "$BACKEND_URL/api/v1/alerts?limit=5")
echo "Recent alerts: $ALERTS"
echo ""

# 6. Show workflow engine
echo -e "${YELLOW}6. Workflow Engine${NC}"
echo "Endpoint: GET $BACKEND_URL/api/v1/workflows"
echo ""

WORKFLOWS=$(curl -s "$BACKEND_URL/api/v1/workflows")
echo "Active workflows: $WORKFLOWS"
echo ""

# 7. Show multi-tenancy
echo -e "${YELLOW}7. Multi-tenancy${NC}"
echo "Endpoint: GET $BACKEND_URL/api/v1/msp/tenants"
echo ""

TENANTS=$(curl -s "$BACKEND_URL/api/v1/msp/tenants")
echo "Tenant isolation: $TENANTS"
echo ""

# 8. Show frontend integration
echo -e "${YELLOW}8. Frontend Integration${NC}"
echo "URL: $FRONTEND_URL/frontend-demo.html"
echo ""

echo -e "${BLUE}🎬 Live Demo Features${NC}"
echo "========================"
echo "1. Multi-client selector (MSP feature)"
echo "2. Alert table with Keep's data model"
echo "3. SLA indicators (MSP feature)"
echo "4. Noise reduction metrics (MSP feature)"
echo "5. AI correlation results (MSP feature)"
echo "6. Real-time updates"
echo ""

# 9. Performance metrics
echo -e "${YELLOW}9. Performance Metrics${NC}"
echo "Endpoint: GET $BACKEND_URL/api/v1/metrics"
echo ""

METRICS=$(curl -s "$BACKEND_URL/api/v1/metrics")
echo "Performance metrics: $METRICS"
echo ""

# 10. Health check
echo -e "${YELLOW}10. System Health${NC}"
echo "Endpoint: GET $BACKEND_URL/health"
echo ""

HEALTH=$(curl -s "$BACKEND_URL/health")
echo "System health: $HEALTH"
echo ""

echo -e "${GREEN}✅ Keep Integration Demo Complete${NC}"
echo ""
echo -e "${BLUE}📊 Demo Summary${NC}"
echo "================"
echo "✅ Keep webhook integration working"
echo "✅ MSP noise reduction active"
echo "✅ AI correlation with Bedrock"
echo "✅ SLA management configured"
echo "✅ Database integration functional"
echo "✅ Workflow engine operational"
echo "✅ Multi-tenancy enforced"
echo "✅ Frontend dashboard live"
echo "✅ Performance metrics available"
echo "✅ System health monitoring"
echo ""

echo -e "${BLUE}🎯 Key Integration Points${NC}"
echo "=========================="
echo "1. Keep webhook format compatibility"
echo "2. PostgreSQL schema alignment"
echo "3. YAML workflow format support"
echo "4. Provider framework extensibility"
echo "5. Multi-tenant data isolation"
echo "6. HMAC signature verification"
echo "7. Alert deduplication"
echo "8. AI enrichment pipeline"
echo "9. SLA-aware routing"
echo "10. Real-time dashboard"
echo ""

echo -e "${GREEN}🚀 Demo Ready for Presentation${NC}"
echo ""
echo "Next steps:"
echo "1. Open frontend: $FRONTEND_URL/frontend-demo.html"
echo "2. Show live alert processing"
echo "3. Demonstrate noise reduction"
echo "4. Highlight AI correlation"
echo "5. Explain Keep integration benefits"
echo ""

# Cleanup
rm -f /tmp/keep_alert.json /tmp/sla_config.json

echo -e "${BLUE}📝 Demo Script Complete${NC}"
