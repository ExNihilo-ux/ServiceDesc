# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    alembic \
    sqlalchemy[asyncio] \
    asyncpg \
    psycopg2-binary

COPY alembic.ini .
COPY alembic/ ./alembic/
COPY app/ ./app/