import os

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(os.path.dirname(BASE_DIR), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )
    # Настройки подключения к БД
    scheme: str = "postgresql+asyncpg"
    postgres_db: str = Field(default="shortener")
    postgres_user: str = Field(default="app")
    postgres_password: str = Field(default="123qwe")
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    # Настройки Redis
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    cache_expire_in_seconds: int = 60 * 5  # 5 минут

    @property
    def dsn(self) -> PostgresDsn:
        return str(
            PostgresDsn.build(
                scheme=self.scheme,
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                path=self.postgres_db,
            )
        )


settings = Settings()
