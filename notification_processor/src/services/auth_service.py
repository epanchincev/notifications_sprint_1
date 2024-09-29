from typing import Dict, Any, List
import httpx
from config.settings import settings
from config.logging import get_logger
from pydantic import UUID4

logger = get_logger(__name__)


class AuthServiceField:
    USER_NAME = "user_name"
    EMAIL = "email"


class AuthService:
    def __init__(self, base_url: str):
        self.base_url: str = base_url

    async def get_user_data(self, user_id: UUID4) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/v1/user/{user_id}")
            response.raise_for_status()
            return response.json()
