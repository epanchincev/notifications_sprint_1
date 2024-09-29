import asyncio
from config.logging import setup_logging, get_logger
from config.settings import settings
from processors.notification_processor import NotificationProcessor
from services.auth_service import AuthService
from services.consumer import RabbitMQConsumer
from services.notification_service import NotificationService
from services.producer import RabbitMQProducer
from services.template_processor import TemplateProcessor

logger = get_logger(__name__)


async def main():
    setup_logging()
    consumer = RabbitMQConsumer(settings.rabbit_url, settings.rabbitmq_queue)
    producer = RabbitMQProducer(settings.rabbit_url, settings.rabbitmq_queue)
    template_processor = TemplateProcessor(settings.template_service_url)
    auth_service = AuthService(settings.auth_service_url)

    processor = NotificationProcessor(template_processor, auth_service)
    notification_service = NotificationService(processor, producer)

    logger.info("Application startup complete")

    try:
        await consumer.start_consuming(notification_service.process_and_send)
    except asyncio.CancelledError:
        logger.info("Received cancellation signal, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        await consumer.cleanup()
        logger.info("Application shutdown complete")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main_task = loop.create_task(main())

    try:
        loop.run_until_complete(main_task)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, cancelling tasks...")
        main_task.cancel()
        loop.run_until_complete(main_task)
    finally:
        loop.close()
