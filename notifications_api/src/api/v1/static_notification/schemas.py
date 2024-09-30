from uuid import UUID

from pydantic import BaseModel
from src.models.notification_status import NotificationStatus


class RegisterNotificationInSchema(BaseModel):
    user_id: UUID
    channel: str


class NotificationOutSchema(BaseModel):
    notification_id: UUID
    status: NotificationStatus
