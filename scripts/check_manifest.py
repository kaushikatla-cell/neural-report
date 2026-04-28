#!/usr/bin/env python3
"""
Validate scripts/site-manifest.json schema and invariants.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "scripts" / "site-manifest.json"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")


def ensure(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    try:
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"check_manifest: failed to parse JSON: {e}")
        return 1

    ensure(isinstance(data, dict), "manifest root must be an object", errors)
    for key in ("base_url", "feed", "briefs", "sitemap_static"):
        ensure(key in data, f"missing top-level key: {key}", errors)
    if errors:
        print("check_manifest: invalid\n")
        print("\n".join(errors))
        return 1

    ensure(isinstance(data["base_url"], str) and data["base_url"].startswith("https://"), "base_url must be https URL", errors)

    feed = data["feed"]
    ensure(isinstance(feed, dict), "feed must be object", errors)
    for k in ("title", "subtitle", "author_name"):
        ensure(isinstance(feed.get(k), str) and feed[k].strip(), f"feed.{k} must be non-empty string", errors)

    briefs = data["briefs"]
    ensure(isinstance(briefs, list) and len(briefs) > 0, "briefs must be a non-empty list", errors)
    slugs: set[str] = set()
    dates: set[str] = set()
    for i, b in enumerate(briefs):
        prefix = f"briefs[{i}]"
        ensure(isinstance(b, dict), f"{prefix} must be object", errors)
        if not isinstance(b, dict):
            continue
        for k in ("slug", "title", "date", "summary", "tags"):
            ensure(k in b, f"{prefix} missing key: {k}", errors)
        if "slug" in b:
            ensure(isinstance(b["slug"], str) and SLUG_RE.match(b["slug"]) is not None, f"{prefix}.slug invalid format", errors)
            if isinstance(b["slug"], str):
                ensure(b["slug"] not in slugs, f"duplicate slug: {b['slug']}", errors)
                slugs.add(b["slug"])
        if "date" in b:
            ensure(isinstance(b["date"], str) and DATE_RE.match(b["date"]) is not None, f"{prefix}.date invalid YYYY-MM-DD", errors)
            if isinstance(b["date"], str):
                dates.add(b["date"])
                if isinstance(b.get("slug"), str):
                    ensure(b["slug"].startswith(b["date"] + "-"), f"{prefix}.slug should start with date", errors)
        for k in ("title", "summary"):
            ensure(isinstance(b.get(k), str) and b[k].strip(), f"{prefix}.{k} must be non-empty string", errors)
        ensure(isinstance(b.get("tags"), list) and len(b["tags"]) > 0, f"{prefix}.tags must be non-empty list", errors)
        if isinstance(b.get("tags"), list):
            for t in b["tags"]:
                ensure(isinstance(t, str) and t.strip(), f"{prefix}.tags values must be non-empty strings", errors)

        if isinstance(b.get("slug"), str):
            brief_path = ROOT / "docs" / "briefs" / f"{b['slug']}.html"
            ensure(brief_path.exists(), f"{prefix} missing brief file: docs/briefs/{b['slug']}.html", errors)

    # Guard publish cadence: no duplicate dates unless intentionally changed later.
    ensure(len(dates) == len(briefs), "dates should be unique per brief", errors)

    sitemap_static = data["sitemap_static"]
    ensure(isinstance(sitemap_static, list) and len(sitemap_static) > 0, "sitemap_static must be non-empty list", errors)
    for i, s in enumerate(sitemap_static):
        prefix = f"sitemap_static[{i}]"
        ensure(isinstance(s, dict), f"{prefix} must be object", errors)
        if not isinstance(s, dict):
            continue
        for k in ("path", "changefreq", "priority"):
            ensure(k in s, f"{prefix} missing key: {k}", errors)
            ensure(isinstance(s.get(k), str), f"{prefix}.{k} must be string", errors)
        if isinstance(s.get("path"), str):
            # Root path is intentionally empty string.
            ensure(s["path"] == "" or bool(s["path"].strip()), f"{prefix}.path must be empty or non-empty string", errors)
        for k in ("changefreq", "priority"):
            if isinstance(s.get(k), str):
                ensure(bool(s[k].strip()), f"{prefix}.{k} must be non-empty string", errors)

    if errors:
        print("check_manifest: invalid\n")
        for e in errors:
            print(e)
        return 1

    print(f"check_manifest: ok ({len(briefs)} briefs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

