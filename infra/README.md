## Local development (Docker)

Callex runs using Docker Compose with two services:
- `backend` (FastAPI API)
- `db` (PostgreSQL)

### Services overview

- **db**
  - PostgreSQL 16
  - Stores all bookings
  - Uses a Docker volume to persist data

- **backend**
  - FastAPI application
  - Exposes REST API on port 8000
  - Connects to PostgreSQL via internal Docker network

### Run locally

```bash
cp .env.example .env
docker compose -f infra/docker-compose.yml up -d --build
