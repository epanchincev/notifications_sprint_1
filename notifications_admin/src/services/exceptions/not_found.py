from http import HTTPStatus
from dataclasses import dataclass

from services.exceptions.base import BaseServiceException


@dataclass
class NotFoundException(BaseServiceException):
    instance_name: str = ''
    status_code: int = HTTPStatus.NOT_FOUND

    @property
    def message(self):
        return f"{self.instance_name} not found"
