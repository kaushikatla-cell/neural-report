#!/usr/bin/env python3
"""
Generate docs/library.html from research/paper_library.csv.
"""
from __future__ import annotations

import csv
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://kaushikatla-cell.github.io/neural-report"


def load_rows() -> list[dict]:
    path = ROOT / "research" / "paper_library.csv"
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return sorted(rows, key=lambda r: (r.get("year", ""), r.get("title", "")), reverse=True)


def render() -> str:
    rows = load_rows()
    domains = sorted({(r.get("domain") or "").strip().lower() for r in rows if (r.get("domain") or "").strip()})
    counts = Counter((r.get("domain") or "other").strip().lower() for r in rows)

    chips = []
    for d in domains:
        chips.append(f'<button class="chip" type="button" data-library-domain="{escape(d)}">{escape(d)} ({counts[d]})</button>')

    cards = []
    for r in rows:
        domain = (r.get("domain") or "").strip().lower()
        title = r.get("title") or ""
        year = r.get("year") or ""
        src = r.get("source_type") or ""
        url = r.get("url") or "#"
        why = r.get("why_it_matters") or ""
        finding = r.get("key_finding") or ""
        cards.append(
            "\n".join(
                [
                    f'<article class="paper-card" data-domain="{escape(domain)}" data-title="{escape(title.lower())}" data-year="{escape(year)}">',
                    f"  <h3>{escape(title)}</h3>",
                    f'  <p class="paper-meta"><span>{escape(year)}</span> · <span>{escape(domain)}</span> · <span>{escape(src)}</span></p>',
                    f'  <p><strong>Why this matters:</strong> {escape(why)}</p>',
                    f'  <p><strong>Key finding:</strong> {escape(finding)}</p>',
                    f'  <p><a href="{escape(url)}">Open source</a></p>',
                    "</article>",
                ]
            )
        )

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Research Library — Neural Report</title>
    <meta name="description" content="Curated paper and policy library for AI, labor, macro, energy, and governance evidence work." />
    <link rel="canonical" href="{BASE}/library.html" />
    <link rel="alternate" type="application/rss+xml" title="Neural Report — Evidence Briefs" href="rss.xml" />
    <link rel="alternate" type="application/atom+xml" title="Neural Report — Evidence Briefs" href="atom.xml" />
    <meta property="og:site_name" content="Neural Report" />
    <meta property="og:title" content="Research Library — Neural Report" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{BASE}/library.html" />
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
          <a href="library.html" aria-current="page">Library</a>
          <a href="faq.html">FAQ</a>
          <a href="glossary.html">Glossary</a>
          <a href="dashboard.html">Dashboard</a>
          <a href="subscribe.html">Subscribe</a>
        </div>
      </nav>
    </header>
    <main id="main-content">
      <h1>Research library</h1>
      <p class="lead">
        High-signal papers and policy docs used in NRP Evidence Briefs. This is an operating library, not a vanity reading list.
      </p>
      <div class="card compact">
        <h3>Filter the library</h3>
        <div class="controls-row">
          <label for="library-search">Search title or findings</label>
          <input id="library-search" type="search" placeholder="e.g. productivity, electricity, monetary policy" autocomplete="off" />
        </div>
        <div class="chip-row">
          <button class="chip is-active" type="button" data-library-domain="">all ({len(rows)})</button>
          {''.join(chips)}
        </div>
        <p id="library-summary" class="muted" style="margin-bottom:0">Showing all sources.</p>
      </div>
      <section id="library-grid" class="paper-grid">
        {''.join(cards)}
      </section>
    </main>
    <footer><a href="index.html">Home</a> · <a href="methodology.html">Methodology</a></footer>
    <script src="js/nrp-core.js" defer></script>
  </body>
</html>
"""


def main() -> int:
    out = ROOT / "docs" / "library.html"
    out.write_text(render(), encoding="utf-8")
    print("wrote docs/library.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

