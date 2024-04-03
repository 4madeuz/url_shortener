import asyncio
import json

from config import settings
from models import URL
from redis.asyncio import Redis
from schemas import URLCashTimestamp
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


async def consumer(queue_name, exit_event, async_session):
    redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        decode_responses=True,
        )

    try:
        while not exit_event.is_set():
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

    except asyncio.CancelledError:
        print("Consumer cancelled")
    finally:
        await redis.close()


async def main():
    queue_name = 'timestamps'
    exit_event = asyncio.Event()

    async_engine = create_async_engine(settings.dsn, echo=True, future=True)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    consumer_task = asyncio.create_task(consumer(queue_name, exit_event, async_session))

    await asyncio.gather(consumer_task, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())
