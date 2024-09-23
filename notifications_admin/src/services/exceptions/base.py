from dataclasses import dataclass
from http import HTTPStatus


@dataclass
class BaseServiceException(Exception):
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR

    @property
    def message(self) -> str:
        return "Internal server error"
