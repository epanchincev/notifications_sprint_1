from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_async_session
from models import Template


class ITemplateRepository(ABC):

    @abstractmethod
    async def get_count(self, type: str) -> int:
        """Get template count"""

    @abstractmethod
    async def get(self, id: str) -> Template:
        """Get template by id"""

    @abstractmethod
    async def get_by_name(self, name: str) -> Template:
        """Get template by name"""

    @abstractmethod
    async def get_multiple(
        self,
        type: str | None,
        page: int | None = 1,
        per_page: int | None = 20,
    ) -> list[Template]:
        """Get all templates"""

    @abstractmethod
    async def create(
        self,
        name: str,
        type: str,
        subject: str,
        content: str,
        parameters: list[str],
    ) -> Template:
        """Create a new template"""

    @abstractmethod
    async def update(
        self,
        template: Template,
        name: str,
        type: str,
        subject: str,
        content: str,
        parameters: list[str],
    ) -> Template:
        """Update a template"""

    @abstractmethod
    async def delete(self, template: Template) -> None:
        """Delete a template"""


@dataclass
class SATemplateRepository(ITemplateRepository):
    session: AsyncSession

    async def get(self, id: str) -> Template:
        template = await self.session.execute(
            select(Template).where(Template.id == id)
        )
        return template.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Template:
        template = await self.session.execute(
            select(Template).where(Template.name == name)
        )

        return template.scalar_one_or_none()

    async def get_count(self, type: str | None) -> int:
        query = select(func.count(Template.id))
        if type:
            query = query.where(Template.type == type)

        count = await self.session.execute(query)

        return count.scalar_one()

    async def get_multiple(
        self,
        type: str | None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[Template]:
        query = select(Template).limit(page_size).offset(
            (page - 1) * page_size)
        if type:
            query = query.where(Template.type == type)

        templates = await self.session.execute(query)

        return templates.scalars().all()

    async def create(
        self,
        name: str,
        type: str,
        subject: str,
        content: str,
        parameters: list[str],
    ) -> Template:
        template = Template(
            name=name,
            type=type,
            subject=subject,
            content=content,
            parameters=parameters,
        )
        self.session.add(template)
        await self.session.commit()
        await self.session.refresh(template)

        return template

    async def update(
        self,
        template: Template,
        name: str,
        type: str,
        subject: str,
        content: str,
        parameters: list[str],
    ) -> Template:
        """Update a template"""
        template.name = name
        template.type = type
        template.subject = subject
        template.content = content
        template.parameters = parameters

        self.session.add(template)
        await self.session.commit()
        await self.session.refresh(template)

        return template

    async def delete(self, template: Template) -> None:
        await self.session.delete(template)
        await self.session.commit()


def get_template_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ITemplateRepository:
    return SATemplateRepository(session)
