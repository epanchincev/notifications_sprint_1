from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends

from src.api.v1.default_notification.schemas import NotificationInSchema
from src.models.notification import NotificationModel
from src.models.notification_status import NotificationStatus
from src.services.producer import (
    get_queue_producer,
    IProducerService,
)


@dataclass
class DefaultNotificationSendUseCase:
    notification_producer: IProducerService

    async def execute(self, data: NotificationInSchema) -> tuple[UUID, NotificationStatus]:
        notification = NotificationModel(**data.model_dump())
        await self.notification_producer.produce(message=notification)
        return notification.notification_id, NotificationStatus.QUEUED,


def get_default_notification_send_use_case(
    notification_producer: IProducerService = Depends(get_queue_producer),
) -> DefaultNotificationSendUseCase:
    return DefaultNotificationSendUseCase(notification_producer=notification_producer)
