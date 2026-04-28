# Security policy

## Supported versions

This repository is a **static site** (`docs/`) plus Markdown operational files. There are no server-side runtime dependencies to version.

## Reporting a vulnerability

If you believe you have found a **security issue** (for example, XSS via user-generated content we add in the future, or a secret accidentally committed to git):

1. **Do not** open a public GitHub issue with exploit details.
2. Email the maintainers at **hello@yourdomain.com** once that inbox exists, **or** use GitHub **Private vulnerability reporting** for this repository (Settings → Security).

We will acknowledge reasonable reports within a few business days and coordinate a fix if applicable.

## Secrets

Never commit API keys, Formspree secrets, or analytics tokens. GA4 measurement IDs in `docs/js/nrp-core.js` are **public by design** once set (they appear in browser traffic).
