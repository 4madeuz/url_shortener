from redis.asyncio import Redis

redis: Redis | None = None


async def get_redis() -> Redis | None:
    """Get the Redis instance."""
    return redis
