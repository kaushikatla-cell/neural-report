#!/usr/bin/env bash
# Run before opening a PR: regenerates feeds/pages/OG assets, then validates links + editorial QA.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if ! python3 -c "import PIL" 2>/dev/null; then
  echo "Install Pillow: python3 -m pip install -r requirements.txt" >&2
  exit 1
fi
echo "==> python3 scripts/generate_feeds.py"
python3 scripts/generate_feeds.py
echo "==> python3 scripts/sync_site_pages.py"
python3 scripts/sync_site_pages.py
echo "==> python3 scripts/generate_og_images.py"
python3 scripts/generate_og_images.py
echo "==> python3 scripts/check_docs.py"
python3 scripts/check_docs.py
echo "==> python3 scripts/check_briefs.py"
python3 scripts/check_briefs.py
echo "==> publish-check: OK (review git diff: feeds, index/archive sync, docs/images/og*.png, brief meta)"
