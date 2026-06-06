#!/usr/bin/env bash
# Boot a local UDOC test environment for SaaS launch validation, then run the station self-test.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${UDOC_PORT:-8077}"
echo "▶ booting UDOC governance core (platform-core) on :$PORT ..."
cd "$ROOT/platform-core"
[ -f gods_core.db ] || python3 seed.py >/dev/null 2>&1 || true
python3 -m uvicorn app.main:app --host 127.0.0.1 --port "$PORT" >/tmp/udoc_station_api.log 2>&1 &
API_PID=$!
trap 'kill $API_PID 2>/dev/null || true' EXIT
sleep 6
echo "▶ running station bring-up self-test ..."
UDOC_API="http://127.0.0.1:$PORT" python3 "$ROOT/udoc-station/bringup_selftest.py"
RC=$?
echo "▶ test environment validated (exit $RC). API log: /tmp/udoc_station_api.log"
exit $RC
