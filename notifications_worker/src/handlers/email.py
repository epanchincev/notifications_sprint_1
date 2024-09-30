import logging
import aiohttp

from core.config import settings
from handlers.notice import INotice
from models.notification import Notification, NotificationType


logger = logging.getLogger().getChild("email-handler")


class EmailNotice(INotice):
    type = NotificationType.email

    def verified(self, msg: Notification) -> bool:
        return True

    async def processing(self, msg: Notification):
        logger.info(f"Processing message {msg}")

        payload = {
            "action": "issue.send",
            "letter": {
                "message": {"html": msg.content},
                "subject": msg.subject,
                "from.email": "hamidabu47@yahoo.com",
            },
            "group": "personal",
            "email": msg.recipient_id,
            "sendwhen": "now",
            "apikey": settings.sendsay_apikey,
        }

        logger.info(payload)

        async with aiohttp.ClientSession() as session:
            url = (
                "https://api.sendsay.ru/general/api/v100/json/" + settings.sendsay_login
            )
            async with session.post(
                url=url,
                json=payload,
            ) as response:
                logger.info(f"Mail service response {response}")
                if response.status == 200:
                    res = await response.json()
                    logger.info(f"Mail service json {res}")
                    errors = res.get("error", None)
                    warnings = res.get("warnings", None)
                    if not errors and not warnings:
                        return
                raise Exception("Sending error")
