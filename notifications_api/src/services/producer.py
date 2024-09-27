from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from fastapi import Depends

import aio_pika
from src.config.loging import get_logger
from src.models.notification import NotificationModel
from src.queue.rabbit import get_rabbitmq
from src.services.errors import UnexpectedProducerError


logger = get_logger()


class IProducerService(ABC):
    @abstractmethod
    async def produce(self, message: NotificationModel):
        """Consuming a message to queue."""


@dataclass
class RabbitMQProducerService(IProducerService):
    connection: aio_pika.Connection
    queue_name: str

    async def produce(self, message: NotificationModel):
        try:
            message_id = message.notification_id
            message = message.model_dump_json()

            async with self.connection.channel() as channel:
                queue = await channel.declare_queue(self.queue_name, durable=True)

                await channel.default_exchange.publish(
                    aio_pika.Message(body=message.encode()), routing_key=queue.name,
                )

                logger.info(
                    "Produced message: %s to queue: %s",
                    message_id,
                    queue.name,
                )
        except Exception as e:
            raise UnexpectedProducerError(
                main_error=e,
            ) from e


def get_queue_producer(
    connection: aio_pika.Connection = Depends(get_rabbitmq),
) -> IProducerService:
    return RabbitMQProducerService(connection, queue_name="notifications")
