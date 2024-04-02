from abc import ABC, abstractmethod


class AbstractCacheService(ABC):
    """Абстрактный класс-интерфейс для сервисов кэширования"""

    @abstractmethod
    async def add_to_set(self, *args, **kwargs):
        """Записывает значение в множество."""
        raise NotImplementedError

    @abstractmethod
    async def is_value_in_set(self, *args, **kwargs):
        """Проверяет, есть ли значение в множестве."""
        raise NotImplementedError

    @abstractmethod
    async def get_pipeline(self, *args, **kwargs):
        """Возвращает pipline."""
        raise NotImplementedError


class AbstractDBService(ABC):
    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def execute(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError
