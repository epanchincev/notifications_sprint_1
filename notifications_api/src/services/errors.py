from dataclasses import dataclass

from src.errors.base import ServiceException


@dataclass
class UnexpectedProducerError(ServiceException):
    main_error: Exception = None

    @property
    def message(self) -> str:
        return "An unexpected error occurred while producing the message"


@dataclass
class TemplateServiceException(UnexpectedProducerError):

    @property
    def message(self) -> str:
        return "An error occurred while retrieving the template"


@dataclass
class BadResponseCodeTemplateService(ServiceException):

    @property
    def message(self) -> str:
        return f"The response code from the template service is {self.status_code}."
