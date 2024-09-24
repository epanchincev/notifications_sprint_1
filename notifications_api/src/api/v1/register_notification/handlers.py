from fastapi import (
    APIRouter,
    Depends,
)

from src.api.v1.register_notification.schemas import (
    NotificationInSchema,
    NotificationOutSchema,
)
from src.api.v1.schemas import ApiResponse
from src.models.notification import NotificationModel
from src.models.notification_status import NotificationStatus
from src.services.producer import (
    get_queue_producer,
    IProducerService,
)


router = APIRouter(
    prefix="/register-notifications",
)


@router.post(
    '/',
    response_model=ApiResponse[NotificationOutSchema],
    description="Register a new notification in the queue",
)
async def register_notifications(
    data: NotificationInSchema,
    queue_service: IProducerService = Depends(get_queue_producer),
):
    notification = NotificationModel(**data.model_dump())
    await queue_service.produce(message=notification)
    return ApiResponse(
        data=NotificationOutSchema(
            notification_id=notification.notification_id,
            status=NotificationStatus.QUEUED,
        ),
    )
