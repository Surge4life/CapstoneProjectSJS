#!/usr/bin/env bash
# Usage: ./use-render.sh https://your-udoc-web.onrender.com
# Points the native app at your live Render web app so GitHub-main -> Render deploys go live in-app.
set -e
URL="${1:?provide your Render web URL, e.g. https://gods-udoc-web.onrender.com}"
HERE="$(cd "$(dirname "$0")" && pwd)"
python3 - "$URL" "$HERE/capacitor.config.json" << 'PY'
import json, sys
url, path = sys.argv[1], sys.argv[2]
cfg = json.load(open(path))
cfg.setdefault("server", {})["url"] = url.rstrip("/")
cfg["server"].update({"androidScheme":"https","cleartext":True,"allowNavigation":["*"]})
json.dump(cfg, open(path,"w"), indent=2)
print("capacitor.config.json server.url ->", url)
PY
echo "Now rebuild: ./build-apk.sh"
