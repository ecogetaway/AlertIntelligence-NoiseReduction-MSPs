"""
Keep API client for fetching alerts/incidents and mapping them to local models.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple

import httpx


class KeepClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or os.getenv("KEEP_API_URL") or "").rstrip("/")
        self.api_key = api_key or os.getenv("KEEP_API_KEY")

    def is_configured(self) -> bool:
        return bool(self.base_url)

    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def fetch_alerts(self, *, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch alerts from Keep. Endpoint may vary by Keep version; try common paths.
        """
        if not self.is_configured():
            return []

        candidate_paths = [
            "/api/alerts",           # hypothetical
            "/alerts",               # hypothetical
            "/v1/alerts",            # hypothetical
        ]
        async with httpx.AsyncClient(timeout=10.0) as client:
            for path in candidate_paths:
                try:
                    resp = await client.get(
                        f"{self.base_url}{path}", headers=self._headers(), params=params or {}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        # Normalize to list
                        if isinstance(data, dict) and "alerts" in data:
                            return data["alerts"]  # type: ignore[return-value]
                        if isinstance(data, list):
                            return data
                except Exception:
                    continue
        return []

    @staticmethod
    def map_keep_alert(keep_alert: Dict[str, Any]) -> Dict[str, Any]:
        """Map a Keep alert dict to our API AlertResponse-like dict.
        Uses best-effort field extraction with safe fallbacks.
        """
        # Common field candidates
        id_val = keep_alert.get("id") or keep_alert.get("_id") or keep_alert.get("fingerprint")
        title = keep_alert.get("title") or keep_alert.get("name") or keep_alert.get("summary") or "Alert"
        description = keep_alert.get("description") or keep_alert.get("details") or ""
        severity = (keep_alert.get("severity") or "medium").lower()
        status = (keep_alert.get("status") or keep_alert.get("state") or "active").lower()
        source = (
            keep_alert.get("source")
            or keep_alert.get("provider")
            or keep_alert.get("generatorURL")
            or "custom"
        )
        source_id = str(keep_alert.get("source_id") or keep_alert.get("fingerprint") or id_val or "")
        fingerprint = str(keep_alert.get("fingerprint") or id_val or source_id)
        labels = keep_alert.get("labels") or keep_alert.get("tags") or {}
        annotations = keep_alert.get("annotations") or {}
        started_at = (
            keep_alert.get("started_at")
            or keep_alert.get("startsAt")
            or keep_alert.get("timestamp")
            or keep_alert.get("createdAt")
            or keep_alert.get("updatedAt")
            or ""
        )
        created_at = keep_alert.get("createdAt") or started_at or ""

        return {
            "id": id_val or fingerprint or source_id,
            "title": title,
            "description": description,
            "severity": severity,
            "status": status,
            "source": str(source).split("/")[-1] if isinstance(source, str) else "custom",
            "source_id": source_id,
            "fingerprint": fingerprint,
            "labels": labels if isinstance(labels, dict) else {},
            "annotations": annotations if isinstance(annotations, dict) else {},
            "started_at": started_at or created_at or "",
            "updated_at": keep_alert.get("updatedAt"),
            "resolved_at": keep_alert.get("resolvedAt"),
            "created_at": created_at or started_at or "",
            "enrichments": [],
            "correlations": [],
            "incident_id": keep_alert.get("incident_id"),
        }

    @staticmethod
    def apply_filters(
        alerts: List[Dict[str, Any]],
        *,
        severity: Optional[str],
        status: Optional[str],
        source: Optional[str],
        search: Optional[str],
    ) -> List[Dict[str, Any]]:
        def match(a: Dict[str, Any]) -> bool:
            if severity and str(a.get("severity", "")).lower() != severity.lower():
                return False
            if status and str(a.get("status", "")).lower() != status.lower():
                return False
            if source and str(a.get("source", "")).lower() != source.lower():
                return False
            if search:
                text = f"{a.get('title','')} {a.get('description','')} {a.get('source','')}"
                if search.lower() not in text.lower():
                    return False
            return True

        return [a for a in alerts if match(a)]


