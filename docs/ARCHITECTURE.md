# Architecture Overview

High-level design decisions for Callex.

---

## Stack

- Backend: FastAPI
- Database: PostgreSQL 16
- ORM: SQLAlchemy
- Migrations: Alembic
- Containerization: Docker + Docker Compose

---

## Local Development Strategy

Local development is script-driven instead of command-driven.

Reasons:
- Prevent environment-specific mistakes
- Standardize setup for all contributors
- Reduce onboarding time
- Avoid accidental data loss

All critical operations (startup, migrations, testing, shutdown) are executed via scripts in `scripts/`.

---

## API Design

- Stateless REST API
- Explicit conflict handling (HTTP 409) on strict booking endpoint
- AI helper endpoints provide user-friendly suggestions without changing strict API behavior
- Backend fails fast on invalid state (HTTP 400)

---

## Availability Model

- Working hours: 09:00 → 17:00
- Slot interval: 30 minutes (MVP default)
- Booked slots are marked unavailable in `/slots`
- AI preference buckets:
  - morning: 09:00–12:00
  - afternoon: 12:00–15:00
  - evening: 15:00–17:00

---

## Database

- PostgreSQL runs via Docker Compose as service `db`
- SQLAlchemy models define tables
- Alembic manages schema changes via migrations

### Connection URLs

Inside Docker network (backend → db):
```
postgresql://callex:callexpass@db:5432/callex
```

From host machine (CLI tools):
```
postgresql://callex:callexpass@localhost:5432/callex
```

### Migration workflow (standard)

1) Start environment:
```bash
./scripts/dev-up.sh
```

2) Create a migration (from `backend/`):
```bash
cd backend
export DATABASE_URL="postgresql://callex:callexpass@localhost:5432/callex"
alembic revision --autogenerate -m "describe change"
```

3) Apply migrations:
```bash
alembic upgrade head
```

---

## Future Extensions

- Authentication and authorization
- External calendar integrations
- Multi-tenant support
- Deployment (EC2/ECS) + CI/CD pipelines
