from fastapi import APIRouter, Depends

from src.services.consumer import IProducerService, get_queue_producer

router = APIRouter(
    prefix="/register-notifications",
)


@router.get('/')
async def register_notifications(
    queue_service: IProducerService = Depends(get_queue_producer)
):
    await queue_service.produce(message="Hello, World!")
