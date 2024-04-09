#!/bin/bash

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  echo "Waiting for PostgreSQL to start..."
  sleep 10
done

echo "PostgreSQL started. Applying migrations..."
alembic upgrade head

# Запуск FastAPI
pytest tests.py