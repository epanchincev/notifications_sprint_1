from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

import httpx
from src.config.settings import settings
from src.models.template import NotificationTemplate
from src.services.errors import (
    BadResponseCodeTemplateService,
    TemplateServiceException,
)


class ITemplateService(ABC):

    @abstractmethod
    async def get_template(self, action: str) -> NotificationTemplate:
        """Returns the template for the given action."""


@dataclass
class TemplateService(ITemplateService):
    SERVICE_URL: str = settings.template_service_url

    async def get_template(self, action: str) -> NotificationTemplate:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.SERVICE_URL}/{action}")
                if not response.status_code == 200:
                    raise BadResponseCodeTemplateService(
                        status_code=response.status_code,
                    )

                # TODO: Определить схему для респонса
                return NotificationTemplate(**response.json())
        except BadResponseCodeTemplateService:
            raise
        except Exception as e:
            raise TemplateServiceException(
                main_error=e,
            ) from e


def get_template_service() -> ITemplateService:
    return TemplateService(
        SERVICE_URL=settings.template_service_url,
    )
