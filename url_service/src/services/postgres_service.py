from uuid import UUID
from typing import Type, TypeVar
from src.services.abstract import AbstractDBService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update
from pydantic import BaseModel

from src.db.postgres import Base

M = TypeVar("M", bound=Base)


class PostgresService(AbstractDBService):
    """Серивис для управления CRUD операциями в Postgres"""

    def __init__(self, session: AsyncSession, model_class: Type[M]):
        self.session = session
        self.model_class = model_class

    async def get_all(self) -> list[M]:
        """Получить список объектов"""
        async with self.session.begin():
            models = await self.session.execute(select(self.model_class))
            return models.unique().scalars().all()

    async def get_by_id(self, model_id: UUID) -> M | None:
        """Получить объект по id"""
        async with self.session.begin():
            model = await self.session.get(self.model_class, model_id)
            return model

    async def get_by_field(self, field: str, value: any) -> M | None:
        """Получить объект по значению поля"""
        async with self.session.begin():
            query = select(self.model_class).where(getattr(self.model_class, field) == value)
            model = await self.session.execute(query)
            return model.scalars().first()

    async def create(self, model_schema: BaseModel) -> M:
        """Создать объет"""
        model_instance = self.model_class(**model_schema.model_dump())
        self.session.add(model_instance)
        await self.session.commit()
        return model_instance

    async def update(self, model_id: UUID, model_schema: BaseModel) -> M | None:
        """Обновить объект по id"""
        model_data = model_schema.model_dump(exclude_none=True)
        async with self.session.begin():
            model = await self.session.get(self.model_class, model_id)
            if model is None:
                return None

            if model_data:
                await self.session.execute(
                    update(self.model_class)
                    .where(self.model_class.id == model_id)
                    .values(model_data)
                )
                self.session.expire_all()

            return await self.session.get(self.model_class, model_id)

    async def delete(self, model_id: UUID) -> M | None:
        """Удалить объект"""
        async with self.session.begin():
            result = await self.session.execute(
                delete(self.model_class)
                .where(self.model_class.id == model_id)
                .returning(self.model_class)
            )
            return result.scalar()
