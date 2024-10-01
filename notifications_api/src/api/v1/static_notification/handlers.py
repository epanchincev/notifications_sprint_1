from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from src.api.v1.schemas import ApiResponse
from src.api.v1.static_notification.schemas import (
    NotificationOutSchema,
    RegisterNotificationInSchema,
)
from src.services.auth import jwt_auth_bearer
from src.usecases.register_notification import (
    get_send_register_notification_use_case,
    SendRegisterNotificationUseCase,
)


router = APIRouter()


@router.post(
    '/user-registration',
    response_model=ApiResponse[NotificationOutSchema],
    description="Send a notification when user registration",
)
async def register_notifications(
    data: RegisterNotificationInSchema,
    token: Annotated[str, Depends(jwt_auth_bearer)],
    use_case: SendRegisterNotificationUseCase = Depends(
        get_send_register_notification_use_case,
    ),
):
    notification_id, status = await use_case.execute(data=data)
    return ApiResponse(
        data=NotificationOutSchema(
            notification_id=notification_id,
            status=status.value,
        ),
    )
