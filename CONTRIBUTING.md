# Contributing to Neural Report

NRP is a **co-founder–led** desk. External PRs are welcome for typos, broken links, and accessibility; substantive claims should be discussed first (open an issue).

## Publishing a new Evidence Brief

1. (Optional) Open a **Ship Evidence Brief** issue from [`.github/ISSUE_TEMPLATE/evidence-brief.md`](.github/ISSUE_TEMPLATE/evidence-brief.md).
2. Draft using [`templates/evidence-brief-template.md`](templates/evidence-brief-template.md) and complete the checklist.
3. Add a new object to [`scripts/site-manifest.json`](scripts/site-manifest.json) for the brief (title, date, summary, `slug` without `.html`).
4. Add `docs/briefs/YYYY-MM-DD-slug.html` (copy [`docs/briefs/_template.html`](docs/briefs/_template.html) and fill meta + byline).
5. Regenerate feeds: `python3 scripts/generate_feeds.py` (updates [`docs/rss.xml`](docs/rss.xml) and [`docs/sitemap.xml`](docs/sitemap.xml) from the manifest; **do not** hand-edit those two files).
6. Update [`docs/archive.html`](docs/archive.html) and the “Latest” section on [`docs/index.html`](docs/index.html) if appropriate.
7. Run `python3 scripts/check_docs.py` from the repo root. **Feeds validate** + **docs check** also run in GitHub Actions.
8. Open a PR; **Divyam Gupta** (editorial lead) or a delegate approves merge after fact-check (**Kaushik Atla** lane).

## House style

- Cite primary sources where possible; label uncertainty.
- No personalized investment advice; no undisclosed conflicts.
- Material corrections go to [`docs/corrections.html`](docs/corrections.html) and the affected brief.
