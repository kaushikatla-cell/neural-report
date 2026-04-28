---
name: Ship Evidence Brief
about: Checklist for publishing a new NRP Evidence Brief
title: "Brief: YYYY-MM-DD — "
labels: brief
---

## Topic

- **Question (headline):**

## Pre-publish

- [ ] Draft completed using `templates/evidence-brief-template.md`
- [ ] Fact-check pass (Kaushik lane) + editorial pass (Divyam lane)
- [ ] **`scripts/site-manifest.json`** — new `{ slug, title, date, summary }` (slug = filename without `.html`)
- [ ] `docs/briefs/YYYY-MM-DD-slug.html` added (from `docs/briefs/_template.html`); meta + `og:*` filled
- [ ] `bash scripts/publish-check.sh` (or `generate_feeds.py` + `sync_site_pages.py` + `generate_og_images.py` + `check_docs.py` + `check_briefs.py`) — commit generated feeds/pages/images/meta if changed
- [ ] `docs/archive.html` and `docs/index.html` updated by `sync_site_pages.py` (verify output)
- [ ] IG teaser scheduled (Shivam lane) with UTM link

## Post-publish

- [ ] `metrics/monthly-dashboard.csv` end-of-month row (batch OK)
- [ ] `CONTRIBUTION_LOG.md` updated (who shipped what)
