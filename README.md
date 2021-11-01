# Async FastAPI Boilerplate

Async FastAPI + Asyncio SQLAlchemy + postgres + Alembic migrations + Celery + Flower (with grafana) + Traefik

## Create new models

- `docker-compose -f docker-compose.dev.yml run backend alembic revision --autogenerate`
- `docker-compose -f docker-compose.dev.yml run backend alembic upgrade head`

## Setup grafana

Follow Add Prometheus As a Data Source In Grafana [Link](https://flower.readthedocs.io/en/latest/prometheus-integration.html#celery-flower-prometheus-grafana-integration-guide)

## TODO:

- react frontend
- cors
