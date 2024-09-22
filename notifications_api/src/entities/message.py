from dataclasses import dataclass
from uuid import UUID


@dataclass
class MessageEntityIn:
    message_id: UUID
    user_id: UUID
    template_id: UUID
    subject: str
    text: str
    notification_type: str
