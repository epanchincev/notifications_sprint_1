from typing import List, Any

from config.logging import get_logger
from models.notification import Notification, ProcessedNotification
from services.auth_service import AuthService, AuthServiceField
from services.template_processor import TemplateProcessor

logger = get_logger(__name__)


class NotificationProcessor:
    def __init__(self, template_processor: TemplateProcessor, auth_service: AuthService):
        self.template_processor: TemplateProcessor = template_processor
        self.auth_service: AuthService = auth_service

    async def process_notification(self, notification: Notification) -> List[ProcessedNotification]:
        template = await self.template_processor.get_template(str(notification.template_id))
        processed_notifications: List[ProcessedNotification] = []

        for recipient in notification.recipients:
            recipient = str(recipient)
            user_data = await self.get_user_data(recipient, template.parameters)
            content = self.template_processor.render_template(template, {**user_data, **notification.parameters})

            processed_notification = ProcessedNotification(
                id=notification.id,
                type=notification.type,
                recipient=recipient,
                content=content,
                subject=template.subject,
            )
            processed_notifications.append(processed_notification)

        return processed_notifications

    async def get_user_data(self, user_id: str, required_fields: List[str]) -> dict[str, Any]:
        auth_fields = [
            getattr(AuthServiceField, field.upper())
            for field in required_fields if hasattr(AuthServiceField, field.upper())
        ]

        if not auth_fields:
            return {}

        user_data = await self.auth_service.get_user_data(user_id)

        return {
            auth_field.value: user_data.get(auth_field.value)
            for auth_field in auth_fields if auth_field.value in user_data
        }
