#!/usr/bin/env bash
set -e

DATE="$1"

if [ -z "$DATE" ]; then
  echo "Usage: ./scripts/dev-test-slots.sh YYYY-MM-DD"
  exit 1
fi

echo "==> GET /slots (date=$DATE)"

if command -v jq >/dev/null 2>&1; then
  curl -s "http://localhost:8000/slots?date=$DATE" | jq .
else
  curl -s "http://localhost:8000/slots?date=$DATE"
fi
