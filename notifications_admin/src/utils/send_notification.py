from logging import getLogger
from typing import Any

from aiohttp import ClientSession
from asyncio import sleep

# from core.config import settings

session: ClientSession | None = None

logger = getLogger(__name__)


async def send_notification(
    body: dict[str, Any],
    delay_in_minutes: int | None = None,
) -> None:

    if delay_in_minutes:
        delay = delay_in_minutes * 60
        await sleep(delay)

    async with session.get("http://localhost:8000/ping") as response:
        await response.json()

        if response.status != 200:
            logger.error(
                f"Failed to send notification. Status code: {response.status}"
            )

        logger.info("Notification sent")

    # async with session.post(
    #     url=settings.notiification_service_url,
    #     json=body,
    # ) as response:
    #     await response.json()

    #     if response.status != 200:
    #         logger.error(
    #           f"Failed to send notification. Status code: {response.status}"
    #         )
