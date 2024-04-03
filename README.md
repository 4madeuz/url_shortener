### url_shorter
Асинхронный веб-сервис для сокращения URL-адресов.

## Описание работы

Асинхронный веб-сервис для сокращения URL-адресов. При отправке запроса
для получения оригинальной ссылки в Redis записывается timestap запроса,
далее worker переносит информацию из Redis в PostgreSQL. Для уменьшения
нагрузки на БД кэшируются запросы на получения оригинальной ссылки. Небольшие
тесты запускаются в отдельном compose.

Документация -- http://127.0.0.1:8000/api/openapi/

## Стек:
- Python
- FastApi
- PostgreSQL
- Redis
- SQLAlchemy
- Pydantic
- Docker
- uvicorn
- swagger
- Pytest


## Запуск проекта
 
 env.example -> .env

 ./url_service/entrypoint.sh -> LF

# Docker

 docker-compose up -d --build

 docker-compose up для запуска основного сервиса

 docker-compose -f docker-compose-tests.yaml up -d --build

 docker-compose -f docker-compose-tests.yaml up для тестов

 Миграции прменяются автоматически при запуске контейнера
