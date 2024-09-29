import asyncio

from core.config import settings
from core.logger import logger
from handlers.email import EmailNotice
from services.notifier import Notifier
from services.queue_consumer import RabbitMQConsumer

queue_parameters = {
    "url": settings.queue.get_url(),
    "queue_name": settings.queue_name,
    "exchange_name": settings.queue_exchange_name,
    "consumer_tag": settings.queue_consumer_tag,
}


async def main() -> None:
    logger.info(f"Start {settings.project_name}")
    queue = RabbitMQConsumer(**queue_parameters)
    email_handler = EmailNotice()
    notifier = Notifier(queue=queue, handlers=[email_handler])

    await notifier.start()

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await notifier.stop()


if __name__ == "__main__":
    asyncio.run(main())
