# External Link Audit

This folder stores machine-readable snapshots of external-link health.

- `latest.json` — most recent run output
- `new-failures.json` — URLs newly failing vs previous snapshot
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

Strict-on-regressions mode (non-zero only when there are *new* failures):

```bash
python3 scripts/snapshot_external_links.py --strict-new
```

