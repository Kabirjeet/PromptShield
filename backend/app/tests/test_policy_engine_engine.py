
import pytest

from app.core.policy_engine import apply_policy, evaluate_policy


@pytest.mark.parametrize(
    ("severity", "expected_action"),
    [
        ("SAFE", "ALLOW"),
        ("LOW", "ALLOW"),
        ("MEDIUM", "FLAG"),
        ("HIGH", "BLOCK"),
        ("CRITICAL", "BLOCK"),
    ],
)
def test_severity_policy_mapping(severity, expected_action):
    result = evaluate_policy({"severity": severity})

    assert result["action"] == expected_action
    assert result["policy_reason"]


def test_unknown_severity_fails_closed():
    result = evaluate_policy({"severity": "UNKNOWN"})

    assert result["action"] == "BLOCK"


def test_missing_severity_fails_closed():
    result = evaluate_policy({})

    assert result["action"] == "BLOCK"


def test_policy_preserves_detection_result():
    analysis = {
        "detected": True,
        "risk_score": 60,
        "severity": "HIGH",
        "categories": ["jailbreak"],
        "matches": [],
        "heuristics": [],
        "reasons": [],
        "normalized_text": "example prompt",
    }

    result = apply_policy(analysis)

    assert result["action"] == "BLOCK"
    assert result["risk_score"] == 60
    assert result["severity"] == "HIGH"
    assert result["categories"] == ["jailbreak"]
    assert result["detected"] is True
