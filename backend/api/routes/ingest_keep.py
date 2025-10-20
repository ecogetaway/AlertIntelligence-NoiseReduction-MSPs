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

from fastapi import APIRouter, HTTPException, Request

from core.config import settings
from services.alert_filter import AlertFilter
from services.alert_deduplicator import AlertDeduplicator
from agents.strands_orchestrator import correlate_with_agents
from services.bedrock_client import summarize_and_triage


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
async def ingest_keep(request: Request):
    raw = await request.body()
    _verify_hmac_signature(request, raw)

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")

    event = payload.get("event")
    if event not in {"alert.created", "alert.updated"}:
        raise HTTPException(status_code=400, detail="unsupported event")

    alert = payload.get("alert") or {}

    # Noise reduction
    if not _passes_filters(alert):
        logger.info("alert filtered", extra={"fingerprint": alert.get("fingerprint")})
        return {"status": "filtered"}

    # Deduplication
    fingerprint = _deduper.generate_fingerprint(
        {
            "source": alert.get("source", "unknown"),
            "service": (alert.get("labels") or {}).get("service") or alert.get("service", "unknown"),
            "name": alert.get("title") or alert.get("name") or "Alert",
            "severity": alert.get("severity", "unknown"),
        }
    )
    alert["fingerprint"] = alert.get("fingerprint") or fingerprint
    if _deduper.is_duplicate(alert, alert["fingerprint"]):
        return {"status": "duplicate"}

    # Correlation (Strands agents)
    correlated = await correlate_with_agents(alert)

    # AI triage/summarization (Bedrock)
    enriched = await summarize_and_triage(correlated)

    # TODO: persist enriched alert/incident and/or write back to Keep via adapter
    # This is intentionally left minimal to keep MVP wiring focused.

    return {"status": "ok", "fingerprint": enriched.get("fingerprint"), "incident": (enriched.get("correlation") or {}).get("incidentId")}


