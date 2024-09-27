from typing import Optional
import aio_pika


rabbitmq: Optional[aio_pika.Connection] = None


def get_rabbitmq() -> aio_pika.Connection:
    return rabbitmq
