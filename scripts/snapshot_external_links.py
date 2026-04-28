#!/usr/bin/env python3
"""
Snapshot external link health from docs/*.html and report deltas over time.

Outputs:
- metrics/link-audit/latest.json
- metrics/link-audit/latest-delta.md
- metrics/link-audit/snapshots/<timestamp>.json
"""
from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
AUDIT_DIR = ROOT / "metrics" / "link-audit"
SNAP_DIR = AUDIT_DIR / "snapshots"

HREF_RE = re.compile(r"""href\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
SKIP_PREFIXES = ("mailto:", "tel:", "javascript:", "data:")
UA = "Mozilla/5.0 (compatible; NeuralReportLinkAudit/1.0; +https://kaushikatla-cell.github.io/neural-report/)"


def extract_external_urls() -> list[str]:
    urls: OrderedDict[str, None] = OrderedDict()
    for path in sorted(DOCS.rglob("*.html")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in HREF_RE.finditer(text):
            href = m.group(1).strip()
            if not href or href.startswith("#") or href.startswith(SKIP_PREFIXES):
                continue
            if href.startswith("http://") or href.startswith("https://"):
                host = urlparse(href).hostname or ""
                if "kaushikatla-cell.github.io" in host:
                    continue
                urls[href] = None
    return list(urls.keys())


def check_url(url: str, timeout: float = 12.0) -> dict:
    headers = {"User-Agent": UA}
    # HEAD first, fallback GET for servers that block HEAD.
    for method in ("HEAD", "GET"):
        try:
            resp = requests.request(
                method,
                url,
                headers=headers,
                timeout=timeout,
                allow_redirects=True,
            )
            code = int(resp.status_code)
            return {"status_code": code, "ok": (200 <= code < 400) or code == 429, "error": "", "method": method}
        except requests.RequestException as e:
            if method == "GET":
                return {"status_code": 0, "ok": False, "error": str(e), "method": method}
    return {"status_code": 0, "ok": False, "error": "unknown error", "method": "GET"}


def load_previous_latest() -> dict | None:
    latest = AUDIT_DIR / "latest.json"
    if latest.exists():
        return json.loads(latest.read_text(encoding="utf-8"))
    return None


def write_delta_markdown(current: dict, previous: dict | None) -> None:
    cur_bad = {r["url"]: r for r in current["results"] if not r["ok"]}
    prev_bad = {}
    if previous:
        prev_bad = {r["url"]: r for r in previous.get("results", []) if not r.get("ok", False)}

    new_failures = sorted(set(cur_bad) - set(prev_bad))
    resolved = sorted(set(prev_bad) - set(cur_bad))

    lines = [
        "# External link audit delta",
        "",
        f"- Timestamp: `{current['timestamp']}`",
        f"- Total URLs checked: **{current['summary']['total']}**",
        f"- Failures now: **{current['summary']['failed']}**",
    ]
    if previous:
        lines.append(f"- Previous failures: **{previous.get('summary', {}).get('failed', 0)}**")
    else:
        lines.append("- Previous snapshot: **none**")
    lines.append("")

    lines.append("## New failures")
    if not new_failures:
        lines.append("- None")
    else:
        for u in new_failures:
            r = cur_bad[u]
            lines.append(f"- `{u}` -> `{r['status_code']}` {r['error']}".rstrip())
    lines.append("")

    lines.append("## Resolved since previous snapshot")
    if not resolved:
        lines.append("- None")
    else:
        for u in resolved:
            lines.append(f"- `{u}`")
    lines.append("")

    (AUDIT_DIR / "latest-delta.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="return non-zero when failures > 0")
    args = parser.parse_args()

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    SNAP_DIR.mkdir(parents=True, exist_ok=True)

    urls = extract_external_urls()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    results = []
    for url in urls:
        r = check_url(url)
        r["url"] = url
        results.append(r)

    summary = {
        "total": len(results),
        "ok": sum(1 for r in results if r["ok"]),
        "failed": sum(1 for r in results if not r["ok"]),
    }
    payload = {"timestamp": timestamp, "summary": summary, "results": results}

    previous = load_previous_latest()
    (AUDIT_DIR / "latest.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    snap_name = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + ".json"
    (SNAP_DIR / snap_name).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_delta_markdown(payload, previous)

    print(
        f"snapshot_external_links: total={summary['total']} ok={summary['ok']} failed={summary['failed']} "
        f"(wrote metrics/link-audit/latest.json, latest-delta.md, snapshots/{snap_name})"
    )

    if args.strict and summary["failed"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

