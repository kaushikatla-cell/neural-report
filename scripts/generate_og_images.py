#!/usr/bin/env python3
"""
Generate social preview PNGs (1200×630) from scripts/site-manifest.json.

Writes:
  - docs/images/og/{slug}.png for each brief
  - docs/images/og-default.png (site-wide default)

Updates og/twitter + Article JSON-LD image (not publisher.logo) in docs/briefs/*.html.

Run from repo root: pip install -r requirements.txt && python3 scripts/generate_og_images.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAD = 56
ACCENT = (125, 211, 252)
BG = (15, 17, 21)
TEXT = (232, 234, 239)
MUTED = (180, 188, 200)


def load_manifest(root: Path) -> dict:
    with open(root / "scripts" / "site-manifest.json", encoding="utf-8") as f:
        return json.load(f)


def pick_font(size: int, bold: bool) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
    else:
        candidates += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap_lines(text: str, draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.replace("\n", " ").split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if draw.textlength(trial, font=font) <= max_width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines[:6]  # cap for card layout


def render_card(
    title: str,
    subtitle: str,
    out_path: Path,
) -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 6, H), fill=ACCENT)

    title_font = pick_font(44, bold=True)
    sub_font = pick_font(24, bold=False)
    max_w = W - 2 * PAD
    lines = wrap_lines(title, draw, title_font, max_w)
    y = PAD + 20
    lh = int(title_font.getbbox("Ay")[3] - title_font.getbbox("Ay")[1]) + 8
    for line in lines:
        draw.text((PAD, y), line, fill=TEXT, font=title_font)
        y += lh

    y = max(y + 24, H - PAD - 72)
    draw.text((PAD, y), subtitle, fill=MUTED, font=sub_font)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG", optimize=True, compress_level=9)


def sync_brief_html(root: Path, base: str, slug: str) -> None:
    path = root / "docs" / "briefs" / f"{slug}.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    card_url = f"{base.rstrip('/')}/images/og/{slug}.png"

    def repl_og(m: re.Match[str]) -> str:
        return f'{m.group(1)}{card_url}{m.group(3)}'

    text = re.sub(
        r'(<meta property="og:image" content=")([^"]+)(" />)',
        repl_og,
        text,
        count=1,
    )
    text = re.sub(
        r'(<meta name="twitter:image" content=")([^"]+)(" />)',
        repl_og,
        text,
        count=1,
    )
    text = re.sub(
        r'(<meta property="og:image:width" content=")(\d+)(" />)',
        r"\g<1>1200\g<3>",
        text,
        count=1,
    )
    text = re.sub(
        r'(<meta property="og:image:height" content=")(\d+)(" />)',
        r"\g<1>630\g<3>",
        text,
        count=1,
    )
    # Article "image" array (first URL only) — keep publisher.logo on og-default
    text = re.sub(
        r'("image": \[\s*")[^"]+("\s*\])',
        rf'\1{card_url}\2',
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8")


def sync_static_pages_dimensions(root: Path) -> None:
    """Set og:image width/height to 1200×630 on pages still using og-default."""
    for rel in [
        "docs/index.html",
        "docs/about.html",
        "docs/archive.html",
        "docs/methodology.html",
        "docs/corrections.html",
        "docs/subscribe.html",
    ]:
        p = root / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        t = re.sub(
            r'(<meta property="og:image:width" content=")(\d+)(" />)',
            r"\g<1>1200\g<3>",
            t,
        )
        t = re.sub(
            r'(<meta property="og:image:height" content=")(\d+)(" />)',
            r"\g<1>630\g<3>",
            t,
        )
        p.write_text(t, encoding="utf-8")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    m = load_manifest(root)
    base = m["base_url"].rstrip("/")

    out_dir = root / "docs" / "images" / "og"
    for b in m["briefs"]:
        slug = b["slug"]
        title = b["title"]
        subtitle = f"NRP Evidence Brief · {b['date']}"
        render_card(title, subtitle, out_dir / f"{slug}.png")
        sync_brief_html(root, base, slug)

    render_card(
        "Neural Report",
        "Evidence Briefs · AI, economics & policy",
        root / "docs" / "images" / "og-default.png",
    )
    sync_static_pages_dimensions(root)

    print(f"wrote {len(m['briefs'])} brief cards + docs/images/og-default.png (1200×630)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
