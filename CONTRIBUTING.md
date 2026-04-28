# Contributing to Neural Report

NRP is a **co-founder–led** desk. External PRs are welcome for typos, broken links, and accessibility; substantive claims should be discussed first (open an issue).

## Before you open a PR

From the repo root:

```bash
bash scripts/publish-check.sh
```

(or `make publish-check` if you use Make). Requires **Pillow**: `python3 -m pip install -r requirements.txt` once per machine.

That runs **`generate_feeds.py`**, **`generate_og_images.py`** (brief cards + `docs/images/og-default.png`, syncs brief `og:image` tags), then **`check_docs.py`** so feeds match [`scripts/site-manifest.json`](scripts/site-manifest.json) and relative links resolve.

Commit updated **`docs/rss.xml`**, **`docs/atom.xml`**, **`docs/sitemap.xml`**, **`docs/images/og/*.png`**, **`docs/images/og-default.png`**, and any **`docs/briefs/*.html`** OG meta changes after editing the manifest.

## Publishing a new Evidence Brief

1. (Optional) Open a **Ship Evidence Brief** issue from [`.github/ISSUE_TEMPLATE/evidence-brief.md`](.github/ISSUE_TEMPLATE/evidence-brief.md).

2. Draft using [`templates/evidence-brief-template.md`](templates/evidence-brief-template.md) and complete the checklist.

3. Add an object to [`scripts/site-manifest.json`](scripts/site-manifest.json): **`slug`** must equal the HTML filename **without** `.html` (e.g. slug `2026-06-01-ai-topic` → file `docs/briefs/2026-06-01-ai-topic.html`).

4. Add `docs/briefs/YYYY-MM-DD-slug.html` — copy [`docs/briefs/_template.html`](docs/briefs/_template.html), set `title`, `description`, canonical URL, byline, and **slug** in `images/og/…` placeholders. **Social preview PNGs** (1200×630) for each brief are generated in step 6 from the manifest—non-brief pages still use [`docs/images/og-default.png`](docs/images/og-default.png).

5. **`python3 scripts/generate_feeds.py`** — refreshes [`docs/rss.xml`](docs/rss.xml), [`docs/atom.xml`](docs/atom.xml), and [`docs/sitemap.xml`](docs/sitemap.xml). **Do not** hand-edit those three files.

6. **`python3 scripts/generate_og_images.py`** — writes `docs/images/og/{slug}.png` and syncs per-brief Open Graph / Twitter / JSON-LD image URLs. **Do not** hand-edit generated PNGs.

7. Update [`docs/archive.html`](docs/archive.html) and the “Latest” section on [`docs/index.html`](docs/index.html) if this is a new public ship.

8. **`python3 scripts/check_docs.py`** (included in `publish-check.sh`). CI runs **site-outputs validate** + **docs check** on `main`.

9. **Custom domain:** run `python3 scripts/rewrite_site_base.py 'OLD_BASE' 'NEW_BASE'`, then re-run steps 5–6 and review the diff.

10. Open a PR. **Divyam Gupta** (editorial) or a delegate merges after fact-check (**Kaushik Atla** lane).

## House style

- Cite primary sources where possible; label uncertainty.
- No personalized investment advice; no undisclosed conflicts.
- Material corrections go to [`docs/corrections.html`](docs/corrections.html) and the affected brief.

## More

- Optional **external URL** scan: [lychee](https://github.com/lycheeverse/lychee) + [`lychee.toml`](lychee.toml) — see [`scripts/README.md`](scripts/README.md) and [`metrics/LINK_AND_UX.md`](metrics/LINK_AND_UX.md).
