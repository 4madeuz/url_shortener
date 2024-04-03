from abc import ABC, abstractmethod


class AbstractCacheService(ABC):
    """Абстрактный класс-интерфейс для сервисов кэширования"""

    @abstractmethod
    async def put_to_cache(self, *args, **kwargs):
        """Записывает значение в множество."""
        raise NotImplementedError

    @abstractmethod
    async def get_from_cache(self, *args, **kwargs):
        """Возвращает pipline."""
        raise NotImplementedError

    async def add_to_queue(self, *args, **kwargs):
        """Добавляет в очередь"""
        raise NotImplementedError


class AbstractDBService(ABC):
    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_by_field(self, *args, **kwargs):
        raise NotImplementedError
