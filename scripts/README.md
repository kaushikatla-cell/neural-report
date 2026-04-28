# Scripts

| File | Purpose |
|------|---------|
| [`site-manifest.json`](site-manifest.json) | **Source of truth** for published briefs (title, date, summary, slug). |
| [`generate_feeds.py`](generate_feeds.py) | Writes `docs/rss.xml` (RSS 2.0), `docs/atom.xml` (Atom), and `docs/sitemap.xml` from the manifest. Run after every manifest change. |
| [`sync_site_pages.py`](sync_site_pages.py) | Rebuilds `docs/index.html` (Latest list) and `docs/archive.html` (table rows) from the manifest. |
| [`generate_og_images.py`](generate_og_images.py) | Renders **1200×630** PNGs: `docs/images/og/{slug}.png` + `docs/images/og-default.png`; syncs brief OG/Twitter/JSON-LD image URLs. Requires Pillow (`requirements.txt`). |
| [`rewrite_site_base.py`](rewrite_site_base.py) | Replace GitHub Pages base URL with a custom domain (or reverse) across `docs/` + key config files. |
| [`check_docs.py`](check_docs.py) | Verifies relative `href`s in `docs/` point to real files (no network). |
| [`check_briefs.py`](check_briefs.py) | Editorial QA: required sections, min source links, and methodology/corrections links in every brief. |

```bash
# from repository root (recommended before every PR)
bash scripts/publish-check.sh
# or: make publish-check

python3 scripts/generate_feeds.py
python3 scripts/sync_site_pages.py
python3 scripts/generate_og_images.py
python3 scripts/check_docs.py
python3 scripts/check_briefs.py
```

**External link check** (advisory in CI; may false-fail on throttling): [lychee](https://github.com/lycheeverse/lychee) with [lychee.toml](../lychee.toml).

```bash
# if lychee is installed: lychee --config lychee.toml './docs/**/*.html'
```
