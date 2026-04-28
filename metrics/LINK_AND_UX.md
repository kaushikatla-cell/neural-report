# Link checking and UX notes

## Internal links

- `python3 scripts/check_docs.py` — no network; required before PR.
- **CI:** [`.github/workflows/docs-check.yml`](../.github/workflows/docs-check.yml).

## External links (advisory)

- **Lychee** in [`.github/workflows/external-links.yml`](../.github/workflows/external-links.yml) runs on a **weekly** schedule and on `docs/**` / `lychee.toml` changes. The job is `continue-on-error: true` because some government and academic hosts block or throttle GitHub Actions IP ranges.
- To run locally: install [lychee](https://github.com/lycheeverse/lychee) and run `lychee --config lychee.toml './docs/**/*.html'`.
- Edit [lychee.toml](../lychee.toml) to add excludes for false positives.

## Open Graph / share image

- Default card: `https://kaushikatla-cell.github.io/neural-report/images/og-default.png` (set in `og:image` / `twitter:image` on each page). Dimensions in meta tags match the file on disk (currently **1536×1024**; replace the asset and update all `og:image:width` / `og:image:height` values if you change size).

## Accessibility (Lighthouse-style)

- Muted text color lightened in CSS for contrast; nav links and brand use **min-height 44px** touch targets; form controls use min-height 44px.
- `prefers-reduced-motion: reduce` trims animation/transition duration; `color-scheme: dark` improves native controls in dark UI.

## Syndication (RSS + Atom)

- **`docs/rss.xml`** — RSS 2.0 with `atom:link` self reference (for readers that expect classic RSS).
- **`docs/atom.xml`** — Atom 1.0 (preferred by some aggregators and tooling).
- Both are generated only from **`scripts/site-manifest.json`** via `scripts/generate_feeds.py`; CI fails on drift.

## Discovery for AI tools

- **`docs/llms.txt`** — short usage note + links to methodology and feeds (optional convention for model-facing context).
- **`docs/.well-known/security.txt`** — security contact per [securitytxt.org](https://securitytxt.org/).
