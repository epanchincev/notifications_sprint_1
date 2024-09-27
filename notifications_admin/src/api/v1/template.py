from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from pydantic import UUID4

from services.template import ITemplateService, get_template_service
from schemas.template import (
    TemplateCreateOrUpdate,
    TemplateFilters,
    TemplateDB,
    TemplateMulti,
)


router = APIRouter(prefix="/admin/templates", tags=["template"])


@router.get(
    "/",
    summary="Возвращает список шаблонов",
    response_model=TemplateMulti,
)
async def get_templates(
    request: Request,
    filters: TemplateFilters = Depends(),
    service: ITemplateService = Depends(get_template_service),
):
    templates, total = await service.get_multiple(
        **filters.model_dump()
    )

    return TemplateMulti(
        templates=templates,
        total=total,
        page=filters.page,
        per_page=len(templates),
    )


@router.get(
    "/{template_id}",
    summary="Возвращает шаблон по id",
    response_model=TemplateDB,

)
async def get_template(
    request: Request,
    template_id: UUID4,
    service: ITemplateService = Depends(get_template_service),
):
    template = await service.get(template_id)

    return template


@router.post(
    "/",
    summary="Создает шаблон",
    response_model=TemplateDB,
)
async def create_template(
    request: Request,
    template_in: TemplateCreateOrUpdate,
    service: ITemplateService = Depends(get_template_service),
):
    template = await service.create(**template_in.model_dump())

    return template


@router.delete(
    "/{template_id}",
    summary="Удаляет шаблон по id",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_template(
    request: Request,
    template_id: UUID4,
    service: ITemplateService = Depends(get_template_service),
):
    await service.delete(template_id)

    return


@router.patch(
    "/{template_id}",
    summary="Обновляет шаблон по id",
    response_model=TemplateDB,
)
async def update_template(
    request: Request,
    template_id: UUID4,
    template_in: TemplateCreateOrUpdate,
    service: ITemplateService = Depends(get_template_service),
):
    template = await service.update(template_id, **template_in.model_dump())

    return template


@router.get(
    "/static/{name}",
    summary="Получить статический шаблон по имени",
    response_model=TemplateDB,
)
async def get_static_template(
    request: Request,
    name: str,
    service: ITemplateService = Depends(get_template_service),
):
    template = await service.get_by_name(name)

    return template
