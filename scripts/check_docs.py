#!/usr/bin/env python3
"""
Validate that relative hrefs in docs/*.html point to real files (static check, no network).
Run from repository root: python3 scripts/check_docs.py
"""
from __future__ import annotations

import os
import re
import sys

DOCS = "docs"
# hrefs to ignore (non-file)
SKIP_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "data:",
    "javascript:",
)
# fragment-only
def should_skip(href: str) -> bool:
    h = href.strip()
    if not h or h.startswith("#"):
        return True
    for p in SKIP_PREFIXES:
        if h.startswith(p):
            return True
    return False


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs = os.path.join(root, DOCS)
    if not os.path.isdir(docs):
        print("error: docs/ not found", file=sys.stderr)
        return 1

    href_re = re.compile(r"""href\s*=\s*["']([^"']+)["']""", re.I)
    errors: list[str] = []

    for dirpath, _dirs, files in os.walk(docs):
        for f in files:
            if not f.endswith((".html", ".xhtml")):
                continue
            path = os.path.join(dirpath, f)
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            for m in href_re.finditer(text):
                href = m.group(1)
                if should_skip(href):
                    continue
                # strip query and hash
                path_part = href.split("#", 1)[0].split("?", 1)[0]
                if not path_part:
                    continue
                if path_part.startswith("/"):
                    # absolute on site — for this project, treat as relative to docs/ (ignore /neural-report prefix)
                    rel = path_part.lstrip("/")
                    if rel.startswith("neural-report/"):
                        rel = rel.split("/", 1)[1]
                    target = os.path.normpath(os.path.join(docs, rel))
                else:
                    target = os.path.normpath(os.path.join(dirpath, path_part))
                if not os.path.exists(target):
                    errors.append(f"{os.path.relpath(path, root)}: href {href!r} -> {os.path.relpath(target, root)} (missing)")

    if errors:
        print("check_docs: internal link check failed\n", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("check_docs: ok (all relative hrefs resolve under docs/)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
