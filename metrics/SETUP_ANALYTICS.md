# Site analytics setup (Neural Report)

## Option A — Google Analytics 4 (recommended for “sessions to /briefs/”)

1. Create a GA4 property for the **GitHub Pages hostname** you use (`kaushikatla-cell.github.io` with path `/neural-report` works as a single stream in GA4’s web data stream—verify in GA’s URL configuration).
2. Copy the **Measurement ID** (`G-XXXXXXXX`).
3. Open [`docs/js/nrp-core.js`](../docs/js/nrp-core.js) and set:

   `var GA_MEASUREMENT_ID = "G-XXXXXXXX";`

4. Commit and push; verify **Realtime** shows your visit on a brief URL.

**Note:** GA does not run until the ID is set; the script is a safe no-op before that.

## Option B — Plausible / Fathom / Cloudflare Web Analytics

If you move DNS to Cloudflare or use a paid privacy tool, follow that vendor’s snippet instead of GA—remove or leave GA block empty to avoid double counting.

## Option C — No third-party JS

Use **GitHub traffic** (see `GITHUB_TRAFFIC.md`) + Instagram insights + newsletter provider stats only.
