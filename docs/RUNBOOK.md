# Callex Runbook

## Prerequisites
- Docker Desktop installed
- Git installed

## Clone
git clone <repo-url>
cd Callex

## Run (Backend + Postgres)
docker compose -f infra/docker-compose.yml up -d --build

## Verify services
docker compose -f infra/docker-compose.yml ps

## Health check
curl http://localhost:8000/health

## Stop + reset DB volume (DANGER: deletes DB data)
docker compose -f infra/docker-compose.yml down -v

## Logs
docker compose -f infra/docker-compose.yml logs -f backend
docker compose -f infra/docker-compose.yml logs -f db
