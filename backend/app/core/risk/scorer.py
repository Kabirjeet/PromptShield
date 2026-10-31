"""
Risk scoring module for PromptShield AI.

Calculates explainable risk scores combining signature detections and heuristic signals.
"""

from typing import Any, Dict, List, Optional

# Category weight definitions for security risk assessment (Signature Detection)
CATEGORY_WEIGHTS: Dict[str, int] = {
    "prompt_override": 25,
    "system_prompt_extraction": 35,
    "role_manipulation": 20,
    "jailbreak": 40,
}

DEFAULT_CATEGORY_WEIGHT: int = 20

# Deterministic explanations for signature categories
CATEGORY_REASONS: Dict[str, str] = {
    "prompt_override": "Prompt attempts to override previous instructions",
    "system_prompt_extraction": "Prompt attempts to extract the system prompt",
    "role_manipulation": "Prompt attempts to manipulate the AI model's role or persona",
    "jailbreak": "Prompt attempts to bypass safety rules or restrictions",
}

# Overlap mapping between signature categories and heuristic signals for deduplication
SIGNATURE_HEURISTIC_OVERLAPS: Dict[str, List[str]] = {
    "prompt_override": ["instruction_override_language"],
    "system_prompt_extraction": ["prompt_extraction_language"],
    "jailbreak": ["roleplay_escalation"],
}

# Bonus for multi-signal attack vectors to reflect compound risk
MULTI_CATEGORY_BONUS: int = 10

# Maximum upper bound for risk score
MAX_RISK_SCORE: int = 100


def calculate_risk(
    matches: List[Dict[str, Any]],
    heuristics: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Calculates an explainable risk score, list of categories, reasons, and active heuristics.

    Args:
        matches (List[Dict[str, Any]]): Signature match objects.
        heuristics (Optional[List[Dict[str, Any]]]): Heuristic signal objects.

    Returns:
        Dict[str, Any]: Object containing:
            - risk_score (int): Score bounded between 0 and 100.
            - categories (List[str]): Unique detected signature categories.
            - heuristics (List[Dict[str, Any]]): Triggered heuristic objects.
            - reasons (List[Dict[str, Any]]): List of explanation dicts (category, weight, reason).
    """
    if heuristics is None:
        heuristics = []

    if not matches and not heuristics:
        return {
            "risk_score": 0,
            "categories": [],
            "heuristics": [],
            "reasons": []
        }

    # 1. Process Signature Categories
    unique_categories: List[str] = list(
        dict.fromkeys(
            m["category"] for m in matches if isinstance(m, dict) and "category" in m
        )
    )

    reasons: List[Dict[str, Any]] = []
    base_score: int = 0
    covered_heuristics: set[str] = set()

    for category in unique_categories:
        weight = CATEGORY_WEIGHTS.get(category, DEFAULT_CATEGORY_WEIGHT)
        reason_text = CATEGORY_REASONS.get(
            category, f"Prompt contains patterns associated with category '{category}'"
        )

        reasons.append({
            "category": category,
            "weight": weight,
            "reason": reason_text
        })
        base_score += weight

        # Track heuristics covered by this signature category to avoid double-counting
        if category in SIGNATURE_HEURISTIC_OVERLAPS:
            for h_name in SIGNATURE_HEURISTIC_OVERLAPS[category]:
                covered_heuristics.add(h_name)

    # 2. Process Heuristic Signals
    active_heuristics: List[Dict[str, Any]] = []
    independent_heuristic_count = 0

    for h in heuristics:
        if not isinstance(h, dict):
            continue
        h_name = h.get("name", "unknown_heuristic")
        h_weight = h.get("weight", 5)
        h_desc = h.get("description", f"Heuristic signal '{h_name}' triggered")

        active_heuristics.append(h)

        # Deduplication rule: If an overlapping signature category is already active,
        # do not double-count points for this heuristic.
        effective_weight = 0 if h_name in covered_heuristics else h_weight
        if effective_weight > 0:
            independent_heuristic_count += 1

        reasons.append({
            "category": h_name,
            "weight": effective_weight,
            "reason": h_desc
        })
        base_score += effective_weight

    # 3. Apply Multi-Signal Bonus
    # Bonus applies if attack combines >= 2 distinct risk signals (signatures + independent heuristics)
    total_distinct_signals = len(unique_categories) + independent_heuristic_count
    if total_distinct_signals >= 2:
        base_score += MULTI_CATEGORY_BONUS

    final_score = min(base_score, MAX_RISK_SCORE)

    return {
        "risk_score": final_score,
        "categories": unique_categories,
        "heuristics": active_heuristics,
        "reasons": reasons
    }
