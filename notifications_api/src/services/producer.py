from abc import ABC, abstractmethod
from dataclasses import dataclass
import aio_pika
import logging

from src.queue.rabbit import get_rabbitmq

from fastapi import Depends

logger = logging.getLogger(__name__)


class IProducerService(ABC):
    @abstractmethod
    async def produce(self, message: str):
        """Consuming a message to queue."""


@dataclass
class RabbitMQProducerService(IProducerService):
    connection: aio_pika.Connection
    queue_name: str

    async def produce(self, message: str):
        async with self.connection.channel() as channel:
            queue = await channel.declare_queue(self.queue_name, durable=True)

            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()), routing_key=queue.name
            )

            logger.info(f"Produced message: {message}")


def get_queue_producer(
    connection: aio_pika.Connection = Depends(get_rabbitmq)
) -> IProducerService:
    return RabbitMQProducerService(connection, queue_name="notifications")
