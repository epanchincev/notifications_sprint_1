from pydantic import BaseModel, ConfigDict, Field, EmailStr
from handlers.notice import NotificationType


class Notification(BaseModel):
    """Модель сообщения"""
    notification_id: str = Field(max_length=256)
    recipient_id: str = Field(max_length=256)
    channel: NotificationType
    subject: str | None = Field(None, max_length=256)
    content: str
    metadata: dict
