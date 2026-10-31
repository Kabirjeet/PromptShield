import re
from typing import Any, Dict, List

from app.core.detection.heuristics import (
    DIRECTIVE_WORDS,
    HEURISTIC_DESCRIPTIONS,
    HEURISTIC_PATTERNS,
    HEURISTIC_WEIGHTS,
)


def detect_heuristics(normalized_text: str, raw_text: str = "") -> Dict[str, Any]:
    """
    Evaluates normalized and raw prompt text against rule-based security heuristics.

    Args:
        normalized_text (str): Pre-processed canonical lowercase prompt text.
        raw_text (str, optional): Original user input string for obfuscation checks.

    Returns:
        Dict[str, Any]: Structured dictionary containing:
            - detected (bool): True if any heuristic signals were triggered.
            - heuristics (List[Dict[str, Any]]): List of triggered heuristic detail objects.
    """
    if not raw_text:
        raw_text = normalized_text

    triggered: List[Dict[str, Any]] = []
    triggered_names: set[str] = set()

    if not normalized_text:
        return {
            "detected": False,
            "heuristics": []
        }

    # 1. Pattern-based heuristics
    for name, patterns in HEURISTIC_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, normalized_text):
                if name not in triggered_names:
                    triggered_names.add(name)
                    triggered.append({
                        "type": "heuristic",
                        "name": name,
                        "weight": HEURISTIC_WEIGHTS[name],
                        "description": HEURISTIC_DESCRIPTIONS[name]
                    })
                break

    # 2. Directive Density Heuristic
    words = normalized_text.split()
    total_words = len(words)
    if total_words > 0:
        directive_count = sum(1 for w in words if w.strip(".,!?:;\"'()[]{}") in DIRECTIVE_WORDS)
        # Trigger if directive density is suspiciously high (e.g., >= 4 directives in short prompt or >= 5 overall)
        if (directive_count >= 4 and (directive_count / total_words) >= 0.15) or directive_count >= 5:
            if "directive_density" not in triggered_names:
                triggered_names.add("directive_density")
                triggered.append({
                    "type": "heuristic",
                    "name": "directive_density",
                    "weight": HEURISTIC_WEIGHTS["directive_density"],
                    "description": HEURISTIC_DESCRIPTIONS["directive_density"]
                })

    # 3. Obfuscation Signal Heuristic
    # Check for suspicious special character sequences (e.g., 5+ consecutive symbols)
    has_symbol_burst = bool(re.search(r"[\!\@\#\$\%\^\&\*\(\)\_\+\=\{\}\[\]\:\"\'\<\>\?\,\.\/\\\|\~\-]{5,}", raw_text))
    # Check for unusually long continuous non-space tokens (> 50 chars) without normal URLs
    has_unusually_long_token = any(len(token) > 50 and not token.startswith("http") for token in raw_text.split())
    # Check for high ratio of unusual non-ASCII characters
    non_ascii_count = sum(1 for char in raw_text if ord(char) > 127)
    high_non_ascii = len(raw_text) > 20 and (non_ascii_count / len(raw_text)) > 0.35

    if has_symbol_burst or has_unusually_long_token or high_non_ascii:
        if "obfuscation_signal" not in triggered_names:
            triggered_names.add("obfuscation_signal")
            triggered.append({
                "type": "heuristic",
                "name": "obfuscation_signal",
                "weight": HEURISTIC_WEIGHTS["obfuscation_signal"],
                "description": HEURISTIC_DESCRIPTIONS["obfuscation_signal"]
            })

    # 4. Prompt Structure Anomaly Heuristic
    # Trigger if multiple distinct text heuristics (e.g., override + system ref or roleplay + extraction) coincide
    if len(triggered_names) >= 2:
        if "prompt_structure_anomaly" not in triggered_names:
            triggered_names.add("prompt_structure_anomaly")
            triggered.append({
                "type": "heuristic",
                "name": "prompt_structure_anomaly",
                "weight": HEURISTIC_WEIGHTS["prompt_structure_anomaly"],
                "description": HEURISTIC_DESCRIPTIONS["prompt_structure_anomaly"]
            })

    return {
        "detected": len(triggered) > 0,
        "heuristics": triggered
    }
