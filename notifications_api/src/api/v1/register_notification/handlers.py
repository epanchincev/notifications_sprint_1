from fastapi import APIRouter, Depends

from notifications_api.src.services.producer import IProducerService, get_queue_producer

router = APIRouter(
    prefix="/register-notifications",
)


@router.get('/')
async def register_notifications(
    queue_service: IProducerService = Depends(get_queue_producer)
):
    await queue_service.produce(message="Hello, World!")
