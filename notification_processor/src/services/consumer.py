import aio_pika
import json
from aio_pika import IncomingMessage
from config.logging import get_logger
from models.notification import Notification

logger = get_logger(__name__)


class RabbitMQConsumer:
    def __init__(self, url: str, queue_name: str):
        self.url = url
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    async def start_consuming(self, callback):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()
        queue = await self.channel.declare_queue(self.queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await self.process_message(message, callback)

    async def process_message(self, message: IncomingMessage, callback):
        async with message.process():
            try:
                notification_data = json.loads(message.body.decode())
                notification = Notification(**notification_data)
                await callback(notification)
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    async def cleanup(self):
        logger.info("Cleaning up RabbitMQ connections...")
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
        logger.info("RabbitMQ connections closed")
