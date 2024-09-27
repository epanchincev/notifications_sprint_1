from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastapi import Depends, BackgroundTasks

from models import Template, Notification
from services.exceptions.not_found import NotFoundException
from services.exceptions.template_not_exists import TemplateNotExistException
from services.exceptions.template_not_filled import TemplateNotFilledException
from repositories.template import ITemplateRepository, get_template_repository
from repositories.notification import (
    INotificationRepository,
    get_notification_repository,
)
from utils.send_notification import send_notification


class INotificationService(ABC):

    @abstractmethod
    async def get(self, id: str) -> Notification:
        """Get notification by id"""

    @abstractmethod
    async def get_multiple(
        self,
        status: str | None,
        type: str | None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Notification], int]:
        """Get Notifications, and total count"""

    @abstractmethod
    async def update_status(
        self,
        notification_id: str,
        new_status: str,
    ) -> Notification:
        """Update notification status"""

    @abstractmethod
    async def create(
        self,
        background_tasks: BackgroundTasks,
        template_id: str,
        recepients: list[str],
        parameters: dict[str, str],
        name: str,
        type: str,
        schedule: str | None = None,
        delay_in_minutes: int | None = None,
    ) -> Template:
        """Create a new template"""

    @abstractmethod
    async def delete(self, id: str) -> None:
        """Delete a template"""


@dataclass
class NotificationService(INotificationService):
    template_rep: ITemplateRepository
    notification_rep: INotificationRepository

    async def get(self, id: str) -> Notification:
        notification = await self.notification_rep.get(id)
        if not notification:
            raise NotFoundException(instance_name="Notification")

        return notification

    async def get_multiple(
        self,
        status: str | None,
        type: str | None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Notification], int]:
        count = await self.notification_rep.get_count(status, type)
        templates = await self.notification_rep.get_multiple(
            status, type, page, per_page,
        )

        return templates, count

    async def update_status(
        self,
        notification_id: str,
        new_status: str,
    ) -> Notification:
        notification = await self.get(notification_id)
        notification = await self.notification_rep.update_status(
            notification, new_status,
        )

        return notification

    async def create(
        self,
        background_tasks: BackgroundTasks,
        template_id: str,
        recepients: list[str],
        parameters: dict[str, str],
        name: str,
        type: str,
        schedule: str | None = None,
        delay_in_minutes: int | None = None,
    ) -> Notification:
        template = await self.template_rep.get(template_id)

        if not template:
            raise TemplateNotExistException(template_id=template_id)

        template_params = set(template.parameters)

        if len(template_params & set(parameters)) != len(template_params):
            raise TemplateNotFilledException()
        channel = template.type
        recepients = [str(r) for r in recepients]
        template_id = str(template_id)
        notification = await self.notification_rep.create(
            template_id, recepients, parameters, name,
            type, schedule, delay_in_minutes,
        )

        if notification.type != "scheduled":
            background_tasks.add_task(
                send_notification,
                body={
                    "recepients": recepients,
                    "template_id": template_id,
                    "parameters": parameters,
                    "channel": channel,
                },
                delay_in_minutes=delay_in_minutes,
            )

        return notification

    async def delete(self, id: str) -> None:
        notification = await self.get(id)
        await self.notification_rep.delete(notification)


def get_notification_service(
    template_rep: ITemplateRepository = Depends(get_template_repository),
    notification_rep: INotificationRepository = Depends(
        get_notification_repository,
    ),
) -> INotificationService:
    return NotificationService(
        template_rep=template_rep,
        notification_rep=notification_rep,
    )
