#!/usr/bin/env python3
"""
Replace the public site base URL across tracked HTML, JSON, and key text files.

Use when moving from GitHub Pages to a custom domain (or the reverse).

  python3 scripts/rewrite_site_base.py \\
    'https://kaushikatla-cell.github.io/neural-report' \\
    'https://report.example.com'

Then run:
  python3 scripts/generate_feeds.py
  python3 scripts/generate_og_images.py
  python3 scripts/check_docs.py

Review git diff before committing (LLM-facing files like docs/llms.txt are included).
"""
from __future__ import annotations

import sys
from pathlib import Path

EXTRA_ROOT_FILES = (
    "docs/manifest.json",
    "scripts/site-manifest.json",
    "README.md",
    "CONTRIBUTING.md",
    "APPLICATION_BLURB.md",
    "metrics/LINK_AND_UX.md",
    "lychee.toml",
    "docs/js/nrp-core.js",
)


def collect_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    docs = root / "docs"
    if docs.is_dir():
        for p in docs.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix in {".html", ".txt", ".xml"}:
                files.add(p)
    for rel in EXTRA_ROOT_FILES:
        path = root / rel
        if path.is_file():
            files.add(path)
    return sorted(files)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: rewrite_site_base.py OLD_BASE NEW_BASE", file=sys.stderr)
        return 2
    old, new = sys.argv[1], sys.argv[2]
    if old == new:
        print("OLD_BASE and NEW_BASE are identical; nothing to do.")
        return 0
    root = Path(__file__).resolve().parent.parent
    n = 0
    for path in collect_files(root):
        text = path.read_text(encoding="utf-8")
        if old not in text:
            continue
        path.write_text(text.replace(old, new), encoding="utf-8")
        print(f"updated {path.relative_to(root)}")
        n += 1
    if n == 0:
        print("no files contained OLD_BASE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
