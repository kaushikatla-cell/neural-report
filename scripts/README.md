# Scripts

| File | Purpose |
|------|---------|
| [`site-manifest.json`](site-manifest.json) | **Source of truth** for published briefs (title, date, summary, slug). |
| [`generate_feeds.py`](generate_feeds.py) | Writes `docs/rss.xml` (RSS 2.0), `docs/atom.xml` (Atom), and `docs/sitemap.xml` from the manifest. Run after every manifest change. |
| [`check_docs.py`](check_docs.py) | Verifies relative `href`s in `docs/` point to real files (no network). |

```bash
# from repository root (recommended before every PR)
bash scripts/publish-check.sh
# or: make publish-check

python3 scripts/generate_feeds.py
python3 scripts/check_docs.py
```

**External link check** (advisory in CI; may false-fail on throttling): [lychee](https://github.com/lycheeverse/lychee) with [lychee.toml](../lychee.toml).

```bash
# if lychee is installed: lychee --config lychee.toml './docs/**/*.html'
```
