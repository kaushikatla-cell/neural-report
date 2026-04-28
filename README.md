# Neural Report (NRP)

**Co-founders:** Divyam Gupta · Kaushik Atla · Shivam Pande  

Student-run editorial desk at the intersection of **AI** and **economics**: weekly **NRP Evidence Briefs** with public methodology, citations, and corrections.

## Live website (GitHub Pages)

**https://kaushikatla-cell.github.io/neural-report/**

Set Instagram `@neural.report` bio URL to the homepage (optionally with UTMs per `metrics/KPI_DEFINITIONS.md`).

## Where everything lives

| What | Path |
|------|------|
| **Public site (deployed)** | [`docs/`](docs/) — HTML/CSS served by GitHub Pages from `/docs` on `main` |
| **Sample published brief** | [`docs/briefs/2026-04-27-has-gen-ai-raised-productivity.html`](docs/briefs/2026-04-27-has-gen-ai-raised-productivity.html) |
| **Brief template (HTML)** | [`docs/briefs/_template.html`](docs/briefs/_template.html) |
| **Editorial spine** | [`EDITORIAL_SPINE.md`](EDITORIAL_SPINE.md) |
| **Roles & decision rights** | [`COFOUNDER_ROLES.md`](COFOUNDER_ROLES.md) |
| **Verifiable contribution log** | [`CONTRIBUTION_LOG.md`](CONTRIBUTION_LOG.md) |
| **Drafting checklist (Markdown)** | [`templates/evidence-brief-template.md`](templates/evidence-brief-template.md) |
| **12-week cadence table** | [`templates/SERIES_12_WEEK_OUTLINE.md`](templates/SERIES_12_WEEK_OUTLINE.md) |
| **Partnerships / syllabus / guests** | [`outreach/VALIDATION_PLAYBOOK.md`](outreach/VALIDATION_PLAYBOOK.md) |
| **KPI definitions + CSV** | [`metrics/KPI_DEFINITIONS.md`](metrics/KPI_DEFINITIONS.md), [`metrics/monthly-dashboard.csv`](metrics/monthly-dashboard.csv) |
| **Validation artifact drop folder** | [`outreach/artifacts/`](outreach/artifacts/) |

## Repository

**https://github.com/kaushikatla-cell/neural-report**

## Weekly workflow

1. Copy [`templates/evidence-brief-template.md`](templates/evidence-brief-template.md) → `drafts/YYYY-MM-DD-slug.md` (create `drafts/` locally if needed).
2. Fact-check; publish HTML under `docs/briefs/` using [`docs/briefs/_template.html`](docs/briefs/_template.html).
3. Add a row to [`docs/archive.html`](docs/archive.html); commit and push; post IG teaser linking to the live brief URL.

## Custom domain (optional)

In the repo: **Settings → Pages → Custom domain** (e.g. `neural.report`). Add the DNS records your registrar shows. Optionally add `docs/CNAME` with the hostname (GitHub can also commit CNAME automatically from Settings).

## License

MIT — see [`LICENSE`](LICENSE).
