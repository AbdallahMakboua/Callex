#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/infra/docker-compose.yml"
BACKEND_DIR="$ROOT_DIR/backend"

echo "==> Starting containers..."
docker compose -f "$COMPOSE_FILE" up -d --build

echo "==> Waiting a moment for Postgres..."
sleep 2

echo "==> Applying DB migrations (Alembic) from host..."
cd "$BACKEND_DIR"
export DATABASE_URL="postgresql://callex:callexpass@localhost:5432/callex"
alembic -c alembic.ini upgrade head

echo "==> Smoke test: /health"
curl -s http://localhost:8000/health || true
echo
echo "==> Done. Backend: http://localhost:8000"
