from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends

from src.api.v1.static_notification.schemas import RegisterNotificationInSchema
from src.models.notification import NotificationModel
from src.models.notification_status import NotificationStatus
from src.services.producer import (
    get_queue_producer,
    IProducerService,
)
from src.services.template import (
    get_template_service,
    ITemplateService,
)


@dataclass
class SendRegisterNotificationUseCase:
    template_service: ITemplateService
    producer_service: IProducerService

    async def execute(self, data: RegisterNotificationInSchema) -> tuple[UUID, NotificationStatus]:
        template = await self.template_service.get_template(action="register")
        notification = NotificationModel(
            recipients=[data.user_id],
            template_id=template.id,
            channel=data.channel,

        )
        await self.producer_service.produce(message=notification)
        return notification.notification_id, NotificationStatus.QUEUED,


def get_send_register_notification_use_case(
    template_service: ITemplateService = Depends(get_template_service),
    producer_service: IProducerService = Depends(get_queue_producer),
) -> SendRegisterNotificationUseCase:
    return SendRegisterNotificationUseCase(
        template_service=template_service,
        producer_service=producer_service,
    )
