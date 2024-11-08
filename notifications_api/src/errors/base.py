from dataclasses import dataclass

from fastapi import status


@dataclass
class ServiceException(Exception):
    status_code: status = status.HTTP_500_INTERNAL_SERVER_ERROR

    @property
    def message(self) -> str:
        return "Internal Server Error"
