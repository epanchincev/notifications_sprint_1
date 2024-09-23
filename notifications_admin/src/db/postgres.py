from datetime import datetime
from typing import AsyncGenerator
from uuid import uuid4


from sqlalchemy import (
    DateTime,
    UUID,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
    Mapped,
    mapped_column,
    sessionmaker,
)

from core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        """Именем таблицы будет название модели в нижнем регистре."""
        return cls.__name__.lower()

    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
    )

    __table_args__ = {'schema': settings.db_schema}


Base = declarative_base(cls=PreBase)

engine = create_async_engine(
    f"postgresql+asyncpg://{settings.db_user}"
    f":{settings.db_password}@{settings.db_host}:"
    f"{settings.db_port}/{settings.db_database}",
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session(
) -> AsyncGenerator[AsyncSession, AsyncSession]:
    """Корутина отдающая асинхронную сессию."""
    async with AsyncSessionLocal() as async_session:
        try:
            yield async_session
        except SQLAlchemyError:
            await async_session.rollback()
            raise
        finally:
            await async_session.close()
