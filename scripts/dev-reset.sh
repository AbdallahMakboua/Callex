#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/infra/docker-compose.yml"

echo "==> STOP + DELETE volumes (DB will be wiped)"
docker compose -f "$COMPOSE_FILE" down -v
echo "==> Done. Next run needs migrations again (dev-up)."
