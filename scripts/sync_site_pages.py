#!/usr/bin/env python3
"""
Sync docs/index.html "Latest" and docs/archive.html table from site-manifest.json.

Run from repo root: python3 scripts/sync_site_pages.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path


def load_manifest(root: Path) -> dict:
    with open(root / "scripts" / "site-manifest.json", encoding="utf-8") as f:
        return json.load(f)


def sorted_briefs(m: dict) -> list[dict]:
    return sorted(m["briefs"], key=lambda b: b["date"], reverse=True)


def build_index_latest(briefs: list[dict], max_items: int = 5) -> str:
    lines = ["      <ul class=\"tight\">"]
    for b in briefs[:max_items]:
        href = f"briefs/{b['slug']}.html"
        title = escape(b["title"])
        summary = escape(b["summary"])
        lines.extend(
            [
                "        <li>",
                f'          <a href="{escape(href)}"><strong>{title}</strong></a>',
                f"          — {summary}",
                "        </li>",
            ]
        )
    lines.append("      </ul>")
    return "\n".join(lines)


def build_archive_tbody(briefs: list[dict]) -> str:
    lines = ["        <tbody>"]
    for b in briefs:
        href = f"briefs/{b['slug']}.html"
        tags_list = b.get("tags", [])
        tags = ", ".join(tags_list) or "—"
        tags_attr = "|".join(t.lower().strip() for t in tags_list if t.strip())
        title_attr = b["title"].lower()
        lines.extend(
            [
                f'          <tr class="archive-row" data-tags="{escape(tags_attr)}" data-title="{escape(title_attr)}" data-date="{escape(b["date"])}">',
                f'            <td data-col="Date">{escape(b["date"])}</td>',
                "            <td>",
                f'              <a href="{escape(href)}">{escape(b["title"])}</a>',
                "            </td>",
                f'            <td data-col="Topic tags">{escape(tags)}</td>',
                "          </tr>",
            ]
        )
    lines.append("        </tbody>")
    return "\n".join(lines)


def replace_index_latest(text: str, latest_html: str) -> str:
    pattern = re.compile(r"(\s*<h2>Latest</h2>\n)(\s*<ul class=\"tight\">.*?</ul>)", re.DOTALL)
    out, n = pattern.subn(r"\1" + latest_html, text, count=1)
    if n != 1:
        raise RuntimeError("Could not locate Latest list in docs/index.html")
    return out


def replace_archive_tbody(text: str, tbody_html: str) -> str:
    pattern = re.compile(r"(\s*<table[^>]*>\n(?:.|\n)*?<thead>(?:.|\n)*?</thead>\n)(\s*<tbody>.*?</tbody>)", re.DOTALL)
    out, n = pattern.subn(r"\1" + tbody_html, text, count=1)
    if n != 1:
        raise RuntimeError("Could not locate archive table body in docs/archive.html")
    return out


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    m = load_manifest(root)
    briefs = sorted_briefs(m)

    index_path = root / "docs" / "index.html"
    archive_path = root / "docs" / "archive.html"

    index_text = index_path.read_text(encoding="utf-8")
    archive_text = archive_path.read_text(encoding="utf-8")

    index_text = replace_index_latest(index_text, build_index_latest(briefs))
    archive_text = replace_archive_tbody(archive_text, build_archive_tbody(briefs))

    index_path.write_text(index_text, encoding="utf-8")
    archive_path.write_text(archive_text, encoding="utf-8")

    print("wrote docs/index.html")
    print("wrote docs/archive.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

