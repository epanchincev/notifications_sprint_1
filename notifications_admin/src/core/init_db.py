from contextlib import asynccontextmanager

from db.postgres import get_async_session


get_async_session_context = asynccontextmanager(get_async_session)


async def create_basic_templates(templates_rep) -> None:
    pass


async def init_db():
    """
    Корутина инициализирует базу данных.

    """
    pass
