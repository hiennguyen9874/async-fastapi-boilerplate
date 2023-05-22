# Async FastAPI Boilerplate

An API Boilerplate written in python with FastAPI and asyncio. Write restful API with fast development and developer friendly.

## Architecture

- models
- crud

## Features

- Full Docker integration (Docker based)
- Docker Compose integration and optimization for local development
- Production ready Python web server using Uvicorn and Gunicorn
- Python FastAPI backend:
  - OpenAPI
  - Validation
  - Serialization
  - Authentication jwt token
- Secure password hashing by default
- JWT token authentication
- SQLAlchemy models (can be used with Celery workers directly)
- Basic starting models for users (modify and remove as you need)
- Alembic migrations
- Celery worker that can import and use models and code from the rest of the backend selectively
- Load balancing with Traefik

## Technical

- fastapi
- sqlalchemy
- alembic
- celery
- sentry
- swagger

## Start Application

### Secret key

- `openssl rand -hex 32`

### Run

- run: `docker compose up`
- docs: `localhost:10081/docs` or redoc: `localhost:10081/redoc`

### Migration

- migrate: `docker-compose -f docker-compose.dev.yml run backend alembic revision --autogenerate`
- migration: `docker-compose -f docker-compose.dev.yml run backend alembic upgrade head`

### Setup grafana

Follow Add Prometheus As a Data Source In Grafana [Link](https://flower.readthedocs.io/en/latest/prometheus-integration.html#celery-flower-prometheus-grafana-integration-guide)
