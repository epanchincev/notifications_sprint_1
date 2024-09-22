from fastapi import APIRouter

from src.api.v1.ping.schemas import PingResponse
from src.api.v1.schemas import ApiResponse

router = APIRouter()


@router.get(
    "/ping",
    response_model=ApiResponse[PingResponse],
    description="Ping the server"
)
async def ping():
    response = PingResponse()
    return ApiResponse(data=response)
