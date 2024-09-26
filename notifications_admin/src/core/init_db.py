from contextlib import asynccontextmanager

from db.postgres import get_async_session
from repositories.template import ITemplateRepository, get_template_repository


get_async_session_context = asynccontextmanager(get_async_session)


async def create_basic_templates(templates_rep: ITemplateRepository) -> None:
    template = await templates_rep.get_by_name('register')
    if not template:
        await templates_rep.create(
            'register',
            'email',
            'Регистрация в сервисе',
            'Поздравляем %username%, Вы успешно зарегистрировались в сервисе!',
            ['username'],
        )


async def init_db():
    async with get_async_session_context() as session:
        template_rep: ITemplateRepository = get_template_repository(session)
        await create_basic_templates(template_rep)
