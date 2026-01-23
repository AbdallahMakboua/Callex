# Callex Runbook

Single source of truth for running, testing, debugging, and stopping Callex locally.

---

## Prerequisites

- Docker Desktop (running)
- Git
- Bash shell (macOS/Linux)
- (Optional) `jq` for pretty JSON output

Verify Docker:
```bash
docker --version
docker compose version
```

---

## Repository Structure (relevant)

```
.
├── backend/              # FastAPI application
├── docs/                 # Documentation
├── scripts/              # Operational scripts (preferred workflow)
├── docker-compose.yml    # Local orchestration
└── README.md
```

All commands must be executed from repository root.

---

## Make scripts executable (once)

```bash
chmod +x scripts/*.sh
```

---

## Start local environment (PRIMARY)

```bash
./scripts/dev-up.sh
```

What it does (in order):
1. Builds Docker images
2. Starts PostgreSQL container
3. Starts backend container
4. Applies Alembic migrations
5. Runs a health smoke test

Backend URL:
```
http://localhost:8000
```

---

## Verify health

```bash
curl http://localhost:8000/health
```

Expected:
```json
{"status":"ok"}
```

---

## Test booking

### Script (preferred)
```bash
./scripts/dev-test-book.sh 2026-01-20 10:00:00
```

Expected:
- First call: `201 Created`
- Same slot again: `409 Conflict`

---

## Test slots

### Script (preferred)
```bash
./scripts/dev-test-slots.sh 2026-01-20
```

### Manual
```bash
curl "http://localhost:8000/slots?date=2026-01-20"
```

---

## AI Availability (Integration)

### Script
```bash
./scripts/dev-test-ai-availability.sh 2026-01-20 any
./scripts/dev-test-ai-availability.sh 2026-01-20 morning
./scripts/dev-test-ai-availability.sh 2026-01-20 afternoon
./scripts/dev-test-ai-availability.sh 2026-01-20 evening
```

---

## AI Booking (Integration)

### Suggest all available slots (no time)
```bash
./scripts/dev-test-ai-book.sh 2026-01-20 morning
```

### Book a chosen time
```bash
./scripts/dev-test-ai-book.sh 2026-01-20 any 12:00
```

### Request a booked/unavailable time (expects 2 closest suggestions)
```bash
./scripts/dev-test-ai-book.sh 2026-01-20 any 11:30
```

---

## Logs

### Backend logs
```bash
./scripts/dev-logs.sh backend
```

### DB logs
```bash
./scripts/dev-logs.sh db
```

### All logs (raw)
```bash
docker compose logs -f
```

---

## Stop services

### Stop containers (keep DB data)
```bash
./scripts/dev-down.sh
```

### Full reset (DESTROYS DATA)
```bash
./scripts/dev-reset.sh
```

Use reset only when you must rebuild the DB from scratch.

---

## Update local repo to latest from GitHub

### Update main
```bash
git checkout main
git fetch origin
git pull
```

### Update your current branch with latest main (rebase)
```bash
git fetch origin
git rebase origin/main
```

---

## Cancel local edits and match remote

### Discard all local changes (DANGEROUS)
```bash
git fetch origin
git reset --hard origin/main
git clean -fd
```

---

## Common issues

### Scripts failing with 'command not found' or markdown characters
Cause: script file contains markdown (``` or ---).
Fix: overwrite the script with clean bash content and re-run `chmod +x`.

### Backend crashes with ModuleNotFoundError: No module named 'backend'
Cause: wrong import path `backend.*`.
Fix: use `app.*` imports only.

### Ports in use
```bash
lsof -i :8000
lsof -i :5432
```

---

## Operational checklist

- [ ] Docker running
- [ ] `chmod +x scripts/*.sh` (once)
- [ ] `./scripts/dev-up.sh`
- [ ] `curl /health` returns OK
- [ ] booking test returns 201 then 409
- [ ] slots returns structured output
