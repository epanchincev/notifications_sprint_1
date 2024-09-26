from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_async_session
from models import Notification


class INotificationRepository(ABC):

    @abstractmethod
    async def get_count(
        self,
        status: str | None,
        type: str | None,
    ) -> int:
        """Get Notification count"""

    @abstractmethod
    async def get(self, id: str) -> Notification:
        """Get Notification by id"""

    @abstractmethod
    async def get_multiple(
        self,
        status: str | None,
        type: str | None,
        page: int | None = 1,
        per_page: int | None = 20,
    ) -> list[Notification]:
        """Get all Notifications"""

    @abstractmethod
    async def create(
        self,
        template_id: str,
        recepients: list[str],
        parameters: dict[str, str],
        name: str,
        type: str,
        schedule: str | None = None,
        delay_in_minutes: int | None = None,
    ) -> Notification:
        """Create a new Notification"""

    @abstractmethod
    async def update_status(
        self,
        notification: Notification,
        new_status: str,
    ) -> Notification:
        """Update Notification status"""

    @abstractmethod
    async def update(
        self,
        notification: Notification,
        template_id: str,
        recepients: list[str],
        parameters: dict[str, str],
        name: str,
        type: str,
        schedule: str | None = None,
        delay_in_minutes: int | None = None,
    ) -> Notification:
        """Update a Notification"""

    @abstractmethod
    async def delete(self, Notification: Notification) -> None:
        """Delete a Notification"""


@dataclass
class SANotificationRepository(INotificationRepository):
    session: AsyncSession

    async def get(self, id: str) -> Notification:
        notification = await self.session.execute(
            select(Notification).where(Notification.id == id)
        )
        return notification.scalar_one_or_none()

    async def get_count(self, status: str | None, type: str | None) -> int:
        query = select(func.count(Notification.id))
        if status:
            query = query.where(Notification.status == status)
        if type:
            query = query.where(Notification.type == type)

        count = await self.session.execute(query)

        return count.scalar_one()

    async def get_multiple(
        self,
        status: str | None,
        type: str | None,
        page: int | None = 1,
        per_page: int | None = 20,
    ) -> list[Notification]:
        query = select(Notification).limit(per_page).offset(
            (page - 1) * per_page)
        if type:
            query = query.where(Notification.type == type)
        if status:
            query = query.where(Notification.status == status)

        notifications = await self.session.execute(query)

        return notifications.scalars().all()

    async def create(
        self,
        template_id: str,
        recepients: list[str],
        parameters: dict[str, str],
        name: str,
        type: str,
        schedule: str | None = None,
        delay_in_minutes: int | None = None,
    ) -> Notification:
        notification = Notification(
            template_id=template_id,
            name=name,
            recepients=recepients,
            parameters=parameters,
            type=type,
            schedule=schedule,
            delay_in_minutes=delay_in_minutes,
        )
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)

        return notification

    async def update_status(
        self,
        notification: Notification,
        new_status: str,
    ) -> Notification:
        notification.status = new_status
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)

        return notification

    async def update(
        self,
        notification: Notification,
        template_id: str,
        recepients: list[str],
        parameters: dict[str, str],
        name: str,
        type: str,
        schedule: str | None = None,
        delay_in_minutes: int | None = None,
    ) -> Notification:
        """Update a Notification"""
        notification.template_id = template_id
        notification.recepients = recepients
        notification.parameters = parameters
        notification.name = name
        notification.type = type
        notification.schedule = schedule
        notification.delay_in_minutes = delay_in_minutes
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)

        return notification

    async def delete(self, notification: Notification) -> None:
        await self.session.delete(notification)
        await self.session.commit()


def get_notification_repository(
    session: AsyncSession = Depends(get_async_session),
) -> INotificationRepository:
    return SANotificationRepository(session)
