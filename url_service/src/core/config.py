from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Настройки подключения к БД
    scheme: str = 'postgresql+asyncpg'
    postgres_db: str = Field(default='shortener')
    postgres_user: str = Field(default='app')
    postgres_password: str = Field(default='123qwe')
    postgres_host: str = Field(default='localhost')
    postgres_port: int = Field(default=5432)
    # Настройки Redis
    redis_host: str = Field(default='localhost')
    redis_port: int = Field(default=6379)
    cache_expire_in_seconds: int = 60 * 5  # 5 минут

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=self.scheme,
                username=self.postgres_user,
                password=self.postgres_password,
                host='localhost',
                port=self.postgres_port,
                path=self.postgres_db,
            )
        )


settings = Settings()
