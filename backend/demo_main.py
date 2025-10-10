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
    """Correlate alerts (simulated)"""
    return {
        "correlations": [
            {
                "alert1_id": "alert-1",
                "alert2_id": "alert-2",
                "correlation_type": "temporal",
                "confidence": 0.85,
                "reason": "Alerts occurred within 2 minutes on same server"
            }
        ],
        "correlation_stats": {
            "total_alerts": len(demo_alerts),
            "correlations_found": 1,
            "correlation_rate": 0.33
        }
    }

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
    if not orchestrator:
        return {"message": "Processing services not available"}
    
    stats = orchestrator.get_processing_stats()
    return {
        "orchestrator_stats": stats,
        "deduplicator_stats": deduplicator.get_cache_stats() if deduplicator else {},
        "filter_stats": filter_engine.get_filter_stats(demo_alerts) if filter_engine else {},
        "websocket_connections": len(manager.active_connections)
    }

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "demo_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
