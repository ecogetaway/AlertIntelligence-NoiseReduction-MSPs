<!-- 660271c7-bc07-4b46-8cdc-8a0a6cba39b5 1d0dbb63-f81c-4c8d-abfb-322614c27e7f -->
# Claude Prototype Integration Plan

## Analysis Summary

After comparing the Claude prototype files with your current Cursor codebase, I've identified several valuable improvements and features to integrate.

### Key Differences Found:

**Claude Prototype Strengths:**

- More comprehensive alert processing pipeline (deduplication, filtering, correlation)
- Better structured data models with dataclasses
- Fingerprint-based deduplication logic
- Real-time WebSocket support
- More sophisticated agent orchestration with multi-phase processing
- Production-ready deployment configs (Terraform, Makefile, proper Docker setup)
- Superior React UI with better component structure

**Your Current Cursor Codebase Strengths:**

- Working demo mode (no database required)
- Simpler startup scripts
- Standalone HTML demo for hackathons
- Already pushed to GitHub

## Integration Steps

### Phase 1: Backend Enhancements (High Priority)

#### 1.1 Add Alert Deduplication Logic

**File**: `backend/services/alert_deduplicator.py` (new file)

Add the fingerprint-based deduplication from Claude prototype:

```python
from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib
from models.alert import Alert

class AlertDeduplicator:
    """Handles alert deduplication logic"""
    
    def __init__(self, window_minutes: int = 5):
        self.alert_cache = defaultdict(list)
        self.window = timedelta(minutes=window_minutes)
    
    def generate_fingerprint(self, alert: Alert) -> str:
        """Generate unique fingerprint for deduplication"""
        key = f"{alert.source}:{alert.service}:{alert.name}:{alert.severity}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def is_duplicate(self, alert: Alert, fingerprint: str) -> bool:
        """Check if alert is duplicate within time window"""
        now = datetime.now()
        
        # Clean old alerts from cache
        self.alert_cache[fingerprint] = [
            cached_time for cached_time in self.alert_cache[fingerprint]
            if now - cached_time < self.window
        ]
        
        # Check if duplicate exists
        if self.alert_cache[fingerprint]:
            return True
        
        # Add to cache
        self.alert_cache[fingerprint].append(now)
        return False
```

#### 1.2 Add Alert Filtering Engine

**File**: `backend/services/alert_filter.py` (new file)

Implement rule-based filtering from Claude:

```python
from typing import List, Dict, Any
import re

class AlertFilter:
    """Handles alert filtering based on rules"""
    
    def __init__(self):
        self.rules = []
        self.load_default_rules()
    
    def load_default_rules(self):
        """Load default filtering rules"""
        self.rules = [
            {"field": "severity", "operator": "in", "value": ["critical", "high"]},
            {"field": "status", "operator": "equals", "value": "active"},
        ]
    
    def add_rule(self, rule: Dict[str, Any]):
        """Add a filtering rule"""
        self.rules.append(rule)
    
    def apply_filter(self, alert_dict: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        """Apply single filter rule to alert"""
        field = rule["field"]
        operator = rule["operator"]
        value = rule["value"]
        
        alert_value = alert_dict.get(field)
        
        if operator == "equals":
            return alert_value == value
        elif operator == "in":
            return alert_value in value
        elif operator == "not_in":
            return alert_value not in value
        elif operator == "regex":
            return re.match(value, str(alert_value)) is not None
        
        return True
    
    def filter_alerts(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter alerts based on all rules"""
        filtered = []
        for alert in alerts:
            if all(self.apply_filter(alert, rule) for rule in self.rules):
                filtered.append(alert)
        return filtered
```

#### 1.3 Improve Agent Orchestrator

**File**: `backend/agents/agent_orchestrator.py` (new file)

Add multi-phase processing pipeline from Claude:

