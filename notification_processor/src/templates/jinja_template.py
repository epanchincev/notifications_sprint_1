from jinja2 import Environment, BaseLoader
from models.template import Template
from typing import Dict, Any

from templates import TemplateRenderer


class JinjaTemplate(TemplateRenderer):
    def __init__(self, text: str):
        self.env: Environment = Environment(
            loader=BaseLoader(),
            variable_start_string="%",
            variable_end_string="%",
        )
        self.jinja_template = self.env.from_string(text)

    def render(self, data: Dict[str, Any]) -> str:
        return self.jinja_template.render(data)
