import logging
from abc import ABC, abstractmethod

import aio_pika

logger = logging.getLogger().getChild("rabbit-consumer")


class IQueueConsumer(ABC):
    @abstractmethod
    def consume(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class RabbitMQConsumer(IQueueConsumer):
    def __init__(
        self,
        url: str,
        queue_name: str,
        exchange_name: str,
        consumer_tag=None,
        prefetch_count: int = 1,
    ):
        self._queue_name = queue_name
        self._queue = None
        self._exchange_name = exchange_name
        self._connection = None
        self._channel = None
        self._consumer_tag = consumer_tag
        self._url = url
        self._prefetch_count = prefetch_count
        self.on_message = None

    async def _connect(self):
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=self._prefetch_count)

        args = {
            "x-dead-letter-exchange": self._exchange_name,
        }
        self._queue = await self._channel.declare_queue(
            self._queue_name, durable=True, arguments=args
        )

    async def consume(self):
        await self._connect()
        await self._queue.consume(
            self.on_message, no_ack=False, consumer_tag=self._consumer_tag
        )

    async def stop(self):
        await self._connection.close()
