# Keep × MSP Alert Intelligence Integration Guide

## Overview

This guide explains how to integrate Keep's alert management platform with your MSP Alert Intelligence backend, combining:
- **Keep**: Provider integrations, alert normalization, workflow engine
- **MSP Backend**: Noise reduction, deduplication, Strands correlation, Bedrock AI triage

Reference: [Keep GitHub](https://github.com/keephq/keep) | [Keep Docs](https://docs.keephq.dev)

## Architecture

```
Providers → Keep Connectors → Keep Alerts/Workflows
                                    ↓
                            Webhook (HMAC signed)
                                    ↓
                        MSP Backend /api/v1/ingest/keep
                                    ↓
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
            Noise Reduction                 Deduplication
            (AlertFilter)                   (Fingerprint)
                    ↓                               ↓
                    └───────────────┬───────────────┘
                                    ↓
                            Strands Correlation
                            (Agent Orchestrator)
                                    ↓
                            Bedrock AI Triage
                            (Severity + Summary)
                                    ↓
                            Persist + Frontend API
```

## Setup Steps

### 1. Configure Keep Provider (in Keep)

Add a webhook provider in Keep to send alerts to your MSP backend:

```yaml
# In Keep: Settings → Providers → Add Webhook Provider
name: msp-backend-webhook
type: webhook
config:
  url: https://your-backend.example.com/api/v1/ingest/keep
  method: POST
  headers:
    Content-Type: application/json
```

### 2. Set HMAC Secret (Both Sides)

**In Keep:**
- Settings → Secrets → Add Secret
- Name: `MSP_WEBHOOK_SECRET`
- Value: Generate a strong secret (e.g., `openssl rand -hex 32`)

**In MSP Backend:**
```bash
# .env
KEEP_WEBHOOK_SECRET=your-secret-here
```

### 3. Deploy Keep Workflow

Copy the workflow from `workflows/keep-to-msp-webhook.yml` to your Keep instance:

```bash
# Using Keep CLI
keep workflow apply -f workflows/keep-to-msp-webhook.yml

# Or via Keep UI
# Workflows → New Workflow → Paste YAML → Save
```

### 4. Configure MSP Backend

Update `.env` with Keep integration settings:

```bash
# Keep Integration
KEEP_API_URL=https://your-keep-instance.com
KEEP_API_KEY=your-keep-api-key
KEEP_WEBHOOK_SECRET=your-webhook-secret

# AWS Bedrock (for AI triage)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

# Strands Agents (for correlation)
STRANDS_AGENTS_ENABLED=true
STRANDS_AGENTS_CONFIG_PATH=./agents/strands_config.yaml

# Alert Processing
ALERT_DEDUPLICATION_WINDOW=300
ALERT_CORRELATION_WINDOW=1800
```

### 5. Start MSP Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend will start on `http://localhost:8000`

## Testing the Integration

### Option 1: Use Test Endpoints

The backend includes test endpoints to simulate Keep webhooks:

```bash
# Get sample payloads
curl http://localhost:8000/api/v1/test/keep-webhook/samples

# Send a test webhook (critical alert)
curl -X POST http://localhost:8000/api/v1/test/keep-webhook/send \
  -H "Content-Type: application/json" \
  -d '{"event": "alert.created", "use_hmac": false, "severity": "critical"}'

# Get cURL examples
curl http://localhost:8000/api/v1/test/keep-webhook/curl
```

### Option 2: Manual cURL Test

```bash
# Without HMAC (for local testing)
curl -X POST http://localhost:8000/api/v1/ingest/keep \
  -H "Content-Type: application/json" \
  -d '{
    "event": "alert.created",
    "alert": {
      "id": "test-alert-001",
      "fingerprint": "test-cpu-high",
      "source": "prometheus",
      "severity": "critical",
      "status": "firing",
      "title": "High CPU usage",
      "labels": {"service": "api", "environment": "production"},
      "annotations": {"summary": "CPU > 90%"},
      "ts": "2025-10-20T10:30:00Z"
    }
  }'
```

### Option 3: Trigger from Keep

1. Create a test alert in Keep (or wait for a real alert)
2. Check Keep workflow logs to verify webhook was sent
3. Check MSP backend logs for processing result

## Data Flow Example

### 1. Keep sends webhook:
```json
{
  "event": "alert.created",
  "alert": {
    "id": "keep-alert-123",
    "fingerprint": "prom-cpu-api-prod",
    "source": "prometheus",
    "severity": "critical",
    "status": "firing",
    "title": "High CPU on API server",
    "labels": {"service": "api", "environment": "production"},
    "ts": "2025-10-20T10:30:00Z"
  }
}
```

### 2. MSP backend processes:

**Noise Reduction:**
- Checks if severity ≥ high (configured in AlertFilter)
- Checks if status = firing
- ✅ Passes filters

**Deduplication:**
- Computes fingerprint: `prometheus:api:High CPU on API server:critical`
- Checks Redis cache for duplicates within 5-minute window
- ✅ Not a duplicate

**Strands Correlation:**
- Runs correlation agents (temporal, topology, etc.)
- Assigns incident ID: `inc-prom-cpu`
- Correlation score: 0.87

**Bedrock AI Triage:**
- Sends to Claude via Bedrock
- Returns:
  - Severity classification: critical
  - Summary: "API server experiencing sustained high CPU. Likely traffic spike or inefficient query."
  - Recommended actions: "1. Check recent deployments, 2. Review slow query logs, 3. Scale horizontally"

### 3. MSP backend response:
```json
{
  "status": "ok",
  "fingerprint": "prom-cpu-api-prod",
  "incident": "inc-prom-cpu"
}
```

### 4. Enriched alert (internal):
```json
{
  "id": "keep-alert-123",
  "fingerprint": "prom-cpu-api-prod",
  "source": "prometheus",
  "severity": "critical",
  "title": "High CPU on API server",
  "correlation": {
    "incidentId": "inc-prom-cpu",
    "score": 0.87,
    "started_at": "2025-10-20T10:30:00Z"
  },
  "ai": {
    "triage": "API server experiencing sustained high CPU. Likely traffic spike or inefficient query. 1. Check recent deployments, 2. Review slow query logs, 3. Scale horizontally"
  }
}
```

## API Endpoints

### Ingest Endpoint
- **URL**: `POST /api/v1/ingest/keep`
- **Auth**: HMAC signature in `X-Keep-Signature` header
- **Body**: Keep webhook payload (see examples above)
- **Response**: `{"status": "ok|filtered|duplicate", "fingerprint": "...", "incident": "..."}`

### Test Endpoints (Development Only)
- `GET /api/v1/test/keep-webhook/samples` - Get sample payloads
- `POST /api/v1/test/keep-webhook/send` - Send test webhook
- `GET /api/v1/test/keep-webhook/curl` - Get cURL examples

### API Documentation
- OpenAPI docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Monitoring & Debugging

### Check Backend Logs

```bash
# Watch logs in real-time
tail -f backend.log

# Look for specific events
grep "alert filtered" backend.log
grep "duplicate" backend.log
grep "correlation" backend.log
```

### Check Keep Workflow Logs

In Keep UI:
- Workflows → `keep-to-msp-webhook` → Execution History
- Look for successful/failed webhook deliveries

### Common Issues

**1. HMAC signature mismatch**
- Verify `KEEP_WEBHOOK_SECRET` matches on both sides
- Check Keep workflow uses correct secret variable
- Ensure no extra whitespace in secret

**2. Webhook not received**
- Verify MSP backend is publicly accessible (or use ngrok for testing)
- Check Keep workflow triggers (filters might be too restrictive)
- Verify Keep provider configuration (URL, headers)

**3. Alerts filtered/duplicated**
- Check `AlertFilter` rules in `backend/services/alert_filter.py`
- Adjust `ALERT_DEDUPLICATION_WINDOW` in `.env`
- Review fingerprint generation logic

**4. Bedrock errors**
- Verify AWS credentials are configured
- Check IAM permissions for Bedrock
- Ensure model ID is correct and available in your region

## Next Steps

### 1. Add Persistence
Currently, enriched alerts are not persisted. Add:
```python
# In ingest_keep.py after enrichment
from services.alert_service import AlertService
alert_service = AlertService(db)
await alert_service.create_alert(enriched)
```

### 2. Bi-directional Sync
Update Keep incidents with MSP enrichments:
```python
# In ingest_keep.py
from services.keep_adapter import update_incident_note
await update_incident_note(
    enriched["correlation"]["incidentId"],
    f"AI Triage: {enriched['ai']['triage']}"
)
```

### 3. Frontend Integration
The frontend already polls `/api/v1/alerts` - it will automatically show enriched alerts with:
- Correlation incident IDs
- AI-generated summaries
- Recommended actions

### 4. Production Deployment
- Deploy Keep and MSP backend in same VPC for lower latency
- Use Redis for deduplication cache (already configured)
- Set up monitoring/alerting for webhook failures
- Configure proper HTTPS/TLS for webhook endpoint

## Example Keep Workflow Variations

### Critical Alerts Only
```yaml
triggers:
  - type: alert
    filters:
      - key: severity
        value: critical
```

### Specific Services
```yaml
triggers:
  - type: alert
    filters:
      - key: labels.service
        value: r"(api|payments|auth)"
        operator: regex
```

### Business Hours Only
```yaml
triggers:
  - type: alert
    filters:
      - key: timestamp
        value: "9-17"  # 9 AM - 5 PM
        operator: time_range
```

## References

- **Keep Documentation**: https://docs.keephq.dev
- **Keep GitHub**: https://github.com/keephq/keep
- **Keep Workflows**: https://docs.keephq.dev/workflows
- **Keep Providers**: https://docs.keephq.dev/providers
- **AWS Bedrock**: https://aws.amazon.com/bedrock
- **Strands Agents**: (Add your Strands docs link)

## Support

- **Keep Community**: https://slack.keephq.dev
- **MSP Backend Issues**: GitHub Issues on your repo
- **Integration Questions**: Open a discussion in Keep Slack #integrations channel

