#!/usr/bin/env python3
"""
Regenerate docs/rss.xml (RSS 2.0), docs/atom.xml (Atom 1.0), and docs/sitemap.xml
from scripts/site-manifest.json.
Run from repo root: python3 scripts/generate_feeds.py
"""
from __future__ import annotations

import json
from email.utils import formatdate
from datetime import datetime, timezone
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


def rss_pub_date(iso_date: str) -> str:
    y, m, d = map(int, iso_date.split("-"))
    dt = datetime(y, m, d, 12, 0, 0, tzinfo=timezone.utc)
    return formatdate(dt.timestamp(), usegmt=True)


def write_rss_feed(root: Path, m: dict) -> None:
    base = m["base_url"].rstrip("/")
    feed = m["feed"]
    briefs = sorted(m["briefs"], key=lambda b: b["date"], reverse=True)
    latest = briefs[0]["date"] if briefs else "1970-01-01"

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        "  <channel>",
        f"    <title>{escape(feed['title'])}</title>",
        f"    <link>{escape(base + '/')}</link>",
        f"    <description>{escape(feed['subtitle'])}</description>",
        "    <language>en-us</language>",
        f"    <lastBuildDate>{rss_pub_date(latest)}</lastBuildDate>",
        f'    <atom:link href="{escape(base + "/rss.xml")}" rel="self" type="application/rss+xml" />',
    ]
    for b in briefs:
        url = brief_url(base, b["slug"])
        lines.append("    <item>")
        lines.append(f"      <title>{escape(b['title'])}</title>")
        lines.append(f"      <link>{escape(url)}</link>")
        lines.append(f'      <guid isPermaLink="true">{escape(url)}</guid>')
        lines.append(f"      <pubDate>{rss_pub_date(b['date'])}</pubDate>")
        lines.append(f"      <description>{escape(b['summary'])}</description>")
        for tag in b.get("tags", []):
            lines.append(f"      <category>{escape(tag)}</category>")
        lines.append("    </item>")
    lines.extend(["  </channel>", "</rss>"])
    out = root / "docs" / "rss.xml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(root)}")


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
        f'  <link href="{escape(base + "/atom.xml")}" rel="self" />',
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
        for tag in b.get("tags", []):
            lines.append(f'    <category term="{escape(tag)}" />')
        lines.append("  </entry>")

    lines.append("</feed>")
    out = root / "docs" / "atom.xml"
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

    for path, cfreq, pri in (
        ("rss.xml", "weekly", "0.35"),
        ("atom.xml", "weekly", "0.35"),
        ("llms.txt", "monthly", "0.25"),
    ):
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(base + '/' + path)}</loc>")
        lines.append(f"    <changefreq>{cfreq}</changefreq>")
        lines.append(f"    <priority>{pri}</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")
    out = root / "docs" / "sitemap.xml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(root)}")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    m = load_manifest(root)
    write_rss_feed(root, m)
    write_atom_feed(root, m)
    write_sitemap(root, m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
