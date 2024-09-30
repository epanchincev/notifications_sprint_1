from typing import Any
from http import HTTPStatus

from aiohttp import ClientSession
from asyncio import sleep

from core.config import settings
from core.logger import get_logger

session: ClientSession | None = None

logger = get_logger()


async def send_notification(
    body: dict[str, Any],
    delay_in_minutes: int | None = None,
) -> None:

    if delay_in_minutes:
        delay = delay_in_minutes * 60
        await sleep(delay)

    async with session.post(
        url=settings.notiification_service_url,
        json=body,
    ) as response:
        await response.json()

        if response.status != HTTPStatus.CREATED:
            logger.error(
              f"Failed to send notification. Status code: {response.status}"
            )
