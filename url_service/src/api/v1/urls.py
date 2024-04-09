from typing import Sequence
from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from src.schemas.url_schemas import URL as URLSchema
from src.schemas.url_schemas import URLCreate
from src.core.exeptions import ModelNotFoundException
from src.services.url_service import URLService, get_url_service

router = APIRouter()


@router.get("", response_model=list[URLSchema], status_code=status.HTTP_200_OK)
async def get_urls(
    url_service: URLService = Depends(get_url_service),
) -> Sequence[URLSchema]:
    url = await url_service.get_all_models()
    if not url:
        raise ModelNotFoundException
    return url


@router.post("", response_model=URLSchema, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    url_data: URLCreate, url_service: URLService = Depends(get_url_service),
) -> URLSchema:
    url = await url_service.create_model(url_data)
    return url


@router.get(
    '/{short_url}', response_class=RedirectResponse
)
async def get_short_url(
    short_url: str, url_service: URLService = Depends(get_url_service),
):
    url = await url_service.get_model_by_short_url(short_url)
    if not url:
        raise ModelNotFoundException
    return url


@router.get(
    '/info/{id}', response_model=URLSchema, status_code=status.HTTP_200_OK
)
async def get_url_info(
    id: UUID, url_service: URLService = Depends(get_url_service),
) -> URLSchema:
    url = await url_service.get_model_by_id(id)
    if not url:
        raise ModelNotFoundException
    return url
