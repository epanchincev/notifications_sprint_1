from typing import List

from config.logging import get_logger
from config.settings import settings
from models.notification import Notification, ProcessedNotification
from processors.notification_processor import NotificationProcessor
from services.producer import RabbitMQProducer

logger = get_logger(__name__)


class NotificationService:
    def __init__(self, processor: NotificationProcessor, producer: RabbitMQProducer):
        self.processor: NotificationProcessor = processor
        self.producer: RabbitMQProducer = producer

    async def process_and_send(self, notification: Notification) -> List[ProcessedNotification]:
        processed_notifications: List[ProcessedNotification] = await self.processor.process_notification(notification)

        for processed_notification in processed_notifications:
            await self.producer.produce(processed_notification)
            logger.info(
                f"Sent processed notification: {processed_notification.id} to recipient: {processed_notification.recipient}")

        return processed_notifications
