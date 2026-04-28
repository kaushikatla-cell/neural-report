#!/usr/bin/env python3
"""
Generate docs/transparency.html from metrics/transparency/*.md notes.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://kaushikatla-cell.github.io/neural-report"
NOTES_DIR = ROOT / "metrics" / "transparency"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def parse_title(text: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def parse_summary(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s and not s.startswith("#") and not s.startswith("-"):
            return s
    return "Monthly operating transparency note."


def render() -> str:
    entries = []
    if NOTES_DIR.exists():
        for p in sorted(NOTES_DIR.glob("*.md"), reverse=True):
            if p.name.upper() == "TEMPLATE.md":
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            title = parse_title(text, p.stem)
            summary = parse_summary(text)
            entries.append((p.name, title, summary))

    rows = []
    for fname, title, summary in entries:
        gh = f"https://github.com/kaushikatla-cell/neural-report/blob/main/metrics/transparency/{fname}"
        rows.append(
            f'<li><a href="{gh}"><strong>{esc(title)}</strong></a> — {esc(summary)}</li>'
        )
    rows_html = "\n".join(rows) if rows else "<li>No notes yet.</li>"

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Transparency — Neural Report</title>
    <meta name="description" content="Monthly transparency notes: what shipped, what changed, what was corrected, and what is next." />
    <link rel="canonical" href="{BASE}/transparency.html" />
    <link rel="alternate" type="application/rss+xml" title="Neural Report — Evidence Briefs" href="rss.xml" />
    <link rel="alternate" type="application/atom+xml" title="Neural Report — Evidence Briefs" href="atom.xml" />
    <meta property="og:site_name" content="Neural Report" />
    <meta property="og:title" content="Transparency — Neural Report" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{BASE}/transparency.html" />
    <meta property="og:image" content="{BASE}/images/og-default.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:image" content="{BASE}/images/og-default.png" />
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header>
      <nav class="nav" aria-label="Primary">
        <a class="brand" href="index.html">NEURAL REPORT</a>
        <div class="nav-links">
          <a href="index.html">Home</a>
          <a href="archive.html">Archive</a>
          <a href="library.html">Library</a>
          <a href="faq.html">FAQ</a>
          <a href="dashboard.html">Dashboard</a>
          <a href="transparency.html" aria-current="page">Transparency</a>
          <a href="methodology.html">Methodology</a>
          <a href="subscribe.html">Subscribe</a>
        </div>
      </nav>
    </header>
    <main id="main-content">
      <h1>Transparency notes</h1>
      <p class="lead">
        Monthly operational notes: what we shipped, where we were uncertain, what we corrected, and what we will improve next.
      </p>

      <div class="card">
        <h3>Why this exists</h3>
        <ul class="tight">
          <li>Separate <strong>performance reporting</strong> from content itself.</li>
          <li>Document <strong>wins, misses, and corrections</strong> with timestamps.</li>
          <li>Keep a public trail of <strong>process quality</strong> improvements.</li>
        </ul>
      </div>

      <h2>Monthly notes</h2>
      <ul class="tight">
        {rows_html}
      </ul>
      <p>
        Also see:
        <a href="dashboard.html">Dashboard</a> ·
        <a href="library.html">Research library</a> ·
        <a href="series.html">Series roadmap</a>.
      </p>
    </main>
    <footer><a href="index.html">Home</a> · <a href="dashboard.html">Dashboard</a></footer>
    <script src="js/nrp-core.js" defer></script>
  </body>
</html>
"""


def main() -> int:
    out = ROOT / "docs" / "transparency.html"
    out.write_text(render(), encoding="utf-8")
    print("wrote docs/transparency.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

