from abc import ABC, abstractmethod
from typing import Dict, Any


class TemplateRenderer(ABC):
    @abstractmethod
    def render(self, data: Dict[str, Any]) -> str:
        pass
