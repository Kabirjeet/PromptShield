from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class AuditLogResponse(BaseModel):
    id: str
    timestamp: datetime
    detected: bool
    risk_score: int
    severity: str
    categories: List[str] = Field(default_factory=list)
    action: str
    policy_reason: str
