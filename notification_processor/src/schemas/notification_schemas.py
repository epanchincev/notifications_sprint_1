from pydantic import BaseModel, UUID4
from typing import List, Dict, Optional
from models.notification import NotificationType


class NotificationCreate(BaseModel):
    type: NotificationType
    template_id: UUID4
    recipients: List[UUID4]
    parameters: Optional[Dict[str, str]] = {}


class NotificationResponse(BaseModel):
    id: UUID4
    status: str


class NotificationStatus(BaseModel):
    id: UUID4
    status: str
    recipient: UUID4
    sent_at: Optional[str] = None
    error: Optional[str] = None
