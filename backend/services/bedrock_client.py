"""Amazon Bedrock runtime wrappers for triage and summarization.

This is a thin adapter; prompt/response parsing can be improved iteratively.
"""

from __future__ import annotations

import json
import os
from typing import Dict, Any

import boto3


MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def _client():
    return boto3.client("bedrock-runtime", region_name=AWS_REGION)


def _prompt(alert: Dict[str, Any]) -> str:
    base = {
        "fingerprint": alert.get("fingerprint"),
        "severity": alert.get("severity"),
        "status": alert.get("status"),
        "title": alert.get("title") or alert.get("name"),
        "labels": alert.get("labels", {}),
        "annotations": alert.get("annotations", {}),
        "source": alert.get("source"),
    }
    return (
        "You are an SRE triage assistant.\n"
        "Given this alert, 1) classify severity (low|medium|high|critical), "
        "2) provide a 1-2 line summary, and 3) list 2-3 remediation steps.\n"
        f"Alert JSON: {json.dumps(base)[:3500]}\n"
    )


async def summarize_and_triage(alert: Dict[str, Any]) -> Dict[str, Any]:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.2,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": _prompt(alert)}]}
        ],
    }

    try:
        resp = _client().invoke_model(modelId=MODEL_ID, body=json.dumps(body))
        payload = json.loads(resp["body"].read())
        text = ""
        try:
            text = payload.get("content", [{}])[0].get("text", "")
        except Exception:
            text = json.dumps(payload)[:800]

        out = dict(alert)
        out.setdefault("ai", {})
        out["ai"].update({
            "triage": text[:1200]
        })
        return out
    except Exception:
        # Non-fatal; return original alert
        return alert


