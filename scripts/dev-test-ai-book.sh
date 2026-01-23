#!/usr/bin/env bash
set -e

DATE="${1:-2026-01-20}"
ARG2="${2:-any}"
ARG3="${3:-}"

# If user provided date + time only (ARG2 looks like HH:MM), treat it as TIME
if [[ "$ARG2" =~ ^[0-9]{2}:[0-9]{2}(:[0-9]{2})?$ ]] && [ -z "$ARG3" ]; then
  PREF="any"
  TIME="$ARG2"
else
  PREF="$ARG2"
  TIME="$ARG3"
fi

echo "==> POST /ai/book (date=$DATE preference=$PREF time=${TIME:-<none>})"

if [ -z "$TIME" ]; then
  BODY=$(cat <<JSON
{"name":"Abdallah","phone":"+971500000000","date":"$DATE","preference":"$PREF"}
JSON
)
else
  BODY=$(cat <<JSON
{"name":"Abdallah","phone":"+971500000000","date":"$DATE","preference":"$PREF","time":"$TIME"}
JSON
)
fi

if command -v jq >/dev/null 2>&1; then
  curl -s -X POST "http://localhost:8000/ai/book" \
    -H "Content-Type: application/json" \
    -d "$BODY" | jq .
else
  curl -s -X POST "http://localhost:8000/ai/book" \
    -H "Content-Type: application/json" \
    -d "$BODY"
fi
