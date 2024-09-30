from fastapi import (
    APIRouter,
    Depends,
)

from src.api.v1.default_notification.schemas import (
    NotificationInSchema,
    NotificationOutSchema,
)
from src.api.v1.schemas import ApiResponse
from src.usecases.notification import (
    DefaultNotificationSendUseCase,
    get_default_notification_send_use_case,
)


router = APIRouter()


@router.post(
    '/send-notification',
    response_model=ApiResponse[NotificationOutSchema],
    description="Register a new notification in the queue",
)
async def register_notifications(
    data: NotificationInSchema,
    use_case: DefaultNotificationSendUseCase = Depends(
        get_default_notification_send_use_case,
    ),
):
    notification_id, status = await use_case.execute(data=data)
    return ApiResponse(
        data=NotificationOutSchema(
            notification_id=notification_id,
            status=status.value,
        ),
    )
