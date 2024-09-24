from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, BackgroundTasks
from pydantic import UUID4

from services.notification import (
    INotificationService,
    get_notification_service,
)
from schemas.notification import (
    NotificationCreate,
    NotificationFilters,
    NotificationDB,
    NotificationMulti,
)


router = APIRouter(prefix="/admin/notifications", tags=["notification"])


@router.get(
    "/",
    summary="Возвращает список уведомлений",
    response_model=NotificationMulti,
)
async def get_notifications(
    request: Request,
    filters: NotificationFilters = Depends(),
    service: INotificationService = Depends(get_notification_service),
):
    notifications, total = await service.get_multiple(
        **filters.model_dump()
    )

    return NotificationMulti(
        notifications=notifications,
        total=total,
        page=filters.page,
        per_page=len(notifications),
    )


@router.get(
    "/{notification_id}",
    summary="Возвращает уведомление по id",
    response_model=NotificationDB,

)
async def get_notification(
    request: Request,
    notification_id: UUID4,
    service: INotificationService = Depends(get_notification_service),
):
    notification = await service.get(notification_id)

    return notification


@router.post(
    "/",
    summary="Создает Уведомление",
    response_model=NotificationDB,
)
async def create_notification(
    request: Request,
    background_tasks: BackgroundTasks,
    template_in: NotificationCreate,
    service: INotificationService = Depends(get_notification_service),
):
    notification = await service.create(
        background_tasks,
        **template_in.model_dump(),
    )

    return notification


@router.delete(
    "/{template_id}",
    summary="Удаляет уведомление по id",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_template(
    request: Request,
    template_id: UUID4,
    service: INotificationService = Depends(get_notification_service),
):
    await service.delete(template_id)

    return
