from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    JSON,
    INTEGER,
    DateTime,
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

    title: Mapped[str] = mapped_column(
        String(255), nullable=False,
    )
    recepients: Mapped[list] = mapped_column(JSON)
    content: Mapped[str] = mapped_column(
        Text, nullable=False,
    )
    notification_type: Mapped[str] = mapped_column(
        String(64), nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(64), nullable=False, default="created",
    )
    delay_in_minutes: Mapped[int] = mapped_column(
        INTEGER,
    )
    start_period: Mapped[datetime] = mapped_column(
        DateTime,
    )
    period_in_days: Mapped[int] = mapped_column(
        INTEGER,
    )
    template_uuid: Mapped[str] = mapped_column(
        ForeignKey(Template.uuid, ondelete="CASCADE")
    )
    template: Mapped[Template] = relationship(
        back_populates="notifications",
    )

    def __repr__(self):
        return f"<Notification {self.title}>"
