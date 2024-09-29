from pydantic import BaseModel, ConfigDict, Field
from enum import StrEnum


class NotificationType(StrEnum):
    email = "email"
    sms = "sms"
    push = "push"


class Notification(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, populate_by_name=True
    )

    notification_id: str = Field(max_length=256)
    recipient_id: str = Field(max_length=256)
    channel: NotificationType
    subject: str | None = Field(None, max_length=256)
    content: str
    metadata: dict
