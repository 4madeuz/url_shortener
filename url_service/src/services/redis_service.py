import json
from typing import Union

from fastapi import Depends
from redis.asyncio import Redis
from src.db.redis import get_redis
from src.services.abstract import AbstractCacheService


class RedisCacheService(AbstractCacheService):
    """A caching service implementation for working with Redis."""

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_from_cache(
        self, cache_key: str
    ) -> Union[str, list[str]] | None:
        """Retrieve a model or list of models from the Redis cache."""
        data = await self.redis.get(cache_key)
        if not data:
            return None

        try:
            deserialized_data = json.loads(data)
        except json.JSONDecodeError:
            return None

        return deserialized_data

    async def put_to_cache(self, cache_key: str, model: str | list[str]):
        """Put a model or list of models into the Redis cache."""
        await self.redis.set(cache_key, model, 240)

    async def add_to_queue(self, queue_name: str, data: str | list[str]):
        """Put a model or list of models into the Redis cache."""
        await self.redis.lpush(queue_name, data)


def get_redis_service(redis: Redis = Depends(get_redis)) -> RedisCacheService:
    return RedisCacheService(redis=redis)
