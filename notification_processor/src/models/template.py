from pydantic import BaseModel, UUID4
from typing import List
from datetime import datetime


class Template(BaseModel):
    id: UUID4
    name: str
    subject: str
    content: str
    parameters: List[str]
    created_at: datetime
