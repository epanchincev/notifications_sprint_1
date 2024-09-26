from uuid import (
    UUID,
    uuid4,
)

from pydantic import (
    BaseModel,
    Field,
)


class NotificationModel(BaseModel):
    recipients: list[UUID]
    template_id: UUID | None
    parameters: dict[str, str] | None
    channel: str
    notification_id: UUID = Field(default_factory=uuid4)
