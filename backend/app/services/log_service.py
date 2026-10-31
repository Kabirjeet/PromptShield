from typing import Any

from app.database.mongodb import get_database
from app.models.log import build_audit_event
from app.utils.logger import logger


async def record_audit_event(
    analysis: dict[str, Any],
    user_id: str,
) -> bool:
    """
    Save an audit event to MongoDB.

    Returns False and logs an error if persistence fails.
    Raw prompts and normalized text are never stored.
    """
    try:
        event = build_audit_event(analysis, user_id)
        db = get_database()
        await db["audit_logs"].insert_one(event)
        return True
    except Exception:
        logger.exception("Failed to persist PromptShield audit event")
        return False


async def get_recent_audit_events(
    user_id: str,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Retrieve the authenticated user's most recent audit events."""
    db = get_database()

    cursor = (
        db["audit_logs"]
        .find({"user_id": user_id}, {"user_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )

    events = await cursor.to_list(length=limit)

    for event in events:
        event["id"] = str(event.pop("_id"))

    return events
