from typing import TypeVar

from sqlalchemy import (
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from db.postgres import Base


Notification = TypeVar("Notification")


class Template(Base):
    """Модель Шаблона."""

    name: Mapped[str] = mapped_column(
        String(256), nullable=False, unique=True,
    )
    subject: Mapped[str] = mapped_column(String(256), nullable=True)
    content: Mapped[str] = mapped_column(
        Text, nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String(64), nullable=False,
    )
    parameters: Mapped[list] = mapped_column(JSON)

    def __repr__(self):
        return f"<Template {self.title}>"
