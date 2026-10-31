"""
Severity classification module for PromptShield AI.

Classifies risk scores into explainable severity levels:
- 0: SAFE
- 1-24: LOW
- 25-49: MEDIUM
- 50-74: HIGH
- 75-100: CRITICAL
"""

SAFE_MAX = 0
LOW_MAX = 24
MEDIUM_MAX = 49
HIGH_MAX = 74

SEVERITY_SAFE = "SAFE"
SEVERITY_LOW = "LOW"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_HIGH = "HIGH"
SEVERITY_CRITICAL = "CRITICAL"


def classify_severity(risk_score: int) -> str:
    """
    Classifies a numerical risk score into a security severity category.

    Args:
        risk_score (int): Risk score bounded between 0 and 100.

    Returns:
        str: One of "SAFE", "LOW", "MEDIUM", "HIGH", or "CRITICAL".
    """
    if risk_score <= SAFE_MAX:
        return SEVERITY_SAFE
    elif risk_score <= LOW_MAX:
        return SEVERITY_LOW
    elif risk_score <= MEDIUM_MAX:
        return SEVERITY_MEDIUM
    elif risk_score <= HIGH_MAX:
        return SEVERITY_HIGH
    else:
        return SEVERITY_CRITICAL
