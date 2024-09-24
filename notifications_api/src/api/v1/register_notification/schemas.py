from uuid import UUID

from pydantic import BaseModel
from src.models.notification_status import NotificationStatus


class NotificationInSchema(BaseModel):
    recipients: list[UUID]
    template_id: UUID
    parameters: dict[str, str] = None
    channel: str


class NotificationOutSchema(BaseModel):
    notification_id: UUID
    status: NotificationStatus
