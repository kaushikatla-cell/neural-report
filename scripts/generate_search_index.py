#!/usr/bin/env python3
"""
Generate docs/search-index.json for command palette and global autocomplete.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://kaushikatla-cell.github.io/neural-report"


def load_manifest() -> dict:
    return json.loads((ROOT / "scripts" / "site-manifest.json").read_text(encoding="utf-8"))


def read_html_title(path: Path) -> str:
    txt = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<title>(.*?)</title>", txt, re.IGNORECASE | re.DOTALL)
    if not m:
        return path.stem
    return re.sub(r"\s+", " ", m.group(1)).strip()


def read_meta_description(path: Path) -> str:
    txt = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', txt, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ""


def build_static_items() -> list[dict]:
    pages = [
        ("index.html", "home"),
        ("archive.html", "archive"),
        ("dashboard.html", "dashboard"),
        ("transparency.html", "transparency"),
        ("library.html", "library"),
        ("faq.html", "faq"),
        ("glossary.html", "glossary"),
        ("series.html", "series"),
        ("methodology.html", "methodology"),
        ("corrections.html", "corrections"),
        ("about.html", "about"),
        ("subscribe.html", "subscribe"),
    ]
    out = []
    for rel, kind in pages:
        p = ROOT / "docs" / rel
        if not p.exists():
            continue
        out.append(
            {
                "kind": kind,
                "title": read_html_title(p).replace(" — Neural Report", "").strip(),
                "summary": read_meta_description(p),
                "url": f"{BASE}/{rel}",
                "slug": rel.replace(".html", ""),
                "tags": [kind],
            }
        )
    return out


def build_brief_items(m: dict) -> list[dict]:
    out = []
    for b in m.get("briefs", []):
        slug = b["slug"]
        out.append(
            {
                "kind": "brief",
                "title": b["title"],
                "summary": b.get("summary", ""),
                "url": f"{BASE}/briefs/{slug}.html",
                "slug": slug,
                "date": b.get("date", ""),
                "tags": b.get("tags", []),
            }
        )
    return out


def build_library_items() -> list[dict]:
    path = ROOT / "research" / "paper_library.csv"
    if not path.exists():
        return []
    rows = []
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            title = (r.get("title") or "").strip()
            url = (r.get("url") or "").strip()
            if not title or not url:
                continue
            rows.append(
                {
                    "kind": "paper",
                    "title": title,
                    "summary": (r.get("why_it_matters") or "").strip(),
                    "url": url,
                    "slug": re.sub(r"[^a-z0-9-]+", "-", title.lower()).strip("-"),
                    "date": (r.get("year") or "").strip(),
                    "tags": [t for t in [(r.get("domain") or "").strip(), (r.get("source_type") or "").strip()] if t],
                }
            )
    return rows


def main() -> int:
    m = load_manifest()
    items = build_static_items() + build_brief_items(m) + build_library_items()
    payload = {
        "base_url": m.get("base_url", BASE),
        "generated_from": ["scripts/site-manifest.json", "research/paper_library.csv", "docs/*.html"],
        "total_items": len(items),
        "items": items,
    }
    out = ROOT / "docs" / "search-index.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

