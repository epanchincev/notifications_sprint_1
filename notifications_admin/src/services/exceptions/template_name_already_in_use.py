from http import HTTPStatus
from dataclasses import dataclass

from services.exceptions.base import BaseServiceException


@dataclass
class TemplateNameAlreadyInUseException(BaseServiceException):
    status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY

    @property
    def message(self):
        return "Template name already in use"
