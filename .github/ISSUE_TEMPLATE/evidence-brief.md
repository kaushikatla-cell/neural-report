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
- [ ] `python3 scripts/generate_feeds.py` run (or `bash scripts/publish-check.sh`)
- [ ] `docs/archive.html` updated
- [ ] `docs/index.html` “Latest” updated (if this week’s ship)
- [ ] IG teaser scheduled (Shivam lane) with UTM link

## Post-publish

- [ ] `metrics/monthly-dashboard.csv` end-of-month row (batch OK)
- [ ] `CONTRIBUTION_LOG.md` updated (who shipped what)
