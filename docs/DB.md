# Database (PostgreSQL + SQLAlchemy + Alembic)

## Overview
- PostgreSQL runs via Docker Compose as service `db`
- Backend uses SQLAlchemy ORM
- Alembic manages migrations (schema changes)

---

## Connection URLs

### Inside Docker network (backend -> db)
```
postgresql://callex:callexpass@db:5432/callex
```

### From host machine (CLI tools / Alembic from host)
```
postgresql://callex:callexpass@localhost:5432/callex
```

---

## Common DB Operations

### Open a psql shell inside the DB container
```bash
docker exec -it callex-db psql -U callex -d callex
```

### List tables
Inside `psql`:
```sql
\dt
```

### Show table schema
Inside `psql`:
```sql
\d bookings
```

---

## Alembic Workflow

### Create a migration (autogenerate)

1) Ensure environment is running:
```bash
./scripts/dev-up.sh
```

2) From `backend/`, export database URL:
```bash
cd backend
export DATABASE_URL="postgresql://callex:callexpass@localhost:5432/callex"
```

3) Autogenerate migration:
```bash
alembic revision --autogenerate -m "describe change"
```

### Apply migrations
```bash
alembic upgrade head
```

### Check current revision
```bash
alembic current
```

### Show migration history
```bash
alembic history
```

---

## Reset database (DANGEROUS)

This deletes all DB data:
```bash
./scripts/dev-reset.sh
```

---

## Notes
- Prefer running migrations through `./scripts/dev-up.sh` (default workflow).
- Manual Alembic commands should be used only for debugging or creating new migrations.
