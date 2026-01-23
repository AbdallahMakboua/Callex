#!/usr/bin/env bash
set -e

DATE="$1"
PREF="${2:-any}"

if [ -z "$DATE" ]; then
  echo "Usage: ./scripts/dev-test-ai-availability.sh YYYY-MM-DD [any|morning|afternoon|evening]"
  exit 1
fi

echo "==> GET /ai/availability (date=$DATE preference=$PREF)"

if command -v jq >/dev/null 2>&1; then
  curl -s "http://localhost:8000/ai/availability?date=$DATE&preference=$PREF" | jq .
else
  curl -s "http://localhost:8000/ai/availability?date=$DATE&preference=$PREF"
fi
