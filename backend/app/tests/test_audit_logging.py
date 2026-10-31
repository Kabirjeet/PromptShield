from datetime import datetime, timezone

import pytest

from app.models.log import build_audit_event
from app.services import log_service


def test_audit_event_excludes_prompt_text():
    analysis = {
        "detected": True,
        "risk_score": 85,
        "severity": "HIGH",
        "categories": ["prompt_injection"],
        "action": "BLOCK",
        "policy_reason": "High severity",
        "normalized_text": "sensitive prompt content",
    }

    event = build_audit_event(analysis, "user_123")

    assert event["user_id"] == "user_123"
    assert event["action"] == "BLOCK"
    assert event["risk_score"] == 85
    assert event["categories"] == ["prompt_injection"]
    assert isinstance(event["timestamp"], datetime)
    assert event["timestamp"].tzinfo == timezone.utc
    assert "normalized_text" not in event
    assert "prompt" not in event


@pytest.mark.asyncio
async def test_record_audit_event_success(monkeypatch):
    class FakeCollection:
        async def insert_one(self, event):
            self.event = event
            return object()

    class FakeDatabase:
        def __init__(self):
            self.collection = FakeCollection()

        def __getitem__(self, name):
            assert name == "audit_logs"
            return self.collection

    fake_db = FakeDatabase()
    monkeypatch.setattr(
        log_service,
        "get_database",
        lambda: fake_db,
    )

    result = await log_service.record_audit_event(
        {
            "detected": False,
            "risk_score": 0,
            "severity": "SAFE",
            "categories": [],
            "action": "ALLOW",
            "policy_reason": "Safe request",
        },
        "user_123",
    )

    assert result is True
    assert fake_db.collection.event["action"] == "ALLOW"


@pytest.mark.asyncio
async def test_record_audit_event_failure(monkeypatch):
    class FakeCollection:
        async def insert_one(self, event):
            raise RuntimeError("Database unavailable")

    class FakeDatabase:
        def __getitem__(self, name):
            return FakeCollection()

    monkeypatch.setattr(
        log_service,
        "get_database",
        lambda: FakeDatabase(),
    )

    result = await log_service.record_audit_event(
        {
            "detected": True,
            "risk_score": 90,
            "severity": "CRITICAL",
            "categories": ["prompt_injection"],
            "action": "BLOCK",
            "policy_reason": "Critical severity",
        },
        "user_123",
    )

    assert result is False