```python
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """Orchestrate multiple agents for complex tasks"""
    
    def __init__(self, bedrock_manager, strands_manager):
        self.bedrock_manager = bedrock_manager
        self.strands_manager = strands_manager
    
    async def process_alert_pipeline(self, alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process alerts through multi-phase agent pipeline"""
        results = {
            "processed": 0,
            "correlations": [],
            "automations": [],
            "phases": []
        }
        
        # Phase 1: Enrichment
        logger.info(f"Phase 1: Processing {len(alerts)} alerts for enrichment")
        for alert in alerts:
            # Simulate enrichment
            alert["enrichments"] = alert.get("enrichments", [])
            alert["enrichments"].append({
                "key": "ai_processed",
                "value": "true",
                "timestamp": "2024-10-10T10:00:00Z"
            })
            results["processed"] += 1
        
        results["phases"].append({"phase": "enrichment", "status": "completed"})
        
        # Phase 2: Correlation
        logger.info("Phase 2: Running correlation analysis")
        # Group alerts by service for correlation
        service_groups = {}
        for alert in alerts:
            service = alert.get("source", "unknown")
            if service not in service_groups:
                service_groups[service] = []
            service_groups[service].append(alert["id"])
        
        for service, alert_ids in service_groups.items():
            if len(alert_ids) >= 2:
                results["correlations"].append({
                    "service": service,
                    "alert_count": len(alert_ids),
                    "confidence": 0.85
                })
        
        results["phases"].append({"phase": "correlation", "status": "completed"})
        
        # Phase 3: Critical alert analysis with Bedrock
        logger.info("Phase 3: Bedrock analysis for critical alerts")
        critical_alerts = [a for a in alerts if a.get("severity") == "critical"]
        
        for alert in critical_alerts:
            # Simulate Bedrock analysis
            analysis = {
                "alert_id": alert["id"],
                "analysis": f"AI detected critical issue with {alert.get('title', 'Unknown')}",
                "recommendations": [
                    "Check system logs",
                    "Review recent changes",
                    "Alert on-call team"
                ],
                "auto_remediation": False  # Don't auto-fix critical issues
            }
            
            # Phase 4: Automation for non-critical
            if alert.get("severity") != "critical":
                results["automations"].append({
                    "alert_id": alert["id"],
                    "workflow_triggered": "auto-ack-workflow",
                    "status": "initiated"
                })
        
        results["phases"].append({"phase": "bedrock_analysis", "status": "completed"})
        results["phases"].append({"phase": "automation", "status": "completed"})
        
        return results
```

#### 1.4 Add WebSocket Support

**File**: Update `backend/demo_main.py`

Add WebSocket endpoint for real-time updates:

```python
from fastapi import WebSocket
import asyncio

@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time alert updates"""
    await websocket.accept()
    logger.info("WebSocket client connected")
    
    try:
        while True:
            # Send periodic updates
            await asyncio.sleep(5)
            await websocket.send_json({
                "type": "alert_update",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "total_alerts": len(demo_alerts),
                    "active_alerts": len([a for a in demo_alerts if a["status"] == "active"]),
                    "agent_status": "processing"
                }
            })
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        logger.info("WebSocket client disconnected")
```

#### 1.5 Enhance API Endpoints

**File**: Update `backend/demo_main.py`

Add batch ingestion endpoint from Claude:

```python
from pydantic import BaseModel
from typing import List

class AlertIngestRequest(BaseModel):
    name: str
    description: str
    severity: str
    source: str
    service: str
    labels: Dict[str, str] = {}
    annotations: Dict[str, str] = {}

@app.post("/api/alerts/ingest")
async def ingest_alerts(alerts: List[AlertIngestRequest]):
    """Ingest and process alerts through the pipeline"""
    from services.alert_deduplicator import AlertDeduplicator
    from services.alert_filter import AlertFilter
    from agents.agent_orchestrator import AgentOrchestrator
    
    # Initialize processors
    deduplicator = AlertDeduplicator()
    filter_engine = AlertFilter()
    orchestrator = AgentOrchestrator(bedrock_manager, strands_manager)
    
    # Convert to dict format
    alert_dicts = [alert.dict() for alert in alerts]
    
    # Add IDs and fingerprints
    for alert in alert_dicts:
        alert["id"] = f"alert_{datetime.utcnow().timestamp()}"
        alert["fingerprint"] = deduplicator.generate_fingerprint(alert)
    
    # Deduplication
    unique_alerts = [
        a for a in alert_dicts 
        if not deduplicator.is_duplicate(a, a["fingerprint"])
    ]
    
    # Filtering
    filtered_alerts = filter_engine.filter_alerts(unique_alerts)
    
    # AI Processing
    agent_results = await orchestrator.process_alert_pipeline(filtered_alerts)
    
    return {
        "received": len(alert_dicts),
        "after_dedup": len(unique_alerts),
        "after_filter": len(filtered_alerts),
        "agent_processing": agent_results,
        "noise_reduction_rate": (1 - len(unique_alerts) / len(alert_dicts)) * 100 if alert_dicts else 0
    }
```

### Phase 2: Frontend Improvements (Medium Priority)

#### 2.1 Enhance Frontend with WebSocket Support

**File**: `frontend/app/page.tsx`

Add real-time WebSocket updates:

```typescript
'use client';

import { useState, useEffect } from 'react';
import AlertCard from '@/components/alert-card';
import { Alert } from '@/types';

const useWebSocket = (url: string) => {
  const [data, setData] = useState<any>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(url);
    
    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setData(data);
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };
    
    return () => ws.close();
  }, [url]);

  return { data, isConnected };
};

export default function Home() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const { data: wsData, isConnected } = useWebSocket('ws://localhost:8000/ws/alerts');

  // Update alerts when WebSocket data arrives
  useEffect(() => {
    if (wsData) {
      console.log('Real-time update:', wsData);
      // Fetch updated alerts
      fetchAlerts();
    }
  }, [wsData]);

  // Rest of component...
}
```

