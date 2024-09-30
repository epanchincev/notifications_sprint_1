import asyncio
import json

from aio_pika import DeliveryMode, ExchangeType, Message, connect

queue_name = "notification.sending"
routing_key = "notification.sending.v1.task"
exchange_name = "notifier"


async def main() -> None:
    connection = await connect(f"amqp://rabbit:rabbit@localhost:5672")

    async with connection:
        channel = await connection.channel()

        logs_exchange = await channel.declare_exchange(
            exchange_name,
            ExchangeType.DIRECT,
        )

        args = {"x-dead-letter-exchange": exchange_name}
        queue = await channel.declare_queue(
            name=queue_name, durable=True, arguments=args
        )

        await queue.bind(logs_exchange, routing_key=routing_key)

        for i in range(1):
            message_body = {
                "notification_id": str(i),
                "recipient_id": "admin@admins.com",
                "channel": "email",
                "content": "string",
                "metadata": {"campaign_id": str(i), "template_id": str(i)},
            }

            message = Message(
                json.dumps(message_body).encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
            )

            await logs_exchange.publish(message, routing_key=routing_key)

        print(f"Sent {message}")


if __name__ == "__main__":
    asyncio.run(main())
