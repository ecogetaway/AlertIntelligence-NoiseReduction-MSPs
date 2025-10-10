"""
API Tests for MSP Alert Intelligence Platform
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from demo_main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "mode" in data

def test_get_alerts():
    """Test get alerts endpoint"""
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert isinstance(data["alerts"], list)

def test_get_agents_status():
    """Test agents status endpoint"""
    response = client.get("/api/v1/agents/status")
    assert response.status_code == 200
    data = response.json()
    assert "bedrock_agentcore" in data
    assert "strands_agents" in data

def test_ingest_alerts():
    """Test alert ingestion endpoint"""
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
    data = response.json()
    assert "received" in data
    assert "after_dedup" in data
    assert "after_filter" in data
    assert "agent_processing" in data

def test_acknowledge_alert():
    """Test alert acknowledgment"""
    response = client.post("/api/v1/alerts/alert-1/acknowledge")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_suppress_alert():
    """Test alert suppression"""
    response = client.post("/api/v1/alerts/alert-1/suppress")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_enrich_alert():
    """Test alert enrichment"""
    response = client.post("/api/v1/alerts/alert-1/enrich")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "enrichments_added" in data

def test_deduplicate_alerts():
    """Test alert deduplication"""
    response = client.post("/api/v1/alerts/deduplicate")
    assert response.status_code == 200
    data = response.json()
    assert "unique_alerts" in data
    assert "deduplication_stats" in data

def test_correlate_alerts():
    """Test alert correlation"""
    response = client.post("/api/v1/alerts/correlate")
    assert response.status_code == 200
    data = response.json()
    assert "correlations" in data
    assert "correlation_stats" in data

def test_processing_stats():
    """Test processing statistics endpoint"""
    response = client.get("/api/v1/processing/stats")
    assert response.status_code == 200
    data = response.json()
    # Should return either stats or a message about services not being available
    assert isinstance(data, dict)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "status" in data

def test_incidents_endpoint():
    """Test incidents endpoint"""
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    data = response.json()
    assert "incidents" in data
    assert "total" in data

if __name__ == "__main__":
    pytest.main([__file__])
