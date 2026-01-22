
---

## `scripts/dev-test-slots.sh`

```bash
#!/usr/bin/env bash
set -e

DATE="$1"

if [ -z "$DATE" ]; then
  echo "Usage: ./scripts/dev-test-slots.sh YYYY-MM-DD"
  exit 1
fi

echo "==> GET /slots (date=$DATE)"

curl -s "http://localhost:8000/slots?date=$DATE" | jq .
