from enum import Enum
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class Notification(BaseModel):
    id: UUID
    type: NotificationType
    template_id: UUID
    recipients: list[UUID]
    parameters: Dict[str, str] | None = {}


class ProcessedNotification(BaseModel):
    id: UUID
    type: NotificationType
    recipient: UUID
    content: str
    subject: Optional[str] = None
