import hashlib
from datetime import datetime
from typing import Any, Sequence, TypeVar
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_session
from src.models.url_models import URL as URLModel
from src.schemas.url_schemas import URL as URLSchema
from src.schemas.url_schemas import URLCashTimestamp, URLCreateFull
from src.services.postgres_service import PostgresService
from src.services.redis_service import RedisCacheService, get_redis_service

M = TypeVar('M', bound=URLSchema)


class URLService():
    """Сервис для управления URL"""

    def __init__(
        self,
        model_schema_class: type[M],
        postgres_service: PostgresService,
        cache: RedisCacheService,
    ):
        self.model_schema_class = model_schema_class
        self.postgres_service = postgres_service
        self.cache = cache

    async def create_model(self, model_schema: M) -> M | None:

        short_url = self._shorten_url(model_schema.original_url)

        schema = URLCreateFull(
            original_url=model_schema.original_url, short_url=short_url,
        )
        db_model = await self.postgres_service.create(schema)  # type: ignore
        return db_model

    async def get_model_by_id(self, model_id: UUID) -> M | None:

        db_model = await self.postgres_service.get_by_id(model_id)  # type: ignore

        if not db_model:
            return None

        return db_model

    async def get_all_models(self) -> Sequence[Any]:

        db_models = await self.postgres_service.get_all()

        return db_models

    async def get_model_by_short_url(self, short_url: str) -> M | None:

        db_model = await self.cache.get_from_cache(short_url)

        if not db_model:
            db_model = await self.postgres_service.get_by_field(
                'short_url', short_url
            )
            if not db_model:
                return None
            schema = self.model_schema_class.model_validate(db_model)
            await self.cache.put_to_cache(
                db_model.short_url, schema.model_dump_json()
            )

        schema = self.model_schema_class.model_validate(db_model)
        await self._add_timestamp_to_queue(schema)
        return db_model

    def _shorten_url(self, original_url: str) -> str:
        hash_object = hashlib.sha256(original_url.encode())
        short_url = hash_object.hexdigest()[:8]
        return short_url

    async def _add_timestamp_to_queue(self, value: M):
        timestamp = URLCashTimestamp(
            id=value.id, timestamp=datetime.now(tz=None),
        )
        await self.cache.add_to_queue(
            queue_name='timestamps', data=timestamp.model_dump_json()
        )


def get_url_service(
    pg_session: AsyncSession = Depends(get_session),
    redis: RedisCacheService = Depends(get_redis_service),
) -> URLService:
    return URLService(
        model_schema_class=URLSchema,
        postgres_service=PostgresService(
            session=pg_session, model_class=URLModel
        ),
        cache=redis,
    )
