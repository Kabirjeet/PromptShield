from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    password: str
    role: str = "guest"
    created_at: datetime = datetime.now(timezone.utc)