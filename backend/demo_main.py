"""
MSP Alert Intelligence & Noise Reduction Platform - Demo Version
Simplified main application entry point for demo purposes
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, Any
from datetime import datetime
import json

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
from uuid import uuid4
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Global agent managers (simulated)
bedrock_manager = None
strands_manager = None
orchestrator = None
deduplicator = None
filter_engine = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown"""
    global bedrock_manager, strands_manager, orchestrator, deduplicator, filter_engine
    
    logger.info("Starting MSP Alert Intelligence Platform (Demo Mode)")
    
    # Initialize AI client
    try:
        from ai.ai_client import get_ai_client
        ai_client = get_ai_client()
        logger.info(f"AI Client initialized: provider={ai_client.provider}, real={ai_client.is_real}")
    except Exception as e:
        logger.warning(f"Could not initialize AI client: {e}")
    
    # Initialize workflow executor
    try:
        from workflows.workflow_executor import get_workflow_executor
        workflow_executor = get_workflow_executor()
        logger.info(f"Workflow Executor initialized with {len(workflow_executor.workflows)} workflows")
    except Exception as e:
        logger.warning(f"Could not initialize Workflow Executor: {e}")
    
    # Initialize simulated agents
    bedrock_manager = {
        "initialized": True,
        "agents": {
            "alert_correlation_agent": {"name": "Alert Correlation Agent", "status": "active"},
            "alert_enrichment_agent": {"name": "Alert Enrichment Agent", "status": "active"},
            "incident_creation_agent": {"name": "Incident Creation Agent", "status": "active"},
            "noise_reduction_agent": {"name": "Noise Reduction Agent", "status": "active"}
        }
    }
    
    strands_manager = {
        "initialized": True,
        "agents": {
            "multi_step_processor": {"name": "Multi-Step Alert Processor", "status": "active"},
            "infrastructure_drift_detector": {"name": "Infrastructure Drift Detector", "status": "active"},
            "ai_summarization_agent": {"name": "AI Summarization Agent", "status": "active"},
            "automated_remediation_agent": {"name": "Automated Remediation Agent", "status": "active"}
        }
    }
    
    # Initialize processing services
    try:
        from services.alert_deduplicator import AlertDeduplicator
        from services.alert_filter import AlertFilter
        from agents.agent_orchestrator import AgentOrchestrator
        
        deduplicator = AlertDeduplicator()
        filter_engine = AlertFilter()
        orchestrator = AgentOrchestrator(bedrock_manager, strands_manager)
        
        logger.info("Processing services initialized successfully")
    except ImportError as e:
        logger.warning(f"Could not import processing services: {e}")
        logger.info("Running in basic demo mode without advanced processing")
    
    logger.info("Demo agents initialized successfully")
    
    yield
    
    # Cleanup
    logger.info("Shutting down MSP Alert Intelligence Platform")

