# Callex

Callex is a lightweight appointment booking backend built with FastAPI, PostgreSQL, Docker, and Alembic.

This repository focuses on:
- Clean local development workflow
- Database migrations
- Simple, reliable API behavior

---

## Local Development (Quick Start)

### Prerequisites
- Docker Desktop
- Git
- macOS / Linux (bash-based scripts)

---

### Start the project
```bash
./scripts/dev-up.sh
````

This will:

* Build and start Docker containers
* Apply database migrations
* Verify backend health

---

### Create a test booking

```bash
./scripts/dev-test-book.sh 2026-01-20 10:00:00
```

---

### View logs

```bash
./scripts/dev-logs.sh backend
./scripts/dev-logs.sh db
```

---

### Stop services

```bash
./scripts/dev-down.sh
```

---

### Reset database (DANGER)

```bash
./scripts/dev-reset.sh
```

This will **delete all database data** and requires migrations to be re-applied.

```