from abc import (
    ABC,
    abstractmethod,
)


class ITemplateService(ABC):

    @abstractmethod
    async def get_template(self, action: str) -> str:
        """Returns the template for the given action."""


class TemplateService(ITemplateService):

    async def get_template(self, action: str) -> str:
        # Implementation here
        raise NotImplementedError


def get_template_service() -> ITemplateService:
    return TemplateService()
