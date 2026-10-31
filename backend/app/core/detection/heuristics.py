"""
Heuristic rules and configurations for PromptShield AI.

Defines deterministic heuristic signals, descriptions, weights, and regex/logic patterns.
"""

from typing import Dict, List

# Heuristic weights definition
HEURISTIC_WEIGHTS: Dict[str, int] = {
    "instruction_override_language": 10,
    "privileged_role_reference": 5,
    "prompt_extraction_language": 10,
    "roleplay_escalation": 10,
    "directive_density": 5,
    "obfuscation_signal": 10,
    "prompt_structure_anomaly": 5,
}

# Explainable descriptions for each heuristic signal
HEURISTIC_DESCRIPTIONS: Dict[str, str] = {
    "instruction_override_language": "Prompt contains language suggesting replacement or override of existing instructions.",
    "privileged_role_reference": "Prompt references system, developer, or internal instruction layers.",
    "prompt_extraction_language": "Prompt contains language attempting to retrieve or display internal instructions.",
    "roleplay_escalation": "Prompt attempts to use persona or role-play to remove safety restrictions.",
    "directive_density": "Prompt contains a high density of imperative directive phrases.",
    "obfuscation_signal": "Prompt contains unusual character sequences, excessive punctuation, or encoding anomalies.",
    "prompt_structure_anomaly": "Prompt exhibits structural anomalies such as combining instruction overrides with extraction or role-play requests.",
}

# Regex patterns for text-matching heuristics
HEURISTIC_PATTERNS: Dict[str, List[str]] = {
    "instruction_override_language": [
        r"\bfrom now on\b",
        r"\bfrom this point forward\b",
        r"\bnew instructions?\b",
        r"\bfollow (these|my|the following) instructions instead\b",
        r"\b(previous|prior) instructions are (no longer|not) valid\b",
        r"\breplace (your|the|all) instructions\b",
        r"\bignore everything (you were|told|previously)\b",
        r"\bdisregard everything (you were|told|previously)\b",
        r"\bsupersede (all|previous|prior) instructions\b",
    ],

    "privileged_role_reference": [
        r"\bsystem (message|instructions?|prompts?|rules?)\b",
        r"\bdeveloper (message|instructions?|prompts?|mode)\b",
        r"\bhidden (instructions?|prompts?|rules?)\b",
        r"\binternal (instructions?|prompts?|guidelines?)\b",
    ],

    "prompt_extraction_language": [
        r"\bshow (your )?((system|hidden|internal)\s+)*instructions?\b",
        r"\bprint (the|your)?\s*(((system|hidden|internal)\s+)*)instructions? you received\b",
        r"\bwhat (system )?instructions (were|was) given to you\b",
        r"\bwhat (were you|was) told before this (conversation|prompt)\b",
        r"\brepeat (your )?((system|hidden|internal)\s+)*instructions?\b",
        r"\bdisplay (your )?configuration\b",
        r"\breveal (your )?((system|hidden|initial)\s+)*(instructions?|prompts?)\b",
    ],

    "roleplay_escalation": [
        r"\bpretend (you are|to be) (an? )?unrestricted\b",
        r"\bact as (an? AI|a model) with no (rules|restrictions|limits|safety)\b",
        r"\bsimulate (an? )?unrestricted model\b",
        r"\byou are no longer bound by\b",
        r"\benter developer mode\b",
        r"\bwith no (safety )?rules\b",
        r"\bdo anything now\b",
    ],
}

# Directive words list for directive density calculation
DIRECTIVE_WORDS: List[str] = [
    "ignore", "follow", "do", "don't", "dont", "reveal", "output",
    "execute", "obey", "respond", "disregard", "override", "forget",
    "bypass", "display", "repeat", "print", "show"
]
