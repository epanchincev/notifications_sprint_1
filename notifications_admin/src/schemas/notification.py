from enum import StrEnum

from pydantic import BaseModel, ConfigDict, UUID4


class NotificationType(StrEnum):
    insta = "insta"
    delayed = "delayed"
    scheduled = "scheduled"


class NotificationStatus(StrEnum):
    in_progress = "in_progress"
    sent = "sent"
    scheduled = "scheduled"


class NotificationBase(BaseModel):

    template_id: UUID4
    recepients: list[UUID4]
    schedule: str | None = None


class NotificationCreate(NotificationBase):

    parameters: dict[str, str]
    name: str | None = None
    type: NotificationType = NotificationType.insta
    delay_in_minutes: int | None = None


class NotificationDB(NotificationBase):

    id: UUID4
    type: NotificationType
    status: str

    model_config = ConfigDict(from_attributes=True)