#### 2.2 Add Better Stat Cards

**File**: `frontend/components/stat-card.tsx` (new file)

```typescript
import { ReactNode } from 'react';
import { TrendingUp } from 'lucide-react';

interface StatCardProps {
  icon: ReactNode;
  label: string;
  value: number | string;
  change?: number;
  color: string;
}

export default function StatCard({ icon, label, value, change, color }: StatCardProps) {
  return (
    <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <div className={`p-3 rounded-lg ${color} bg-opacity-10`}>
            {icon}
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-600">{label}</p>
            <p className="text-2xl font-semibold text-gray-900">{value}</p>
          </div>
        </div>
        {change && (
          <div className="flex items-center text-sm">
            <TrendingUp className="w-4 h-4 mr-1 text-green-500" />
            <span className="text-green-600">{change}%</span>
          </div>
        )}
      </div>
    </div>
  );
}
```

### Phase 3: Deployment & Infrastructure (Low Priority)

#### 3.1 Add Makefile for Easy Commands

**File**: `Makefile` (new file at root)

```makefile
.PHONY: help demo run test clean

help:
	@echo "MSP Alert Intelligence Platform - Commands"
	@echo "=========================================="
	@echo "make demo        - Run frontend demo"
	@echo "make demo-backend - Run backend demo"
	@echo "make demo-full   - Run both frontend and backend"
	@echo "make test        - Run tests"
	@echo "make clean       - Clean up resources"

demo:
	@echo "Starting frontend demo..."
	./start-demo-safe.sh

demo-backend:
	@echo "Starting backend demo..."
	./start-demo.sh

demo-full:
	@echo "Starting full demo (backend + frontend)..."
	cd backend && source venv/bin/activate && python demo_main.py &
	sleep 2
	python3 -m http.server 3000

test:
	@echo "Running tests..."
	cd tests && npx playwright test

clean:
	@echo "Cleaning up..."
	pkill -f "python demo_main.py" || true
	pkill -f "http.server" || true
```

#### 3.2 Improve Docker Compose

**File**: Update `docker-compose.yml`

Add proper health checks and dependencies:

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - DATABASE_URL=${DATABASE_URL:-postgresql://postgres:postgres@db:5432/alerts}
      - REDIS_URL=${REDIS_URL:-redis://redis:6379}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    command: uvicorn demo_main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=alerts
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

### Phase 4: Testing & Documentation (Low Priority)

#### 4.1 Add API Tests

**File**: `tests/test_api.py` (new file)

```python
import pytest
from fastapi.testclient import TestClient
from backend.demo_main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_alerts():
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    assert "alerts" in response.json()

def test_ingest_alerts():
    alerts = [
        {
            "name": "Test Alert",
            "description": "Test description",
            "severity": "high",
            "source": "test",
            "service": "api"
        }
    ]
    response = client.post("/api/alerts/ingest", json=alerts)
    assert response.status_code == 200
    assert "received" in response.json()
```

## Summary of Changes

### Files to Create:

1. `backend/services/alert_deduplicator.py` - Fingerprint-based deduplication
2. `backend/services/alert_filter.py` - Rule-based filtering
3. `backend/agents/agent_orchestrator.py` - Multi-phase processing
4. `frontend/components/stat-card.tsx` - Reusable stat cards
5. `Makefile` - Easy command shortcuts
6. `tests/test_api.py` - API unit tests

### Files to Modify:

1. `backend/demo_main.py` - Add WebSocket, batch ingestion, orchestrator integration
2. `frontend/app/page.tsx` - Add WebSocket support for real-time updates
3. `docker-compose.yml` - Add health checks and better configuration
4. `backend/requirements.txt` - Add `pytest` for testing

### Beginner-Friendly Notes:

- Start with Phase 1.1 and 1.2 (deduplication and filtering) - these are standalone and easy to test
- Test each new file individually before integrating
- The WebSocket feature (1.4, 2.1) is optional for hackathon - skip if short on time
- Phase 3 (deployment) can be skipped for hackathon demo
- Focus on Phase 1 backend improvements for maximum impact

### Integration Priority:

1. **High**: Alert deduplication and filtering (Phase 1.1-1.2)
2. **High**: Agent orchestrator improvements (Phase 1.3)
3. **Medium**: Batch ingestion API (Phase 1.5)
4. **Medium**: WebSocket support (Phase 1.4, 2.1)
5. **Low**: Deployment configs (Phase 3)
6. **Low**: Testing (Phase 4)