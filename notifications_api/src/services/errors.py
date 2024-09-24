from dataclasses import dataclass

from src.errors.base import ServiceException


@dataclass
class UnexpectedProducerError(ServiceException):
    main_error: Exception = None

    @property
    def message(self) -> str:
        return "An unexpected error occurred while producing the message"
