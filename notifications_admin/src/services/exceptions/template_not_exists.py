from http import HTTPStatus
from dataclasses import dataclass, field

from services.exceptions.base import BaseServiceException


@dataclass
class TemplateNotExistException(BaseServiceException):
    template_id: str = field()
    status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY

    @property
    def message(self):
        return f"Template with id {self.template_id} not exists"
