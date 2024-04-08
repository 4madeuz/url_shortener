from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from src.core.config import settings

Base = declarative_base()

engine = create_async_engine(settings.dsn, echo=True, future=True)
async_session = sessionmaker(  # type: ignore
    engine, class_=AsyncSession, expire_on_commit=False,
)


async def get_session() -> AsyncSession:  # type: ignore
    async with async_session() as session:
        yield session
