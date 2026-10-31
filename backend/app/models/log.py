from datetime import datetime, timezone
from typing import Any


def build_audit_event(
    analysis: dict[str, Any],
    user_id: str,
) -> dict[str, Any]:
    """Build a privacy-conscious audit event without storing prompt text."""
    return {
        "user_id": user_id,
        "timestamp": datetime.now(timezone.utc),
        "detected": bool(analysis.get("detected", False)),
        "risk_score": int(analysis.get("risk_score", 0)),
        "severity": str(analysis.get("severity", "UNKNOWN")),
        "categories": list(analysis.get("categories", [])),
        "action": str(analysis.get("action", "BLOCK")),
        "policy_reason": str(analysis.get("policy_reason", "")),
    }
