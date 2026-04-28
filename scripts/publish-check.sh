#!/usr/bin/env bash
# Run before opening a PR: regenerates RSS/sitemap from manifest, then validates internal links.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "==> python3 scripts/generate_feeds.py"
python3 scripts/generate_feeds.py
echo "==> python3 scripts/check_docs.py"
python3 scripts/check_docs.py
echo "==> publish-check: OK (review git diff for docs/rss.xml docs/sitemap.xml if you edited site-manifest.json)"
