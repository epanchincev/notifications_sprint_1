from typing import List, Any

from config.logging import get_logger
from models.notification import Notification, ProcessedNotification
from processors.template_processor import TemplateProcessor
from services.auth_service import AuthService, AuthServiceField
from templates.jinja_template import JinjaTemplate

logger = get_logger(__name__)


class NotificationProcessor:
    def __init__(
        self, template_processor: TemplateProcessor, auth_service: AuthService
    ):
        self.template_processor: TemplateProcessor = template_processor
        self.auth_service: AuthService = auth_service

    async def process_notification(
        self, notification: Notification
    ) -> List[ProcessedNotification]:
        template = await self.template_processor.get_template(
            str(notification.template_id)
        )
        renderer_content = JinjaTemplate(template.content)
        renderer_subject = JinjaTemplate(template.subject)

        processed_notifications: List[ProcessedNotification] = []

        for recipient in notification.recipients:
            recipient = str(recipient)
            user_data = await self.get_user_data(recipient, template.parameters)
            logger.info(f"retrived user_data: {user_data}")
            subject = self.template_processor.render_template(
                renderer_content, {**user_data, **notification.parameters}
            )
            content = self.template_processor.render_template(
                renderer_subject, {**user_data, **notification.parameters}
            )

            processed_notifications.append(
                ProcessedNotification(
                    id=notification.id,
                    type=notification.type,
                    recipient=recipient,
                    content=content,
                    subject=subject,
                )
            )

        return processed_notifications

    async def get_user_data(
        self, user_id: str, required_fields: List[str]
    ) -> dict[str, Any]:
        auth_fields = [
            getattr(AuthServiceField, field.upper())
            for field in required_fields
            if hasattr(AuthServiceField, field.upper())
        ]

        logger.info(
            f"Processing user data for user ID: {user_id} and auth_fields: {auth_fields}"
            + f"and required fields: {required_fields}"
        )
        if not auth_fields:
            return {}

        user_data = await self.auth_service.get_user_data(user_id)
        logger.info(f"Processed user data {user_data}")

        return {
            auth_field: user_data.get(auth_field)
            for auth_field in auth_fields
            if auth_field in user_data
        }
