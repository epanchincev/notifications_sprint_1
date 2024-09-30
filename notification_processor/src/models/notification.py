from enum import Enum
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class Notification(BaseModel):
    notification_id: UUID
    channel: NotificationType
    template_id: UUID
    recipients: list[UUID]
    parameters: Dict[str, str] | None = {}


class ProcessedNotification(BaseModel):
    notification_id: UUID
    channel: NotificationType
    recipient: UUID
    content: str
    subject: Optional[str] = None
