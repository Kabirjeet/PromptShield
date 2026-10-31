import re
from typing import Any, Dict, List

from app.core.detection.heuristics import HEURISTIC_PATTERNS
from app.core.detection.heuristic_engine import detect_heuristics
from app.core.detection.normalizer import normalize_text
from app.core.detection.signatures import SIGNATURES
from app.core.risk.scorer import calculate_risk
from app.core.risk.severity import classify_severity


def detect_raw_signatures(text: str) -> Dict[str, Any]:
    """
    Detect known prompt-injection patterns in normalized text.

    Args:
        text (str): Raw user prompt input.

    Returns:
        Dict[str, Any]: Object containing normalized_text and raw signature matches.
    """
    normalized_text = normalize_text(text)
    matches: List[Dict[str, str]] = []

    if not normalized_text:
        return {
            "matches": matches,
            "normalized_text": ""
        }

    for category, patterns in SIGNATURES.items():
        for pattern in patterns:
            if re.search(pattern, normalized_text):
                matches.append({
                    "type": "signature",
                    "category": category,
                    "pattern": pattern
                })

    return {
        "matches": matches,
        "normalized_text": normalized_text
    }


def analyze_prompt(text: str) -> Dict[str, Any]:
    """
    Complete Phase 3.3 detection pipeline:
    1. Normalization
    2. Signature Detection
    3. Heuristic Detection
    4. Risk Scoring (with deduplication)
    5. Severity Classification

    Args:
        text (str): Input prompt string.

    Returns:
        Dict[str, Any]: Full structured security assessment result.
    """
    raw_detection = detect_raw_signatures(text)
    matches = raw_detection["matches"]
    normalized_text = raw_detection["normalized_text"]

    # Run heuristic engine
    heuristic_result = detect_heuristics(normalized_text, raw_text=text)
    heuristics = heuristic_result["heuristics"]

    # Calculate combined risk score
    risk_info = calculate_risk(matches, heuristics)
    risk_score = risk_info["risk_score"]
    categories = risk_info["categories"]
    reasons = risk_info["reasons"]
    active_heuristics = risk_info["heuristics"]

    # Classify security severity
    severity = classify_severity(risk_score)

    is_detected = (len(matches) > 0) or (len(active_heuristics) > 0)

    return {
        "detected": is_detected,
        "risk_score": risk_score,
        "severity": severity,
        "categories": categories,
        "matches": matches,
        "heuristics": active_heuristics,
        "reasons": reasons,
        "normalized_text": normalized_text
    }


def detect_signatures(text: str) -> Dict[str, Any]:
    """
    Legacy wrapper for detect_signatures, returning the complete detection pipeline result.
    """
    return analyze_prompt(text)