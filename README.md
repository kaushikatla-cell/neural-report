# Neural Report (NRP)

**Co-founders:** Divyam Gupta · Kaushik Atla · Shivam Pande  

Student-run editorial desk at the intersection of **AI** and **economics**: weekly **NRP Evidence Briefs** with public methodology, citations, and corrections.

## Live website (GitHub Pages)

**https://kaushikatla-cell.github.io/neural-report/**

Set Instagram `@neural.report` bio URL to the homepage (optionally with UTMs per [`metrics/KPI_DEFINITIONS.md`](metrics/KPI_DEFINITIONS.md)).

## Where everything lives

| What | Path |
|------|------|
| **Public site (deployed)** | [`docs/`](docs/) — GitHub Pages serves `/docs` on `main` |
| **RSS 2.0 feed** | [`docs/rss.xml`](docs/rss.xml) |
| **Atom feed** | [`docs/atom.xml`](docs/atom.xml) |
| **Sitemap** | [`docs/sitemap.xml`](docs/sitemap.xml) (also linked in [`docs/robots.txt`](docs/robots.txt)) |
| **llms.txt / security.txt** | [`docs/llms.txt`](docs/llms.txt) · [`docs/.well-known/security.txt`](docs/.well-known/security.txt) |
| **404 page** | [`docs/404.html`](docs/404.html) |
| **Security disclosures** | [`SECURITY.md`](SECURITY.md) |
| **Subscribe / list growth** | [`docs/subscribe.html`](docs/subscribe.html) (RSS/Atom, RSS→email, Web3Forms, newsletter vendors) |
| **Optional GA4** | [`docs/js/nrp-core.js`](docs/js/nrp-core.js) — see [`metrics/SETUP_ANALYTICS.md`](metrics/SETUP_ANALYTICS.md) |
| **Published Evidence Briefs** | [`docs/briefs/`](docs/briefs/) — **5** shipped (Apr 27–May 25, 2026) |
| **PWA manifest** | [`docs/manifest.json`](docs/manifest.json) (Add to Home Screen / `theme-color`) |
| **humans.txt** | [`docs/humans.txt`](docs/humans.txt) |
| **CI: internal link check** | [`.github/workflows/docs-check.yml`](.github/workflows/docs-check.yml) + [`scripts/check_docs.py`](scripts/check_docs.py) |
| **CI: feeds + pages + OG + sitemap = sources** | [`.github/workflows/feeds-validate.yml`](.github/workflows/feeds-validate.yml) + manifest + [`scripts/generate_feeds.py`](scripts/generate_feeds.py) + [`scripts/sync_site_pages.py`](scripts/sync_site_pages.py) + [`scripts/generate_og_images.py`](scripts/generate_og_images.py) |
| **CI: external links (advisory)** | [`.github/workflows/external-links.yml`](.github/workflows/external-links.yml) + [`lychee.toml`](lychee.toml) |
| **CI: citation freshness (strict lychee)** | [`.github/workflows/citation-freshness.yml`](.github/workflows/citation-freshness.yml) (scheduled Wednesdays) |
| **Custom domain / base URL** | [`scripts/rewrite_site_base.py`](scripts/rewrite_site_base.py) |
| **Social preview (site)** | [`docs/images/og-default.png`](docs/images/og-default.png) (1200×630; non-brief pages) |
| **Social preview (briefs)** | [`docs/images/og/`](docs/images/og/) — one **1200×630** PNG per brief from [`scripts/generate_og_images.py`](scripts/generate_og_images.py) |
| **Python deps (OG generation)** | [`requirements.txt`](requirements.txt) (Pillow) |
| **Script notes** | [`scripts/README.md`](scripts/README.md), [`Makefile`](Makefile) (`make publish-check`, `make quality`) |
| **Brief template (HTML)** | [`docs/briefs/_template.html`](docs/briefs/_template.html) |
| **Editorial spine** | [`EDITORIAL_SPINE.md`](EDITORIAL_SPINE.md) |
| **Roles & decision rights** | [`COFOUNDER_ROLES.md`](COFOUNDER_ROLES.md) |
| **Verifiable contribution log** | [`CONTRIBUTION_LOG.md`](CONTRIBUTION_LOG.md) |
| **Application blurb** | [`APPLICATION_BLURB.md`](APPLICATION_BLURB.md) |
| **Drafting checklist (Markdown)** | [`templates/evidence-brief-template.md`](templates/evidence-brief-template.md) |
| **12-week ship plan** | [`templates/SERIES_12_WEEK_OUTLINE.md`](templates/SERIES_12_WEEK_OUTLINE.md) |
| **Weeks 5–12 outlines** | [`drafts/WEEKS_05-12_OUTLINE.md`](drafts/WEEKS_05-12_OUTLINE.md) |
| **Outreach templates** | [`outreach/VALIDATION_PLAYBOOK.md`](outreach/VALIDATION_PLAYBOOK.md) |
| **Validation checklist (Tier-1 proof)** | [`outreach/VALIDATION_CHECKLIST.md`](outreach/VALIDATION_CHECKLIST.md) |
| **Club + syllabus packets** | [`outreach/packets/`](outreach/packets/) |
| **Guest pipeline CSV** | [`outreach/GUEST_PIPELINE.csv`](outreach/GUEST_PIPELINE.csv) |
| **KPI definitions + CSV** | [`metrics/KPI_DEFINITIONS.md`](metrics/KPI_DEFINITIONS.md), [`metrics/monthly-dashboard.csv`](metrics/monthly-dashboard.csv) |
| **GitHub traffic (no JS)** | [`metrics/GITHUB_TRAFFIC.md`](metrics/GITHUB_TRAFFIC.md) |
| **Validation artifact drop folder** | [`outreach/artifacts/`](outreach/artifacts/) |
| **Weekly ship issue template** | [`.github/ISSUE_TEMPLATE/evidence-brief.md`](.github/ISSUE_TEMPLATE/evidence-brief.md) |

## Repository

**https://github.com/kaushikatla-cell/neural-report**

## Weekly workflow

1. Copy [`templates/evidence-brief-template.md`](templates/evidence-brief-template.md) → `drafts/YYYY-MM-DD-slug.md`.
2. Fact-check; publish HTML under `docs/briefs/` using [`docs/briefs/_template.html`](docs/briefs/_template.html).
3. Add a row to [`docs/archive.html`](docs/archive.html); update [`docs/index.html`](docs/index.html) “Latest”; commit and push; post IG teaser with UTM link.

## Custom domain (optional)

Repo **Settings → Pages → Custom domain** (e.g. `neural.report`). Follow DNS instructions from GitHub / registrar.

## License

MIT — see [`LICENSE`](LICENSE).
