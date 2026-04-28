# KPI definitions — Neural Report

Use numbers you can **defend** in an interview or application. Prefer **composites** (subs + saves + workshop count) over a single vanity metric.

## Core KPIs

| KPI | Definition | How to capture |
|-----|------------|----------------|
| **Evidence Briefs shipped** | Count of briefs meeting publish checklist in [templates/evidence-brief-template.md](../templates/evidence-brief-template.md) | Count rows in `docs/archive.html` or files under `docs/briefs/` |
| **Newsletter subscribers** | Total + net new (if newsletter exists) | Export from Substack/Beehiiv/Mailchimp monthly |
| **Site sessions (30d)** | Unique sessions to `/briefs/*` | Plausible, GA4, or host analytics |
| **IG bio link clicks** | Clicks on URL in profile | Link-in-bio tool UTM or Instagram “link taps” if available |
| **IG saves per post** | Saves ÷ reach (or saves absolute) | Instagram insights export / screenshot monthly |
| **External validations** | Count from [VALIDATION_PLAYBOOK.md](../outreach/VALIDATION_PLAYBOOK.md) | Integer + list of artifact filenames |
| **Workshop / talk attendees** | Sum heads for NRP-hosted sessions | Sign-in sheet or Zoom report |

## UTM convention (optional but recommended)

**GitHub Pages example (this repo):** `https://kaushikatla-cell.github.io/neural-report/`

Homepage from bio:

`https://kaushikatla-cell.github.io/neural-report/?utm_source=instagram&utm_medium=bio&utm_campaign=profile`

(or swap in your custom domain later.)

Per brief from Stories:

`https://kaushikatla-cell.github.io/neural-report/briefs/YYYY-MM-DD-slug.html?utm_source=instagram&utm_medium=story&utm_content=slug`

## Honesty rules

- Do not conflate **followers** with **impact** in written materials; pair followers with **briefs shipped** + **saves** or **subs**.
- If follower growth had a specific legitimate driver (ad, viral reel, cross-promo), keep an internal note so you can explain consistently.

## Monthly rhythm

1. On the last day of the month, fill one row in [monthly-dashboard.csv](monthly-dashboard.csv).
2. Screenshot IG insights for that month → store in `metrics/screenshots/` (local, optional).
3. 10-minute cofounder review: what moved, one experiment for next month.
