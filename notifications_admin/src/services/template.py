from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastapi import Depends

from models import Template
from services.exceptions.not_found import NotFoundException
from repositories.template import ITemplateRepository, get_template_repository


class ITemplateService(ABC):

    @abstractmethod
    async def get(self, id: str) -> Template:
        """Get template by id"""

    @abstractmethod
    async def get_multiple(
        self,
        type: str | None,
        page: int | None = 1,
        per_page: int | None = 20,
    ) -> tuple[list[Template], int]:
        """Get all templates, and total count"""

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
        id: str,
        name: str,
        type: str,
        subject: str,
        content: str,
        parameters: list[str],
    ) -> Template:
        """Update a template"""

    @abstractmethod
    async def delete(self, id: str) -> None:
        """Delete a template"""


@dataclass
class TemplateSevice(ITemplateService):
    template_rep: ITemplateRepository

    async def get(self, id: str) -> Template:
        template = await self.template_rep.get(id)
        if not template:
            raise NotFoundException(instance_name="Template")

        return template

    async def get_multiple(
        self,
        type: str | None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Template], int]:
        count = await self.template_rep.get_count(type)
        templates = await self.template_rep.get_multiple(type, page, per_page)

        return templates, count

    async def create(
        self,
        name: str,
        type: str,
        subject: str,
        content: str,
        parameters: list[str],
    ) -> Template:
        return await self.template_rep.create(
            name, type, subject,
            content, parameters,
        )

    async def update(
        self,
        id: str,
        name: str,
        type: str,
        subject: str,
        content: str,
        parameters: list[str],
    ) -> Template:
        template = await self.get(id)
        template = await self.template_rep.update(
            template, name, str(type),
            subject, content, parameters
        )

        return template

    async def delete(self, id: str) -> None:
        template = await self.get(id)
        await self.template_rep.delete(template)


def get_template_service(
    template_rep: ITemplateRepository = Depends(get_template_repository),
) -> ITemplateService:
    return TemplateSevice(
        template_rep=template_rep,
    )
