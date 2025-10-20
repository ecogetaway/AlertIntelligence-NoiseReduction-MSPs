"""Test endpoint for Keep webhook integration.

Provides sample payloads and a test route to simulate Keep → MSP webhook flow.
"""

from __future__ import annotations

import json
import hmac
import hashlib
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class TestWebhookRequest(BaseModel):
    """Request to send a test webhook"""
    event: str = "alert.created"
    use_hmac: bool = False
    severity: str = "critical"


# Sample Keep alert payloads
SAMPLE_ALERTS = {
    "critical_prometheus": {
        "event": "alert.created",
        "alert": {
            "id": "keep-alert-abc123",
            "fingerprint": "prom-cpu-high-api",
            "source": "prometheus",
            "severity": "critical",
            "status": "firing",
            "title": "High CPU usage on API server",
            "labels": {
                "service": "api",
                "environment": "production",
                "instance": "api-01",
                "alertname": "HighCPUUsage"
            },
            "annotations": {
                "summary": "CPU usage above 90% for 5 minutes",
                "description": "API server api-01 has CPU usage at 94%",
                "runbook_url": "https://runbooks.example.com/high-cpu"
            },
            "ts": "2025-10-20T10:30:00Z",
            "started_at": "2025-10-20T10:25:00Z"
        }
    },
    "high_datadog": {
        "event": "alert.created",
        "alert": {
            "id": "keep-alert-def456",
            "fingerprint": "dd-memory-high-db",
            "source": "datadog",
            "severity": "high",
            "status": "firing",
            "title": "High memory usage on database",
            "labels": {
                "service": "postgres",
                "environment": "production",
                "host": "db-primary-01"
            },
            "annotations": {
                "summary": "Memory usage above 85%",
                "description": "Database server db-primary-01 memory at 87%"
            },
            "ts": "2025-10-20T10:35:00Z",
            "started_at": "2025-10-20T10:30:00Z"
        }
    },
    "medium_sentry": {
        "event": "alert.updated",
        "alert": {
            "id": "keep-alert-ghi789",
            "fingerprint": "sentry-error-rate-payments",
            "source": "sentry",
            "severity": "medium",
            "status": "firing",
            "title": "Error rate spike in payments service",
            "labels": {
                "service": "payments",
                "environment": "production",
                "project": "payments-api"
            },
            "annotations": {
                "summary": "Error rate increased by 300%",
                "description": "Payments API showing 45 errors/min vs baseline 15/min"
            },
            "ts": "2025-10-20T10:40:00Z",
            "started_at": "2025-10-20T10:35:00Z"
        }
    }
}


def _compute_hmac(payload: Dict[str, Any], secret: str) -> str:
    """Compute HMAC signature for Keep webhook."""
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={signature}"


@router.get("/test/keep-webhook/samples")
async def get_sample_payloads():
    """Get sample Keep webhook payloads for testing."""
    return {
        "samples": SAMPLE_ALERTS,
        "description": "Sample Keep webhook payloads for different alert types",
        "usage": "POST these to /api/v1/ingest/keep to test the pipeline"
    }


@router.post("/test/keep-webhook/send")
async def send_test_webhook(request: TestWebhookRequest):
    """Send a test webhook to the ingest endpoint.
    
    This simulates what Keep would send when an alert is created/updated.
    """
    import httpx
    from core.config import settings
    
    # Select sample based on severity
    sample_key = {
        "critical": "critical_prometheus",
        "high": "high_datadog",
        "medium": "medium_sentry"
    }.get(request.severity, "critical_prometheus")
    
    payload = SAMPLE_ALERTS[sample_key].copy()
    payload["event"] = request.event
    
    # Prepare headers
    headers = {"Content-Type": "application/json"}
    
    if request.use_hmac and settings.KEEP_WEBHOOK_SECRET:
        signature = _compute_hmac(payload, settings.KEEP_WEBHOOK_SECRET)
        headers["X-Keep-Signature"] = signature
    
    # Send to ingest endpoint
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/api/v1/ingest/keep",
                json=payload,
                headers=headers,
                timeout=10.0
            )
            return {
                "status": "sent",
                "response_status": response.status_code,
                "response_body": response.json() if response.status_code == 200 else response.text,
                "payload": payload,
                "headers": headers
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send test webhook: {str(e)}")


@router.get("/test/keep-webhook/curl")
async def get_curl_example():
    """Get cURL examples for testing the Keep webhook endpoint."""
    from core.config import settings
    
    sample = SAMPLE_ALERTS["critical_prometheus"]
    payload_json = json.dumps(sample, indent=2)
    
    # Basic example without HMAC
    basic_curl = f"""# Basic test (no HMAC verification)
curl -X POST http://localhost:8000/api/v1/ingest/keep \\
  -H "Content-Type: application/json" \\
  -d '{payload_json}'
"""
    
    # Example with HMAC
    if settings.KEEP_WEBHOOK_SECRET:
        signature = _compute_hmac(sample, settings.KEEP_WEBHOOK_SECRET)
        hmac_curl = f"""# With HMAC verification
curl -X POST http://localhost:8000/api/v1/ingest/keep \\
  -H "Content-Type: application/json" \\
  -H "X-Keep-Signature: {signature}" \\
  -d '{payload_json}'
"""
    else:
        hmac_curl = "# Set KEEP_WEBHOOK_SECRET in .env to generate HMAC example"
    
    return {
        "basic": basic_curl,
        "with_hmac": hmac_curl,
        "note": "Replace localhost:8000 with your actual backend URL"
    }

