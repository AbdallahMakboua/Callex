#!/usr/bin/env bash
set -euo pipefail

DATE="${1:-2026-01-20}"
TIME="${2:-10:00:00}"

echo "==> POST /book (date=$DATE time=$TIME)"
curl -s -X POST http://localhost:8000/book \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Abdallah\",\"phone\":\"+971500000000\",\"date\":\"$DATE\",\"time\":\"$TIME\"}"
echo
