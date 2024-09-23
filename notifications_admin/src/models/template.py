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


class Template(Base):
    """Модель Шаблона."""

    name: Mapped[str] = mapped_column(
        String(255), nullable=False,
    )
    subject: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(
        Text, nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String(64), nullable=False,
    )
    parameters: Mapped[list] = mapped_column(JSON)

    def __repr__(self):
        return f"<Template {self.title}>"
