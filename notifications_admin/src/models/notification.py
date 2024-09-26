from sqlalchemy import (
    String,
    JSON,
    INTEGER,
    ForeignKey,
    ARRAY,
    UUID,
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
    recepients: Mapped[list] = mapped_column(ARRAY(UUID))
    parameters: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(
        String(64), nullable=False, default="in_progress",
    )
    delay_in_minutes: Mapped[int] = mapped_column(
        INTEGER,
    )
    type: Mapped[str] = mapped_column(String(64))
    schedule: Mapped[str] = mapped_column(String(64))
    template_id: Mapped[str] = mapped_column(
        ForeignKey(Template.id),
    )
    template: Mapped[Template] = relationship()

    def __repr__(self):
        return f"<Notification {self.title}>"
