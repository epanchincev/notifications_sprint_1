from enum import StrEnum

from pydantic import BaseModel, ConfigDict, UUID4, model_validator, Field


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
    recepients: list[UUID4] = Field(min_length=1)
    schedule: str | None = None


class NotificationCreate(NotificationBase):

    parameters: dict[str, str]
    name: str | None = None
    type: NotificationType = NotificationType.insta
    delay_in_minutes: int | None = None

    @model_validator(mode="after")
    def check_delay(self):
        if (
            self.type == NotificationType.delayed
            and self.delay_in_minutes is None
        ):
            raise ValueError(
                "delay_in_minutes is required for delayed notifications",
            )

        return self

    @model_validator(mode="after")
    def check_schedule(self):
        if self.type == NotificationType.scheduled and self.schedule is None:
            raise ValueError(
                "schedule is required for scheduled notifications"
            )

        return self


class NotificationDB(NotificationBase):

    id: UUID4
    type: NotificationType
    status: str

    model_config = ConfigDict(from_attributes=True)