# Create FastAPI application
app = FastAPI(
    title="MSP Alert Intelligence Platform (Demo)",
    description="Alert Intelligence & Noise Reduction for Managed Service Providers - Demo Version",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Demo data
demo_alerts = [
    {
        "id": "alert-1",
        "title": "High CPU Usage on Server-01",
        "description": "CPU usage has exceeded 90% for the past 5 minutes",
        "severity": "high",
        "status": "active",
        "source": "prometheus",
        "source_id": "cpu_usage_high",
        "fingerprint": "cpu-high-server01",
        "labels": {"instance": "server-01", "job": "node_exporter"},
        "annotations": {"summary": "High CPU usage detected"},
        "started_at": "2024-01-15T10:30:00Z",
        "created_at": "2024-01-15T10:30:00Z",
        "enrichments": [
            {"key": "ai_summary", "value": "AI detected potential performance bottleneck", "source": "ai_agent"},
            {"key": "similar_incidents", "value": "3 similar incidents in past 30 days", "source": "ai_agent"}
        ],
        "correlations": [
            {"correlated_alert_id": "alert-2", "correlation_type": "temporal", "confidence": 0.85}
        ]
    },
    {
        "id": "alert-2",
        "title": "Memory Usage Critical on Server-01",
        "description": "Memory usage has reached 95% capacity",
        "severity": "critical",
        "status": "active",
        "source": "prometheus",
        "source_id": "memory_usage_critical",
        "fingerprint": "memory-critical-server01",
        "labels": {"instance": "server-01", "job": "node_exporter"},
        "annotations": {"summary": "Critical memory usage detected"},
        "started_at": "2024-01-15T10:32:00Z",
        "created_at": "2024-01-15T10:32:00Z",
        "enrichments": [
            {"key": "ai_summary", "value": "AI detected memory leak pattern", "source": "ai_agent"},
            {"key": "recommended_actions", "value": "Restart application, check for memory leaks", "source": "ai_agent"}
        ],
        "correlations": [
            {"correlated_alert_id": "alert-1", "correlation_type": "temporal", "confidence": 0.85}
        ]
    },
    {
        "id": "alert-3",
        "title": "Database Connection Pool Exhausted",
        "description": "All database connections are in use",
        "severity": "critical",
        "status": "acknowledged",
        "source": "datadog",
        "source_id": "db_pool_exhausted",
        "fingerprint": "db-pool-exhausted",
        "labels": {"service": "database", "environment": "production"},
        "annotations": {"summary": "Database connection pool exhausted"},
        "started_at": "2024-01-15T10:35:00Z",
        "created_at": "2024-01-15T10:35:00Z",
        "enrichments": [
            {"key": "ai_summary", "value": "AI detected database performance issue", "source": "ai_agent"},
            {"key": "root_cause", "value": "Likely caused by long-running queries", "source": "ai_agent"}
        ],
        "correlations": []
    }
]

demo_incidents = [
    {
        "id": "incident-1",
        "title": "Server-01 Performance Degradation",
        "description": "Multiple performance alerts on Server-01",
        "status": "investigating",
        "priority": "p2",
        "incident_type": "infrastructure",
        "assignee": "john.doe@msp.com",
        "tags": ["performance", "server-01", "critical"],
        "started_at": "2024-01-15T10:30:00Z",
        "created_at": "2024-01-15T10:30:00Z",
        "ai_summary": "AI analysis indicates potential memory leak causing CPU and memory issues",
        "ai_root_cause": "Application memory leak detected in production environment",
        "ai_impact_assessment": "High impact - affects user experience and system stability",
        "ai_recommendations": "1. Restart application services 2. Investigate memory leak 3. Scale resources if needed",
        "alerts": ["alert-1", "alert-2"]
    }
]

@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "name": "MSP Alert Intelligence Platform (Demo)",
        "version": "1.0.0",
        "status": "operational",
        "mode": "demo",
        "features": [
            "Alert Deduplication (Simulated)",
            "Smart Filtering (Simulated)", 
            "Correlation Analysis (Simulated)",
            "Agentic AI Processing (Simulated)",
            "Real-time Dashboards",
            "Automated Workflows (Simulated)"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "simulated",
        "bedrock_agentcore": "simulated",
        "strands_agents": "simulated",
        "mode": "demo"
    }

@app.get("/api/v1/alerts")
async def list_alerts(
    page: int = 1,
    page_size: int = 20,
    severity: str = None,
    status: str = None,
    source: str = None,
    search: str = None
):
    """List alerts with filtering"""
    alerts = demo_alerts.copy()
    
    # Apply filters
    if severity:
        alerts = [a for a in alerts if a["severity"] == severity]
    if status:
        alerts = [a for a in alerts if a["status"] == status]
    if source:
        alerts = [a for a in alerts if a["source"] == source]
    if search:
        alerts = [a for a in alerts if search.lower() in a["title"].lower() or search.lower() in a["description"].lower()]
    
    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated_alerts = alerts[start:end]
    
    return {
        "alerts": paginated_alerts,
        "total": len(alerts),
        "page": page,
        "page_size": page_size,
        "has_next": end < len(alerts),
        "has_previous": page > 1
    }

@app.get("/api/v1/alerts/{alert_id}")
async def get_alert(alert_id: str):
    """Get a specific alert by ID"""
    alert = next((a for a in demo_alerts if a["id"] == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@app.post("/api/v1/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str, user: str = "demo-user"):
    """Acknowledge an alert"""
    alert = next((a for a in demo_alerts if a["id"] == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert["status"] = "acknowledged"
    alert["annotations"]["acknowledged_by"] = user
    alert["annotations"]["acknowledged_at"] = datetime.utcnow().isoformat()
    
    return {"message": "Alert acknowledged successfully"}

@app.post("/api/v1/alerts/{alert_id}/suppress")
async def suppress_alert(alert_id: str, reason: str = "Demo suppression"):
    """Suppress an alert"""
    alert = next((a for a in demo_alerts if a["id"] == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert["status"] = "suppressed"
    alert["annotations"]["suppression_reason"] = reason
    alert["annotations"]["suppressed_at"] = datetime.utcnow().isoformat()
    
    return {"message": "Alert suppressed successfully"}

@app.get("/api/v1/incidents")
async def list_incidents():
    """List incidents"""
    return {
        "incidents": demo_incidents,
        "total": len(demo_incidents)
    }

@app.get("/api/v1/agents/status")
async def agents_status():
    """Get status of all AI agents"""
    return {
        "bedrock_agentcore": {
            "initialized": bedrock_manager["initialized"],
            "agents_count": len(bedrock_manager["agents"]),
            "agents": list(bedrock_manager["agents"].keys()),
            "status": "simulated"
        },
        "strands_agents": {
            "initialized": strands_manager["initialized"],
            "agents_count": len(strands_manager["agents"]),
            "agents": list(strands_manager["agents"].keys()),
            "status": "simulated"
        }
    }

@app.post("/api/v1/alerts/deduplicate")
async def deduplicate_alerts():
    """Deduplicate alerts (simulated)"""
    return {
        "unique_alerts": demo_alerts,
        "duplicate_alerts": [],
        "deduplication_stats": {
            "total_alerts": len(demo_alerts),
            "unique_alerts": len(demo_alerts),
            "duplicates_removed": 0
        }
    }

@app.post("/api/v1/alerts/correlate")
async def correlate_alerts():
    """Correlate alerts using simple demo rules.

    Rules:
    - Same source AND same labels.instance (if present)
    - Started within 10 minutes of each other
    """
    def parse_dt(s: str) -> datetime:
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return datetime.utcnow()

    window_minutes = 10
    correlations: List[Dict[str, Any]] = []
    alerts = demo_alerts
    for i in range(len(alerts)):
        for j in range(i + 1, len(alerts)):
            a = alerts[i]
            b = alerts[j]
            same_source = a.get("source") == b.get("source")
            same_instance = a.get("labels", {}).get("instance") and a.get("labels", {}).get("instance") == b.get("labels", {}).get("instance")

            if not (same_source and same_instance):
                continue

            t1 = parse_dt(a.get("started_at", a.get("created_at", "")))
            t2 = parse_dt(b.get("started_at", b.get("created_at", "")))
            within_window = abs((t2 - t1).total_seconds()) <= window_minutes * 60

            if within_window:
                correlations.append({
                    "alert1_id": a["id"],
                    "alert2_id": b["id"],
                    "correlation_type": "temporal+entity",
                    "confidence": 0.85,
                    "reason": f"Same source and instance within {window_minutes}m"
                })

    return {
        "correlations": correlations,
        "correlation_stats": {
            "total_alerts": len(alerts),
            "correlations_found": len(correlations),
            "correlation_rate": round(len(correlations) / max(1, len(alerts)), 2)
        }
    }

class CorrelationToIncidentRequest(BaseModel):
    alert_ids: List[str]
    title: str | None = None
    description: str | None = None

@app.post("/api/v1/incidents/from-correlation")
async def create_incident_from_correlation(payload: CorrelationToIncidentRequest):
    """Create an incident from a set of correlated alert IDs with AI summary."""
    if not payload.alert_ids:
        raise HTTPException(status_code=400, detail="alert_ids is required")

    related_alerts = [a for a in demo_alerts if a["id"] in payload.alert_ids]
    if not related_alerts:
        raise HTTPException(status_code=404, detail="No matching alerts found")

    incident_id = f"incident-{uuid4().hex[:8]}"
    title = payload.title or (related_alerts[0]["title"] + " (Correlated)")
    description = payload.description or "Created from correlated alerts"

    incident = {
        "id": incident_id,
        "title": title,
        "description": description,
        "status": "open",
        "priority": "p2",
        "incident_type": "infrastructure",
        "assignee": None,
        "tags": ["correlated", "ai-enhanced"],
        "started_at": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "alerts": payload.alert_ids,
    }
    
    # Generate AI summary
    try:
        from ai.ai_client import get_ai_client
        ai_client = get_ai_client()
        ai_summary = await ai_client.incident_summary(incident, related_alerts)
        incident.update(ai_summary)
        logger.info(f"AI summary generated for incident {incident_id}")
    except Exception as e:
        logger.warning(f"Could not generate AI summary: {e}")
        incident["ai_summary"] = "[Simulated] Incident involving multiple correlated alerts"
    
    demo_incidents.append(incident)

    # Annotate alerts with incident id
    for a in demo_alerts:
        if a["id"] in payload.alert_ids:
            a.setdefault("annotations", {})["incident_id"] = incident_id

    return {"incident": incident}

class IncidentUpdateRequest(BaseModel):
    status: str

@app.patch("/api/v1/incidents/{incident_id}")
async def update_incident(incident_id: str, payload: IncidentUpdateRequest):
    """Update incident status (open, investigating, resolved, closed)."""
    incident = next((i for i in demo_incidents if i["id"] == incident_id), None)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident["status"] = payload.status
    incident["updated_at"] = datetime.utcnow().isoformat()
    if payload.status in {"resolved", "closed"}:
        incident["resolved_at"] = datetime.utcnow().isoformat()
    return {"incident": incident}

@app.post("/api/v1/alerts/{alert_id}/enrich")
async def enrich_alert(alert_id: str):
    """Enrich an alert with AI (simulated)"""
    alert = next((a for a in demo_alerts if a["id"] == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Simulate AI enrichment
    new_enrichments = [
        {"key": "ai_analysis", "value": "AI detected potential performance bottleneck", "source": "ai_agent"},
        {"key": "recommended_actions", "value": "Check application logs, restart if necessary", "source": "ai_agent"},
        {"key": "similar_incidents", "value": "2 similar incidents in past week", "source": "ai_agent"}
    ]
    
    alert["enrichments"].extend(new_enrichments)
    
    return {
        "message": "Alert enrichment completed",
        "enrichments_added": len(new_enrichments),
        "confidence": 0.92
    }

# WebSocket endpoint for real-time updates
@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time alert updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Send periodic updates every 10 seconds
            await asyncio.sleep(10)
            
            # Get current stats
            active_alerts = len([a for a in demo_alerts if a["status"] == "active"])
            total_alerts = len(demo_alerts)
            
            # Send update
            update_data = {
                "type": "alert_update",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "total_alerts": total_alerts,
                    "active_alerts": active_alerts,
                    "agent_status": "processing",
                    "connections": len(manager.active_connections)
                }
            }
            
            await manager.send_personal_message(json.dumps(update_data), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# New API Models
class AlertIngestRequest(BaseModel):
    name: str
    description: str
    severity: str
    source: str
    service: str
    labels: Dict[str, str] = {}
    annotations: Dict[str, str] = {}

# Enhanced API endpoints with new processing pipeline
@app.post("/api/alerts/ingest")
async def ingest_alerts(alerts: List[AlertIngestRequest]):
    """Ingest and process alerts through the enhanced pipeline"""
    if not deduplicator or not filter_engine or not orchestrator:
        # Fallback to basic processing if services not available
        return {
            "received": len(alerts),
            "after_dedup": len(alerts),
            "after_filter": len(alerts),
            "agent_processing": {"message": "Basic processing mode"},
            "noise_reduction_rate": 0
        }
    
    # Convert to dict format
    alert_dicts = [alert.dict() for alert in alerts]
    
    # Add IDs and timestamps
    for alert in alert_dicts:
        alert["id"] = f"alert_{datetime.utcnow().timestamp()}"
        alert["created_at"] = datetime.utcnow().isoformat()
        alert["status"] = "active"
    
    # Phase 1: Deduplication
    unique_alerts = deduplicator.deduplicate_batch(alert_dicts)
    
    # Phase 2: Filtering
    filtered_alerts = filter_engine.filter_alerts(unique_alerts)
    
    # Phase 3: AI Processing
    agent_results = await orchestrator.process_alert_pipeline(filtered_alerts)
    
    # Calculate noise reduction
    noise_reduction_rate = (1 - len(unique_alerts) / len(alert_dicts)) * 100 if alert_dicts else 0
    
    # Broadcast update to WebSocket clients
    if manager.active_connections:
        update_data = {
            "type": "batch_processed",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "received": len(alert_dicts),
                "processed": len(filtered_alerts),
                "noise_reduction": noise_reduction_rate
            }
        }
        await manager.broadcast(json.dumps(update_data))
    
    return {
        "received": len(alert_dicts),
        "after_dedup": len(unique_alerts),
        "after_filter": len(filtered_alerts),
        "agent_processing": agent_results,
        "noise_reduction_rate": noise_reduction_rate
    }

@app.get("/api/v1/processing/stats")
async def get_processing_stats():
    """Get processing statistics"""
    active_count = len([a for a in demo_alerts if a["status"] == "active"])
    suppressed_count = len([a for a in demo_alerts if a["status"] == "suppressed"])
    
    base_stats = {
        "total_alerts": len(demo_alerts),
        "active_alerts": active_count,
        "suppressed_alerts": suppressed_count,
        "incidents": len(demo_incidents),
        "websocket_connections": len(manager.active_connections),
        "noise_reduction_rate": round((suppressed_count / max(1, len(demo_alerts))) * 100, 2)
    }
    
    if orchestrator:
        stats = orchestrator.get_processing_stats()
        base_stats.update({
            "orchestrator_stats": stats,
            "deduplicator_stats": deduplicator.get_cache_stats() if deduplicator else {},
            "filter_stats": filter_engine.get_filter_stats(demo_alerts) if filter_engine else {}
        })
    
    return base_stats

# Workflow API Endpoints
@app.get("/api/v1/workflows")
async def list_workflows():
    """List all available workflows"""
    try:
        from workflows.workflow_executor import get_workflow_executor
        executor = get_workflow_executor()
        return {"workflows": executor.list_workflows()}
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        return {"workflows": [], "error": str(e)}

@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get a specific workflow by ID"""
    try:
        from workflows.workflow_executor import get_workflow_executor
        executor = get_workflow_executor()
        workflow = executor.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return {"workflow": workflow}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class WorkflowExecuteRequest(BaseModel):
    workflow_id: str
    trigger_event: Dict[str, Any]
    context: Dict[str, Any] | None = None

@app.post("/api/v1/workflows/execute")
async def execute_workflow(payload: WorkflowExecuteRequest):
    """Execute a workflow with a given trigger event (for testing/demo)"""
    try:
        from workflows.workflow_executor import get_workflow_executor
        executor = get_workflow_executor()
        result = await executor.execute_workflow(
            payload.workflow_id,
            payload.trigger_event,
            payload.context
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "demo_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
