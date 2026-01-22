#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/infra/docker-compose.yml"

echo "==> Stopping containers (keeping DB data)..."
docker compose -f "$COMPOSE_FILE" down
echo "==> Done."
