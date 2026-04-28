#!/usr/bin/env python3
"""
Regenerate docs/rss.xml and docs/sitemap.xml from scripts/site-manifest.json.
Run from repo root: python3 scripts/generate_feeds.py
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape


def load_manifest(root: Path) -> dict:
    p = root / "scripts" / "site-manifest.json"
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def brief_url(base: str, slug: str) -> str:
    path = f"briefs/{slug}.html"
    if not base.endswith("/"):
        base = base + "/"
    return base + path


def write_atom_feed(root: Path, m: dict) -> None:
    base = m["base_url"].rstrip("/")
    feed = m["feed"]
    briefs = sorted(m["briefs"], key=lambda b: b["date"], reverse=True)
    latest = max(b["date"] for b in briefs) if briefs else "1970-01-01"
    updated_ts = f"{latest}T12:00:00Z"

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        f"  <title>{escape(feed['title'])}</title>",
        f"  <subtitle>{escape(feed['subtitle'])}</subtitle>",
        f'  <link href="{escape(base + "/rss.xml")}" rel="self" />',
        f'  <link href="{escape(base + "/")}" />',
        f"  <updated>{updated_ts}</updated>",
        f'  <id>{escape(base + "/")}</id>',
        "  <author>",
        f"    <name>{escape(feed['author_name'])}</name>",
        "  </author>",
    ]

    for b in briefs:
        url = brief_url(base, b["slug"])
        ts = f"{b['date']}T12:00:00Z"
        lines.append("  <entry>")
        lines.append(f"    <title>{escape(b['title'])}</title>")
        lines.append(f'    <link href="{escape(url)}" />')
        lines.append(f'    <id>{escape(url)}</id>')
        lines.append(f"    <updated>{ts}</updated>")
        lines.append(f"    <summary>{escape(b['summary'])}</summary>")
        lines.append("  </entry>")

    lines.append("</feed>")
    out = root / "docs" / "rss.xml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(root)}")


def write_sitemap(root: Path, m: dict) -> None:
    base = m["base_url"].rstrip("/")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for s in m["sitemap_static"]:
        if s["path"] == "":
            loc = base + "/"
        else:
            loc = base + "/" + s["path"]
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(loc)}</loc>")
        lines.append(f"    <changefreq>{escape(s['changefreq'])}</changefreq>")
        lines.append(f"    <priority>{escape(s['priority'])}</priority>")
        lines.append("  </url>")

    for b in sorted(m["briefs"], key=lambda x: x["date"], reverse=True):
        loc = brief_url(base, b["slug"])
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(loc)}</loc>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append("    <priority>0.85</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")
    out = root / "docs" / "sitemap.xml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(root)}")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    m = load_manifest(root)
    write_atom_feed(root, m)
    write_sitemap(root, m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
