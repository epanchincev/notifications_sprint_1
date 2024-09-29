import aio_pika
import json
from config.logging import get_logger
from models.notification import ProcessedNotification
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue

logger = get_logger(__name__)


class RabbitMQProducer:
    def __init__(self, url: str, queue: str):
        self.url: str = url
        self.queue: str = queue

    async def produce(self, notification: ProcessedNotification):
        connection: AbstractConnection = await aio_pika.connect_robust(self.url)
        channel: AbstractChannel = await connection.channel()

        message_body = json.dumps(notification.model_dump_json()).encode()
        message = aio_pika.Message(body=message_body)

        await channel.default_exchange.publish(message, routing_key=self.queue)
        logger.info(f"Sent processed notification: {notification.id} into {self.queue}. Message: {message.body}")
