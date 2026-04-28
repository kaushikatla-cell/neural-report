# Contributing to Neural Report

NRP is a **co-founder–led** desk. External PRs are welcome for typos, broken links, and accessibility; substantive claims should be discussed first (open an issue).

## Before you open a PR

From the repo root:

```bash
bash scripts/publish-check.sh
```

(or `make publish-check` if you use Make). That runs **`generate_feeds.py`** then **`check_docs.py`** so RSS/sitemap match [`scripts/site-manifest.json`](scripts/site-manifest.json) and relative links resolve.

Commit any updated **`docs/rss.xml`** / **`docs/sitemap.xml`** after editing the manifest.

## Publishing a new Evidence Brief

1. (Optional) Open a **Ship Evidence Brief** issue from [`.github/ISSUE_TEMPLATE/evidence-brief.md`](.github/ISSUE_TEMPLATE/evidence-brief.md).

2. Draft using [`templates/evidence-brief-template.md`](templates/evidence-brief-template.md) and complete the checklist.

3. Add an object to [`scripts/site-manifest.json`](scripts/site-manifest.json): **`slug`** must equal the HTML filename **without** `.html` (e.g. slug `2026-06-01-ai-topic` → file `docs/briefs/2026-06-01-ai-topic.html`).

4. Add `docs/briefs/YYYY-MM-DD-slug.html` — copy [`docs/briefs/_template.html`](docs/briefs/_template.html), set `title`, `description`, canonical URL, and byline. The template includes **og:image**; the default share image is [`docs/images/og-default.png`](docs/images/og-default.png). If you **replace** that file and its pixel size changes, update every page’s `og:image:width` / `og:image:height` (see [`metrics/LINK_AND_UX.md`](metrics/LINK_AND_UX.md)).

5. **`python3 scripts/generate_feeds.py`** — refreshes [`docs/rss.xml`](docs/rss.xml) and [`docs/sitemap.xml`](docs/sitemap.xml). **Do not** hand-edit those two files.

6. Update [`docs/archive.html`](docs/archive.html) and the “Latest” section on [`docs/index.html`](docs/index.html) if this is a new public ship.

7. **`python3 scripts/check_docs.py`** (included in `publish-check.sh`). CI also runs **feeds validate** + **docs check** on `main`.

8. Open a PR. **Divyam Gupta** (editorial) or a delegate merges after fact-check (**Kaushik Atla** lane).

## House style

- Cite primary sources where possible; label uncertainty.
- No personalized investment advice; no undisclosed conflicts.
- Material corrections go to [`docs/corrections.html`](docs/corrections.html) and the affected brief.

## More

- Optional **external URL** scan: [lychee](https://github.com/lycheeverse/lychee) + [`lychee.toml`](lychee.toml) — see [`scripts/README.md`](scripts/README.md) and [`metrics/LINK_AND_UX.md`](metrics/LINK_AND_UX.md).
