from sqlalchemy import (
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from db.postgres import Base


class Template(Base):
    """Модель Шаблона."""

    title: Mapped[str] = mapped_column(
        String(255), nullable=False,
    )
    subject: Mapped[str] = mapped_column(
        String(255), nullable=False,
    )
    body: Mapped[str] = mapped_column(
        Text, nullable=False,
    )
    template_type: Mapped[str] = mapped_column(
        String(64), nullable=False,
    )

    def __repr__(self):
        return f"<Template {self.title}>"
