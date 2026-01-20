

## `docs/ARCHITECTURE.md`

```md
# Architecture Overview

This document explains high-level design decisions for Callex.

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

All critical operations (startup, migrations, testing, shutdown) are executed via scripts.

---

## Database Management

- Schema changes are handled via Alembic migrations
- No manual SQL required
- Database lifecycle:
  1. Start containers
  2. Apply migrations
  3. Run application

---

## API Design

- Stateless REST API
- Explicit conflict handling (HTTP 409)
- Database constraints enforce business rules
- Backend fails fast on invalid state

---

## Future Extensions

- Authentication and authorization
- AI-based availability logic
- External calendar integrations
- Multi-tenant support
```