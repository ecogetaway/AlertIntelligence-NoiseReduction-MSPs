"""
Phase 1 Smoke Tests for MSP Alert Intelligence Platform
Tests critical Phase 1 features: Correlation, Incidents, AI, Workflows, Analytics
"""

import pytest
import httpx
import asyncio

BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_health_check():
    """Test that the API is running"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_correlation_endpoint():
    """Test alert correlation endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/v1/alerts/correlate")
        assert response.status_code == 200
        data = response.json()
        assert "correlations" in data
        assert "correlation_stats" in data
        # Should find at least one correlation in demo data
        assert data["correlation_stats"]["total_alerts"] > 0


@pytest.mark.asyncio
async def test_incident_creation_from_correlation():
    """Test creating an incident from correlated alerts"""
    async with httpx.AsyncClient() as client:
        # Create incident from demo alert IDs
        payload = {
            "alert_ids": ["alert-1", "alert-2"],
            "title": "Test Incident from Correlation",
            "description": "Smoke test incident"
        }
        response = await client.post(
            f"{BASE_URL}/api/v1/incidents/from-correlation",
            json=payload
        )
        assert response.status_code == 200
        data = response.json()
        assert "incident" in data
        incident = data["incident"]
        assert incident["title"] == "Test Incident from Correlation"
        assert "alert-1" in incident["alerts"]
        assert "alert-2" in incident["alerts"]
        # Should have AI summary (even if simulated)
        assert "ai_summary" in incident or "ai_analysis" in incident
        
        # Test incident lifecycle update
        incident_id = incident["id"]
        update_payload = {"status": "resolved"}
        response = await client.patch(
            f"{BASE_URL}/api/v1/incidents/{incident_id}",
            json=update_payload
        )
        assert response.status_code == 200
        data = response.json()
        assert data["incident"]["status"] == "resolved"


@pytest.mark.asyncio
async def test_workflows_list():
    """Test listing available workflows"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/workflows")
        assert response.status_code == 200
        data = response.json()
        assert "workflows" in data
        workflows = data["workflows"]
        # Should load workflows from the workflows/ directory
        assert len(workflows) > 0
        # Check workflow structure
        if workflows:
            wf = workflows[0]
            assert "id" in wf
            assert "name" in wf


@pytest.mark.asyncio
async def test_workflow_execution():
    """Test executing a workflow"""
    async with httpx.AsyncClient() as client:
        # First, get a workflow ID
        response = await client.get(f"{BASE_URL}/api/v1/workflows")
        workflows = response.json()["workflows"]
        
        if not workflows:
            pytest.skip("No workflows available")
        
        workflow_id = workflows[0]["id"]
        
        # Execute the workflow with a test alert
        payload = {
            "workflow_id": workflow_id,
            "trigger_event": {
                "id": "test-alert-1",
                "title": "Test Alert for Workflow",
                "severity": "high",
                "source": "test"
            },
            "context": {"test": True}
        }
        
        response = await client.post(
            f"{BASE_URL}/api/v1/workflows/execute",
            json=payload
        )
        assert response.status_code == 200
        data = response.json()
        assert "workflow_id" in data
        assert "status" in data
        assert data["status"] in ["success", "partial_failure", "failed"]
        assert "steps_executed" in data


@pytest.mark.asyncio
async def test_processing_stats():
    """Test analytics/processing stats endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/processing/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_alerts" in data
        assert "active_alerts" in data
        assert "incidents" in data
        assert "noise_reduction_rate" in data
        # Noise reduction should be a percentage
        assert 0 <= data["noise_reduction_rate"] <= 100


@pytest.mark.asyncio
async def test_ai_integration():
    """Test AI integration (checks if it works with or without real API key)"""
    async with httpx.AsyncClient() as client:
        # Try to enrich an alert (which should use AI if available)
        response = await client.post(f"{BASE_URL}/api/v1/alerts/alert-1/enrich")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "enrichments_added" in data


@pytest.mark.asyncio
async def test_agent_status():
    """Test that AI agents are initialized"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/agents/status")
        assert response.status_code == 200
        data = response.json()
        assert "bedrock_agentcore" in data
        assert "strands_agents" in data


if __name__ == "__main__":
    # Run tests
    print("Running Phase 1 Smoke Tests...")
    print("\n=== Starting Test Suite ===\n")
    
    asyncio.run(test_health_check())
    print("✓ Health check passed")
    
    asyncio.run(test_correlation_endpoint())
    print("✓ Correlation endpoint passed")
    
    asyncio.run(test_incident_creation_from_correlation())
    print("✓ Incident creation and lifecycle passed")
    
    asyncio.run(test_workflows_list())
    print("✓ Workflows listing passed")
    
    asyncio.run(test_workflow_execution())
    print("✓ Workflow execution passed")
    
    asyncio.run(test_processing_stats())
    print("✓ Processing stats passed")
    
    asyncio.run(test_ai_integration())
    print("✓ AI integration passed")
    
    asyncio.run(test_agent_status())
    print("✓ Agent status passed")
    
    print("\n=== All Phase 1 Smoke Tests Passed! ===\n")

