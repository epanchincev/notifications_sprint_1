import logging
import aio_pika

from handlers.notice import INotice
from models.notification import Notification
from services.queue_consumer import IQueueConsumer
from core.config import settings


logger = logging.getLogger(settings.logger_name)


class Notifier:
    _handlers: dict

    def __init__(self, queue: IQueueConsumer, handlers: list[INotice]):
        self._handlers = {}
        for handler in handlers:
            self._handlers[str(handler.type)] = handler
        self._queue = queue
        self._queue.on_message = self.on_message

    def add_handler(self, handler: INotice):
        self._handlers[handler.type] = handler

    async def on_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process(ignore_processed=True):
            try:
                notification = Notification.model_validate_json(message.body)
                handler = self._handlers.get(notification.channel)
                if handler:
                    await handler.processing(notification)
                    await message.ack()
                else:
                    raise ValueError("Unknown message type")
            except Exception as e:
                logger.error(f"Except {str(e)}")
                await message.reject(requeue=False)

    async def start(self):
        await self._queue.consume()

    async def stop(self):
        await self._queue.stop()
