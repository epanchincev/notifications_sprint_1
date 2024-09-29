from typing import Dict, Any

import httpx

from config.logging import get_logger
from models.template import Template

logger = get_logger(__name__)


class TemplateProcessor:
    def __init__(self, base_url: str):
        self.base_url: str = base_url
        self.path = f"{base_url}/api/v1/admin/templates"

    async def get_template(self, template_id: str) -> Template:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.path}/{template_id}")
            response.raise_for_status()
            return Template(**response.json())

    def render_template(self, template: Template, parameters: Dict[str, Any]) -> str:
        content = template.content
        for key, value in parameters.items():
            content = content.replace(f"{{{{ {key} }}}}", str(value))
        return content
