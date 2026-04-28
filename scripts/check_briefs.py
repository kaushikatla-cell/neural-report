#!/usr/bin/env python3
"""
Editorial QA for docs/briefs/*.html.

Checks:
- required headings exist
- minimum number of source links
- corrections and methodology links exist
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRIEFS_DIR = ROOT / "docs" / "briefs"

REQUIRED_SNIPPETS = (
    "<h2>TL;DR</h2>",
    "<h2>Claims and evidence</h2>",
    "<h2>Still uncertain because",
    "<h2>Sources",
)


def source_link_count(html: str) -> int:
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL | re.IGNORECASE)
    block = m.group(1) if m else html
    return len(re.findall(r"<a\s+href=", block, re.IGNORECASE))


def main() -> int:
    errors: list[str] = []
    brief_files = sorted(BRIEFS_DIR.glob("20*.html"))
    for path in brief_files:
        html = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)

        for snippet in REQUIRED_SNIPPETS:
            if snippet not in html:
                errors.append(f"{rel}: missing required section containing {snippet!r}")

        if source_link_count(html) < 2:
            errors.append(f"{rel}: fewer than 2 links detected in main content")

        if "../corrections.html" not in html:
            errors.append(f"{rel}: missing link to ../corrections.html")
        if "../methodology.html" not in html:
            errors.append(f"{rel}: missing link to ../methodology.html")

    if errors:
        print("check_briefs: editorial QA failed\n")
        for e in errors:
            print(e)
        return 1

    print(f"check_briefs: ok ({len(brief_files)} briefs passed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

