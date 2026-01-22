## `docs/RUNBOOK.md`

# Callex Runbook

This document is the single source of truth for running, testing, debugging, and stopping the Callex application locally.

---

## Purpose

- Provide deterministic local startup
- Eliminate manual Docker / Alembic usage
- Enable fast debugging and recovery
- Standardize workflow for all contributors

---

## Prerequisites

Required on host machine:

- Docker Desktop (running)
- Git
- Bash shell
- macOS or Linux

Verify Docker:

```bash
docker --version
docker compose version
````

---

## Repository Structure (Relevant)

```
.
├── backend/              # FastAPI application
├── docs/                 # Documentation
├── scripts/              # All operational commands
├── docker-compose.yml    # Local orchestration
└── README.md
```

All operations **must be executed from repository root**.

---

## Environment Variables

Local environment is fully defined inside Docker Compose.

No `.env` file is required for standard local usage.

Database credentials (internal):

* DB Name: `callex`
* User: `callex`
* Password: `callexpass`
* Port: `5432`

---
Make scripts executable (once)

From repo root:
```bash
chmod +x scripts/*.sh
```
---

## Start Local Environment (PRIMARY COMMAND)

```bash
./scripts/dev-up.sh
```

What this does (in order):

1. Builds Docker images
2. Starts PostgreSQL container
3. Starts backend container
4. Applies Alembic migrations
5. Waits for database readiness
6. Performs backend health check

Expected result:

* Containers running
* No errors in output
* Backend reachable

Backend URL:

```
http://localhost:8000
```

---

## Verify Application Health

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

If this fails → **application is not ready**.

---

## Create Test Booking (Recommended)

### Using script (preferred)

```bash
./scripts/dev-test-book.sh 2026-01-20 10:00:00
```

### Manual API call

```bash
curl -X POST http://localhost:8000/book \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Test User",
    "phone":"+000000000",
    "date":"2026-01-20",
    "time":"10:00:00"
  }'
```

Expected behavior:

* First request → `201 Created`
* Same date/time again → `409 Conflict`

This confirms:

* Database connectivity
* Business rules enforcement
* API correctness
---

## Get Available Slots

### Using script (preferred)

```bash
./scripts/dev-test-slots.sh 2026-01-20
```
Manual API call

```bash
curl "http://localhost:8000/slots?date=2026-01-20"
```

Expected behavior:

Returns slots between 09:00 and 17:00

Already booked slots are marked unavailable

---

## Logs and Debugging

### Backend logs (FastAPI)

```bash
./scripts/dev-logs.sh backend
```

### Database logs (PostgreSQL)

```bash
./scripts/dev-logs.sh db
```

### All containers (raw Docker)

```bash
docker compose logs -f
```

---

## Database Migrations

Migrations are managed using **Alembic**.

### Automatic (default)

* Applied automatically during `dev-up.sh`
* No action required

### Manual (only if debugging)

```bash
cd backend
export DATABASE_URL="postgresql://callex:callexpass@localhost:5432/callex"
alembic -c alembic.ini upgrade head
```

Manual migration should be **exceptional**, not normal workflow.

---

## Stop Services

### Stop containers (keep data)

```bash
./scripts/dev-down.sh
```

Use when:

* Finished development
* Want to resume later with same data

---

### Full reset (DESTROYS DATA)

```bash
./scripts/dev-reset.sh
```

What it does:

* Stops containers
* Removes volumes
* Deletes all database data

Use only when:

* Schema is broken
* Migration history is invalid
* Clean rebuild is required

---

## Common Issues & Fixes

### Backend not responding

Check:

```bash
docker compose ps
```

Fix:

```bash
./scripts/dev-down.sh
./scripts/dev-up.sh
```

---

### 500 Internal Server Error on booking

Cause:

* Database schema not applied

Fix:

```bash
./scripts/dev-up.sh
```

---

### Database connection errors

Important distinction:

* Inside Docker → host = `db`
* From host machine → host = `localhost`

This is already handled correctly by scripts.

---

### Port already in use

Check:

```bash
lsof -i :8000
lsof -i :5432
```

Fix:

* Stop conflicting services
* Or stop Callex and retry

---

## Golden Rules

* ❌ Do NOT run docker compose manually
* ❌ Do NOT apply migrations by hand unless debugging
* ✅ Always use scripts
* ✅ Run commands from repo root
* ✅ Reset only when necessary

---

## Operational Checklist (Quick)

* [ ] Docker running
* [ ] `./scripts/dev-up.sh`
* [ ] Health check OK
* [ ] Test booking works
* [ ] Logs clean

