from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Account:
    id: UUID
    name: str
    email: str
    is_active: bool
    is_staff: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
