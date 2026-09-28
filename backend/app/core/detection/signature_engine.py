import re

from app.core.detection.normalizer import normalize_text
from app.core.detection.signatures import SIGNATURES


def detect_signatures(text: str) -> dict:
    """
    Detect known prompt-injection patterns.

    Returns a structured detection result.
    """

    normalized_text = normalize_text(text)

    matches = []

    for category, patterns in SIGNATURES.items():

        for pattern in patterns:

            if re.search(pattern, normalized_text):

                matches.append({
                    "category": category,
                    "pattern": pattern
                })

    return {
        "detected": len(matches) > 0,
        "matches": matches,
        "normalized_text": normalized_text
    }