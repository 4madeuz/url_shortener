from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.models.url_models import URL as URLModel
from src.schemas.url_schemas import URL as URLSchema
from src.services.pydantic_base import BaseService
from src.services.postgres_service import PostgresService


class URLService(BaseService):
    """Сервис для управления URL"""


@lru_cache
def get_url_service(pg_session: AsyncSession = Depends(get_session)) -> URLService:
    return URLService(
        model_schema_class=URLSchema,
        postgres_service=PostgresService(session=pg_session, model_class=URLModel),
    )
