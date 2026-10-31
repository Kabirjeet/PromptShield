
from typing import Any, Dict


# Initial default policy. These rules can be made configurable later.
SEVERITY_ACTIONS = {
    "SAFE": "ALLOW",
    "LOW": "ALLOW",
    "MEDIUM": "FLAG",
    "HIGH": "BLOCK",
    "CRITICAL": "BLOCK",
}


def evaluate_policy(analysis: Dict[str, Any]) -> Dict[str, str]:
    """
    Convert a detection result into an enforcement decision.

    Unknown or malformed severity values fail closed.
    """
    severity = analysis.get("severity")

    if not isinstance(severity, str):
        severity = ""

    severity = severity.upper()
    action = SEVERITY_ACTIONS.get(severity, "BLOCK")

    reasons = {
        "ALLOW": f"Severity {severity}: request permitted by policy.",
        "FLAG": "Medium-risk request flagged for review.",
        "BLOCK": (
            f"Severity {severity or 'UNKNOWN'}: request blocked by policy."
        ),
    }

    return {
        "action": action,
        "policy_reason": reasons[action],
    }


def apply_policy(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Return the original analysis result with its policy decision."""
    result = dict(analysis)
    result.update(evaluate_policy(analysis))
    return result
