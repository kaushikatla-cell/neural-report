# External Link Audit

This folder stores machine-readable snapshots of external-link health.

- `latest.json` — most recent run output
- `latest-delta.md` — new failures/resolved since prior snapshot
- `snapshots/*.json` — timestamped history

Generate locally:

```bash
python3 scripts/snapshot_external_links.py
```

Strict mode (non-zero exit on failures):

```bash
python3 scripts/snapshot_external_links.py --strict
```

