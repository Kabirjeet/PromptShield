from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth.dependencies import get_current_user
from app.schemas.log_schema import AuditLogResponse
from app.services.log_service import get_recent_audit_events
from app.utils.logger import logger

router = APIRouter(prefix="/logs", tags=["Audit Logs"])


def get_user_id(current_user: dict) -> str:
    """Extract a stable identifier from the authenticated user."""
    user_id = (
        current_user.get("id")
        or current_user.get("_id")
        or current_user.get("sub")
    )

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Authenticated user identifier is missing",
        )

    return str(user_id)


@router.get("", response_model=list[AuditLogResponse])
async def list_audit_logs(
    limit: int = Query(default=50, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    """Return recent audit events belonging to the authenticated user."""
    user_id = get_user_id(current_user)

    try:
        return await get_recent_audit_events(user_id, limit)
    except Exception:
        logger.exception("Failed to retrieve audit logs")
        raise HTTPException(
            status_code=503,
            detail="Audit logs are temporarily unavailable",
        ) from None
