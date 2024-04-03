import asyncio
import json
import uuid
from datetime import datetime

from config import settings
from redis.asyncio import Redis
from schemas import URLCashTimestamp
from sqlalchemy import ARRAY, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class URL(Base):
    __tablename__ = "urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(String)
    short_url = Column(String, unique=True)
    timestamps = Column(ARRAY(DateTime))


async def consumer(queue_name, async_session):
    redis = Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True,
        )
    _, data = await redis.brpop(queue_name)
    print(f'Consumed: {data}')

    data_dict = json.loads(data)
    url_id = data_dict['id']
    timestamp = data_dict['timestamp']
    timestamp = URLCashTimestamp(**data_dict)

    async with async_session() as session:
        url_data = await session.get(URL, url_id)
        if url_data:
            data2 = url_data.timestamps.copy()
            data2.append(timestamp.timestamp)
            url_data.timestamps = data2
            session.add(url_data)
            await session.commit()


if __name__ == "__main__":
    async_engine = create_async_engine(settings.dsn, echo=True, future=True)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    asyncio.run(consumer('timestamps', async_session))
