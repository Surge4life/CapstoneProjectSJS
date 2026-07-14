#!/usr/bin/env bash
# UDOC client-station installer — provisions the governance core + edge stack as a system service.
# Air-gap: place pip wheels in ./wheels and pass --offline to install without internet.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OFFLINE=""
[ "$1" = "--offline" ] && OFFLINE="--no-index --find-links $(pwd)/wheels"
echo "▶ UDOC Station install — jurisdiction $(python3 -c 'import json;print(json.load(open("station.config.json"))["jurisdiction"])')"
python3 -m venv "$ROOT/.udoc-venv"
. "$ROOT/.udoc-venv/bin/activate"
pip install --upgrade pip $OFFLINE >/dev/null
pip install $OFFLINE -r "$ROOT/platform-core/requirements.txt"
echo "▶ initialising governance core (seed)"
( cd "$ROOT/platform-core" && python3 seed.py ) || true
# systemd unit (Linux production stations)
UNIT=/etc/systemd/system/udoc-station.service
if [ -w /etc/systemd/system ] 2>/dev/null; then
cat > "$UNIT" <<UNITEOF
[Unit]
Description=UDOC Sovereign AI Governance Station
After=network.target
[Service]
WorkingDirectory=$ROOT/platform-core
ExecStart=$ROOT/.udoc-venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8077
Restart=always
[Install]
WantedBy=multi-user.target
UNITEOF
systemctl daemon-reload && systemctl enable --now udoc-station.service && echo "▶ udoc-station.service enabled"
else
echo "▶ (no systemd write access — start manually: uvicorn app.main:app --host 0.0.0.0 --port 8077)"
fi
echo "▶ install complete. Validate with: ./udoc-station/run_test_env.sh  (or)  python3 udoc-station/bringup_selftest.py"
