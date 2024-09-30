from http import HTTPStatus
from dataclasses import dataclass

from services.exceptions.base import BaseServiceException


@dataclass
class TemplateNotFilledException(BaseServiceException):
    status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY

    @property
    def message(self):
        return "All template parameters must be filled in."
