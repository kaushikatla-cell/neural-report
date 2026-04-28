#!/usr/bin/env python3
"""
Bootstrap a new evidence brief:
- creates docs/briefs/YYYY-MM-DD-slug.html from template
- appends entry to scripts/site-manifest.json
- optionally runs downstream generators/checks

Example:
  python3 scripts/bootstrap_brief.py \
    --date 2026-06-01 \
    --slug ai-adoption-and-wages \
    --title "Has AI adoption raised wages yet?" \
    --summary "Early labor-market evidence on AI adoption and wages." \
    --tags "AI,labor,wages,measurement" \
    --run-all
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "docs" / "briefs" / "_template.html"
MANIFEST = ROOT / "scripts" / "site-manifest.json"
BASE = "https://kaushikatla-cell.github.io/neural-report"


def slugify(raw: str) -> str:
    s = raw.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s


def make_brief_html(date: str, full_slug: str, title: str, summary: str) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    canonical = f"{BASE}/briefs/{full_slug}.html"
    og_image = f"{BASE}/images/og/{full_slug}.png"
    replacements = {
        "YYYY-MM-DD-slug": full_slug,
        "[Title]": title,
        "[One-line summary for search + social]": summary,
        "[One-line summary]": summary,
        "[Title — match og:title]": title,
        "[Headline question]": title,
        "[YYYY-MM-DD]": date,
        "Read time\n          ~[n] min": "Read time ~6 min",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Ensure canonical and image URLs are precise.
    text = text.replace(f"{BASE}/briefs/{full_slug}.html", canonical)
    text = text.replace(f"{BASE}/images/og/{full_slug}.png", og_image)
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--slug", required=True, help="slug without date prefix")
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--tags", required=True, help="comma-separated tags")
    parser.add_argument("--run-all", action="store_true", help="run publish-check after creation")
    args = parser.parse_args()

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", args.date):
        raise SystemExit("--date must be YYYY-MM-DD")
    core_slug = slugify(args.slug)
    full_slug = f"{args.date}-{core_slug}"
    brief_path = ROOT / "docs" / "briefs" / f"{full_slug}.html"
    if brief_path.exists():
        raise SystemExit(f"brief already exists: {brief_path}")

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    if not tags:
        raise SystemExit("--tags must contain at least one non-empty tag")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for b in manifest["briefs"]:
        if b["slug"] == full_slug:
            raise SystemExit(f"manifest already has slug: {full_slug}")

    brief_path.write_text(make_brief_html(args.date, full_slug, args.title, args.summary), encoding="utf-8")

    manifest["briefs"].append(
        {
            "slug": full_slug,
            "title": args.title,
            "date": args.date,
            "summary": args.summary,
            "tags": tags,
        }
    )
    # Keep newest first for easier review.
    manifest["briefs"] = sorted(manifest["briefs"], key=lambda b: b["date"], reverse=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"created {brief_path.relative_to(ROOT)}")
    print("updated scripts/site-manifest.json")

    if args.run_all:
        subprocess.run(["bash", "scripts/publish-check.sh"], cwd=ROOT, check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

