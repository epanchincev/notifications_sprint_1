from jinja2 import Environment, BaseLoader
from models.template import Template
from typing import Dict, Any


class JinjaTemplate:
    def __init__(self, template: Template):
        self.template: Template = template
        self.env: Environment = Environment(loader=BaseLoader())
        self.jinja_template = self.env.from_string(template.content)

    def render(self, data: Dict[str, Any]) -> str:
        return self.jinja_template.render(data)
