#!/usr/bin/env python3
"""
Generate docs/dashboard.html from manifest + metrics + link-audit outputs.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://kaushikatla-cell.github.io/neural-report"


def load_manifest() -> dict:
    return json.loads((ROOT / "scripts" / "site-manifest.json").read_text(encoding="utf-8"))


def load_monthly_rows() -> list[dict]:
    path = ROOT / "metrics" / "monthly-dashboard.csv"
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_link_audit() -> dict:
    path = ROOT / "metrics" / "link-audit" / "latest.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"timestamp": "n/a", "summary": {"total": 0, "ok": 0, "failed": 0, "new_failures": 0}}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render() -> str:
    m = load_manifest()
    briefs = sorted(m["briefs"], key=lambda b: b["date"], reverse=True)
    monthly = load_monthly_rows()
    latest_month = monthly[-1] if monthly else {}
    audit = load_link_audit()
    summary = audit.get("summary", {})

    latest_briefs_html = []
    for b in briefs[:5]:
        latest_briefs_html.append(
            f'<li><a href="briefs/{esc(b["slug"])}.html"><strong>{esc(b["title"])}</strong></a> — {esc(b["summary"])}</li>'
        )

    monthly_rows = []
    for r in monthly[-6:]:
        monthly_rows.append(
            "<tr>"
            f"<td>{esc(r.get('month', ''))}</td>"
            f"<td>{esc(r.get('briefs_published_this_month', ''))}</td>"
            f"<td>{esc(r.get('newsletter_subs_end_of_month', ''))}</td>"
            f"<td>{esc(r.get('bio_link_clicks_30d', ''))}</td>"
            f"<td>{esc(r.get('external_validations_cumulative', ''))}</td>"
            "</tr>"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Dashboard — Neural Report</title>
    <meta name="description" content="Public operating dashboard for Neural Report: publishing cadence, validation progress, and link-health status." />
    <link rel="canonical" href="{BASE}/dashboard.html" />
    <link rel="alternate" type="application/rss+xml" title="Neural Report — Evidence Briefs" href="rss.xml" />
    <link rel="alternate" type="application/atom+xml" title="Neural Report — Evidence Briefs" href="atom.xml" />
    <meta property="og:site_name" content="Neural Report" />
    <meta property="og:title" content="Dashboard — Neural Report" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{BASE}/dashboard.html" />
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
          <a href="dashboard.html" aria-current="page">Dashboard</a>
          <a href="transparency.html">Transparency</a>
          <a href="methodology.html">Methodology</a>
          <a href="subscribe.html">Subscribe</a>
        </div>
      </nav>
    </header>
    <main id="main-content">
      <h1>Public dashboard</h1>
      <p class="lead">Operating signals for NRP: shipping cadence, audience growth, external validation, and link reliability.</p>

      <div class="card trust-card">
        <h3>Current snapshot</h3>
        <ul class="tight">
          <li><strong>Total briefs:</strong> {len(briefs)}</li>
          <li><strong>Latest publish date:</strong> {esc(briefs[0]['date'] if briefs else "n/a")}</li>
          <li><strong>Last metrics month:</strong> {esc(latest_month.get('month', 'n/a'))}</li>
          <li><strong>External validations (cumulative):</strong> {esc(latest_month.get('external_validations_cumulative', 'n/a'))}</li>
          <li><strong>Link audit:</strong> {summary.get('ok', 0)}/{summary.get('total', 0)} ok · failed {summary.get('failed', 0)} · new failures {summary.get('new_failures', 0)}</li>
        </ul>
        <p style="margin-bottom:0">
          <a href="https://github.com/kaushikatla-cell/neural-report/tree/main/metrics/link-audit">View raw link-audit artifacts</a>
          · Last run: <code>{esc(audit.get('timestamp', 'n/a'))}</code>
        </p>
      </div>

      <h2>Latest briefs</h2>
      <ul class="tight">
        {''.join(latest_briefs_html)}
      </ul>

      <h2>Monthly KPI table (last 6 rows)</h2>
      <table>
        <thead>
          <tr>
            <th>Month</th>
            <th>Briefs this month</th>
            <th>Newsletter subs (EOM)</th>
            <th>Bio link clicks (30d)</th>
            <th>External validations (cum.)</th>
          </tr>
        </thead>
        <tbody>
          {''.join(monthly_rows)}
        </tbody>
      </table>
      <p>
        Source files: <code>metrics/monthly-dashboard.csv</code>,
        <code>metrics/link-audit/latest.json</code>, <code>scripts/site-manifest.json</code>,
        <code>research/paper_library.csv</code>.
      </p>
      <p>
        Supporting resources:
        <a href="library.html">Research library</a> ·
        <a href="faq.html">FAQ</a> ·
        <a href="glossary.html">Glossary</a> ·
        <a href="series.html">Series roadmap</a>
      </p>
    </main>
    <footer><a href="index.html">Home</a> · <a href="transparency.html">Transparency notes</a></footer>
    <script src="js/nrp-core.js" defer></script>
  </body>
</html>
"""


def main() -> int:
    out = ROOT / "docs" / "dashboard.html"
    out.write_text(render(), encoding="utf-8")
    print("wrote docs/dashboard.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

