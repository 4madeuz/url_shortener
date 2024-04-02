from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.url_schemas import URL as URLSchema, URLCreate
from src.services.pydantic_base import BaseService
from src.services.postgres_service import PostgresService
from src.services.url_service import URLService, get_url_service

router = APIRouter()


@router.get("", response_model=list[URLSchema], status_code=status.HTTP_200_OK)
async def get_urls(
    role_service: URLService = Depends(get_url_service),
) -> list[URLSchema]:
    roles = await role_service.get_all_models()
    return roles


@router.post("", response_model=URLSchema, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    role_data: URLCreate,
    role_service: URLService = Depends(get_url_service),
) -> URLSchema:
    role = await role_service.create_model(role_data)
    return role


@router.get("{short_url}", response_model=list[URLSchema], status_code=status.HTTP_200_OK)
async def get_short_url(
    role_service: URLService = Depends(get_url_service),
) -> list[URLSchema]:
    roles = await role_service.get_all_models()
    return roles
