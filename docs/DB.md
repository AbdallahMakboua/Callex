# Database (Postgres + SQLAlchemy + Alembic)

## Overview
- Postgres runs via Docker Compose as service `db`
- Backend uses SQLAlchemy ORM
- Alembic manages migrations (schema changes)

## Connection URLs
Inside Docker network (backend -> db):
postgresql://callex:callexpass@db:5432/callex

From local machine (CLI tools / alembic local):
postgresql://callex:callexpass@localhost:5432/callex

## Generate migration
1) Ensure DB is running:
docker compose -f infra/docker-compose.yml up -d --build

2) Export DATABASE_URL (local):
cd backend
export DATABASE_URL="postgresql://callex:callexpass@localhost:5432/callex"

3) Autogenerate migration:
alembic revision --autogenerate -m "create bookings table"

## Apply migration
alembic upgrade head

## Verify table
cd ..
docker exec -it callex-db psql -U callex -d callex -c "\dt"
