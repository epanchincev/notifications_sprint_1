from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NotificationTemplate(BaseModel):
    name: str
    type: str  # noqa
    subject: str
    content: str
    parameters: list[str]
    id: UUID  # noqa    
    created_at: datetime
