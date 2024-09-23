from sqlalchemy import (
    String,
    JSON,
    INTEGER,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from db.postgres import Base
from models.template import Template


class Notification(Base):
    """Модель Уведомления."""

    name: Mapped[str] = mapped_column(
        String(255), nullable=False,
    )
    recepients: Mapped[list] = mapped_column(JSON)
    parameters: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(
        String(64), nullable=False, default="created",
    )
    delay_in_minutes: Mapped[int] = mapped_column(
        INTEGER,
    )
    type: Mapped[str] = mapped_column(String(64))
    schedule: Mapped[str] = mapped_column(String(64))
    template_id: Mapped[str] = mapped_column(
        ForeignKey(Template.id, ondelete="CASCADE")
    )
    template: Mapped[Template] = relationship()

    def __repr__(self):
        return f"<Notification {self.title}>"
