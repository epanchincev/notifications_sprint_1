from abc import ABC
from enum import StrEnum


class NotificationType(StrEnum):
    email = "email"
    sms = "sms"
    push = "push"


class INotice(ABC):
    type: NotificationType
    pass
