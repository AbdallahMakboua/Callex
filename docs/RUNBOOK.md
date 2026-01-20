
## `docs/RUNBOOK.md`

```md
# Callex Runbook

This document describes how to run, test, debug, and stop the Callex project locally.

---

## Overview

Local development is fully automated using shell scripts located in the `scripts/` directory.
Manual Docker or Alembic commands should not be needed during daily development.

---

## Start Local Environment

```bash
./scripts/dev-up.sh
```

This script performs:
- Docker Compose build and startup
- PostgreSQL container initialization
- Alembic migrations execution
- Backend health check

Backend URL:
```
http://localhost:8000
```

---

## Database Migrations

Migrations are handled using **Alembic**.

They are automatically applied during startup by `dev-up.sh`.

Manual run (only if required):

```bash
cd backend
export DATABASE_URL="postgresql://callex:callexpass@localhost:5432/callex"
alembic -c alembic.ini upgrade head
```

---

## API Testing

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"ok"}
```

---

### Create Booking

```bash
curl -X POST http://localhost:8000/book \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","phone":"+000000000","date":"2026-01-20","time":"10:00:00"}'
```

Behavior:
- First request → `201 Created`
- Same slot again → `409 Conflict`

---

## Logs

### Backend logs

```bash
./scripts/dev-logs.sh backend
```

### Database logs

```bash
./scripts/dev-logs.sh db
```

---

## Stop Services

### Stop containers (keep data)

```bash
./scripts/dev-down.sh
```

### Stop containers and wipe database

```bash
./scripts/dev-reset.sh
```

Use reset **only when schema or data must be rebuilt from scratch**.

---

## Common Issues

### Internal Server Error on booking

Cause:
- Database migrations not applied

Fix:
```bash
./scripts/dev-up.sh
```

---

### Database host confusion

- Inside Docker: `db`
- On host machine: `localhost`

Handled automatically by scripts.
```

---