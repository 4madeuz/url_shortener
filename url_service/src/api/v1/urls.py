from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.url_schemas import URL as URLSchema
from src.schemas.url_schemas import URLCreate, URLShort
from src.services.postgres_service import PostgresService
from src.services.pydantic_base import BaseService
from src.services.url_service import URLService, get_url_service

router = APIRouter()


@router.get("", response_model=list[URLSchema], status_code=status.HTTP_200_OK)
async def get_urls(
    url_service: URLService = Depends(get_url_service),
) -> list[URLSchema]:
    url = await url_service.get_all_models()
    return url


@router.post("", response_model=URLSchema, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    url_data: URLCreate,
    url_service: URLService = Depends(get_url_service),
) -> URLSchema:
    url = await url_service.create_model(url_data)
    return url


@router.get("/{short_url}", response_model=URLShort, status_code=status.HTTP_200_OK)
async def get_short_url(
    short_url: str,
    url_service: URLService = Depends(get_url_service),
) -> URLShort:
    url = await url_service.get_model_by_short_url(short_url)
    return url


@router.get("/info/{id}", response_model=URLSchema, status_code=status.HTTP_200_OK)
async def get_url_info(
    id: str,
    url_service: URLService = Depends(get_url_service),
) -> URLSchema:
    url = await url_service.get_model_by_id(id)
    return url
