"""
Keep → MSP webhook endpoint

Accepts Keep workflow webhooks on alert events, performs MSP noise reduction,
deduplication, correlation (Strands), and AI triage/summarization (Bedrock).
"""

from __future__ import annotations

import hmac
import hashlib
import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request, Depends
from sqlmodel import Session

from core.config import settings
from core.database import get_db
from services.alert_filter import AlertFilter
from services.alert_deduplicator import AlertDeduplicator
from agents.strands_orchestrator import correlate_with_agents
from services.bedrock_client import summarize_and_triage
from services.keep_client import KeepClient
from models.alert import Alert, AlertCreate, AlertEnrichment, AlertSeverity, AlertStatus, AlertSource


logger = logging.getLogger(__name__)
router = APIRouter()

_filter_engine = AlertFilter()
_deduper = AlertDeduplicator(window_minutes=int(settings.ALERT_DEDUPLICATION_WINDOW // 60))


def _verify_hmac_signature(request: Request, raw_body: bytes) -> None:
    """Verify webhook HMAC signature if secret is configured.

    Supports common header names: 'X-Keep-Signature' or 'X-Hub-Signature-256'.
    Signature format expected: 'sha256=<hexdigest>'.
    """
    secret = settings.KEEP_WEBHOOK_SECRET
    if not secret:
        # No secret configured → accept (useful for local dev)
        return

    provided = (
        request.headers.get("X-Keep-Signature")
        or request.headers.get("X-Hub-Signature-256")
        or ""
    )
    if not provided.startswith("sha256="):
        raise HTTPException(status_code=401, detail="invalid signature header")

    expected = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(provided.split("=", 1)[1], expected):
        raise HTTPException(status_code=401, detail="signature mismatch")


def _passes_filters(alert: Dict[str, Any]) -> bool:
    """Run alert through active filter rules.

    We reuse AlertFilter's single-rule application by synthesizing an AND across
    configured rules. If no rules exist, accept by default.
    """
    rules = _filter_engine.get_rules()
    if not rules:
        return True
    return all(_filter_engine.apply_filter(alert, r) for r in rules)


@router.post("/ingest/keep")
async def ingest_keep(request: Request, db: Session = Depends(get_db)):
    raw = await request.body()
    _verify_hmac_signature(request, raw)

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")

    event = payload.get("event")
    if event not in {"alert.created", "alert.updated"}:
        raise HTTPException(status_code=400, detail="unsupported event")

    alert_data = payload.get("alert") or {}

    # Noise reduction
    if not _passes_filters(alert_data):
        logger.info("alert filtered", extra={"fingerprint": alert_data.get("fingerprint")})
        return {"status": "filtered"}

    # Deduplication
    fingerprint = _deduper.generate_fingerprint(
        {
            "source": alert_data.get("source", "unknown"),
            "service": (alert_data.get("labels") or {}).get("service") or alert_data.get("service", "unknown"),
            "name": alert_data.get("title") or alert_data.get("name") or "Alert",
            "severity": alert_data.get("severity", "unknown"),
        }
    )
    alert_data["fingerprint"] = alert_data.get("fingerprint") or fingerprint
    if _deduper.is_duplicate(alert_data, alert_data["fingerprint"]):
        return {"status": "duplicate"}

    # Correlation (Strands agents)
    correlated = await correlate_with_agents(alert_data)

    # AI triage/summarization (Bedrock)
    enriched = await summarize_and_triage(correlated)

    # Persist to database
    try:
        # Map Keep alert to our AlertCreate model
        from datetime import datetime
        alert_create = AlertCreate(
            title=enriched.get("title") or enriched.get("name") or "Alert from Keep",
            description=(enriched.get("annotations") or {}).get("summary") or enriched.get("description") or "",
            severity=AlertSeverity(enriched.get("severity", "medium").lower()),
            status=AlertStatus.ACTIVE if enriched.get("status") == "firing" else AlertStatus.RESOLVED,
            source=AlertSource.CUSTOM,  # Map to specific source if needed
            source_id=str(enriched.get("id", "")),
            fingerprint=enriched["fingerprint"],
            labels=enriched.get("labels") or {},
            annotations=enriched.get("annotations") or {},
            started_at=enriched.get("started_at") or enriched.get("ts") or datetime.utcnow().isoformat()
        )
        
        # Create alert in database
        db_alert = Alert(**alert_create.dict())
        db.add(db_alert)
        
        # Add enrichments from AI and correlation
        if enriched.get("ai"):
            ai_enrichment = AlertEnrichment(
                alert_id=db_alert.id,
                key="ai_triage",
                value=str(enriched["ai"].get("triage", "")),
                source="bedrock_ai"
            )
            db.add(ai_enrichment)
        
        if enriched.get("correlation"):
            corr_enrichment = AlertEnrichment(
                alert_id=db_alert.id,
                key="correlation",
                value=str(enriched["correlation"]),
                source="strands_agents"
            )
            db.add(corr_enrichment)
        
        db.commit()
        db.refresh(db_alert)
        
        logger.info("alert persisted", extra={
            "alert_id": str(db_alert.id),
            "fingerprint": db_alert.fingerprint,
            "incident": (enriched.get("correlation") or {}).get("incidentId")
        })
        
        return {
            "status": "ok",
            "alert_id": str(db_alert.id),
            "fingerprint": enriched.get("fingerprint"),
            "incident": (enriched.get("correlation") or {}).get("incidentId")
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to persist alert: {e}")
        # Return success for webhook but log error
        return {
            "status": "ok",
            "fingerprint": enriched.get("fingerprint"),
            "incident": (enriched.get("correlation") or {}).get("incidentId"),
            "warning": "alert processed but not persisted"
        }


