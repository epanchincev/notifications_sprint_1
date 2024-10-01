import http

from fastapi import (
    HTTPException,
    Request,
)
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from src.config.settings import settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        return await self._bearer_auth(request)

    async def _bearer_auth(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail='Invalid authorization code.',
            )
        if not credentials.scheme == 'Bearer':
            raise HTTPException(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                detail='Only Bearer token might be accepted',
            )
        if not credentials.credentials == settings.APP_AUTH_TOKEN:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail='Invalid authorization token.',
            )
        return credentials.credentials


jwt_auth_bearer = JWTBearer()
