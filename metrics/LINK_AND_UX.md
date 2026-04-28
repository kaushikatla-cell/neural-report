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
