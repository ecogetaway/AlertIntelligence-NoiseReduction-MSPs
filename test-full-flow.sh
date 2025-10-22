#!/bin/bash

# Test the complete Keep → Backend → Frontend flow
# This script sends a test alert and verifies it was processed

set -e

API_BASE="http://localhost:8000"

echo "🧪 Testing MSP Alert Intelligence - Full Flow"
echo "=============================================="
echo ""

# Check if backend is running
echo "1️⃣ Checking backend health..."
HEALTH=$(curl -s "$API_BASE/health" || echo "FAILED")

if [[ "$HEALTH" == "FAILED" ]]; then
    echo "❌ Backend not running at $API_BASE"
    echo "   Run: ./test-backend-locally.sh"
    exit 1
fi

echo "✅ Backend is healthy"
echo ""

# Send test alert
echo "2️⃣ Sending test alert via Keep webhook..."
RESPONSE=$(curl -s -X POST "$API_BASE/api/v1/test/keep-webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "alert.created",
    "alert": {
      "id": "test-cpu-spike-001",
      "title": "High CPU Usage - Production Server",
      "name": "cpu_usage_high",
      "description": "CPU usage exceeded 90% for 5 minutes",
      "severity": "high",
      "source": "prometheus",
      "service": "api-server",
      "status": "firing",
      "labels": {
        "host": "prod-api-01",
        "environment": "production",
        "team": "platform"
      },
      "annotations": {
        "runbook": "https://wiki.company.com/runbooks/high-cpu",
        "dashboard": "https://grafana.company.com/d/cpu"
      }
    }
  }')

echo "Response: $RESPONSE"
echo ""

# Check if alert was processed
if echo "$RESPONSE" | grep -q '"status":"ok"'; then
    echo "✅ Alert processed successfully"
    
    # Extract alert ID if present
    ALERT_ID=$(echo "$RESPONSE" | grep -o '"alert_id":"[^"]*"' | cut -d'"' -f4 || echo "")
    
    if [[ -n "$ALERT_ID" ]]; then
        echo "   Alert ID: $ALERT_ID"
    fi
    
    FINGERPRINT=$(echo "$RESPONSE" | grep -o '"fingerprint":"[^"]*"' | cut -d'"' -f4 || echo "")
    if [[ -n "$FINGERPRINT" ]]; then
        echo "   Fingerprint: $FINGERPRINT"
    fi
    
    INCIDENT=$(echo "$RESPONSE" | grep -o '"incident":"[^"]*"' | cut -d'"' -f4 || echo "")
    if [[ -n "$INCIDENT" ]]; then
        echo "   Incident: $INCIDENT"
    fi
else
    echo "⚠️  Alert processing response: $RESPONSE"
fi

echo ""

# Query alerts
echo "3️⃣ Fetching all alerts from API..."
ALERTS=$(curl -s "$API_BASE/api/v1/alerts")

# Count alerts
ALERT_COUNT=$(echo "$ALERTS" | grep -o '"total":[0-9]*' | cut -d':' -f2 || echo "0")
echo "✅ Found $ALERT_COUNT alert(s) in system"
echo ""

# Show recent alerts (first 3)
echo "4️⃣ Recent alerts:"
echo "$ALERTS" | python3 -m json.tool 2>/dev/null | head -50 || echo "$ALERTS"

echo ""
echo "=============================================="
echo "✅ Full flow test complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Open frontend-demo.html in browser"
echo "   2. Check alerts display with enrichments"
echo "   3. Verify AI triage and correlation data"
echo ""

