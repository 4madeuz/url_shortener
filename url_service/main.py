from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from redis.asyncio import Redis
from src.api.v1 import urls
from src.core.config import settings
from src.db import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(
        host='localhost',
        port=settings.redis_port,
        db=0,
        decode_responses=True,
    )
    yield
    await redis.redis.close()


app = FastAPI(
    title='Url shortener',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    lifespan=lifespan,
)

app.include_router(
    urls.router, prefix='/shortener', tags=['shortener'],
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app', host='0.0.0.0', port=8000,
    )
