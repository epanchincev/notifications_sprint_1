from abc import ABC, abstractmethod
from typing import Any

from models.notification import Notification


class INotice(ABC):
    type: str

    @abstractmethod
    def verified(self, msg: Notification) -> bool:
        pass

    @abstractmethod
    def processing(self, msg: Notification) -> Any:
        pass
