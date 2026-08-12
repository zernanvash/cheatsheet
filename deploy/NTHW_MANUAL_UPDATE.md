# Manually update the NTHW snapshot

The reader is published at `https://ch.zernanvash.dev/nthw/`. Its content is an attributed, non-commercial snapshot of the official NTHW `nthw` branch.

From the deployed H4G checkout, refresh the snapshot only when you choose:

```bash
python3 scripts/build_nthw_snapshot.py
git status --short nthw/data.json nthw/LICENSE-NTHW.md
```

Review the recorded commit and counts, then commit and deploy the two generated files. The updater uses a temporary shallow clone, accepts Markdown links with `http`, `https`, or `mailto` destinations, and replaces `data.json` only after validation succeeds.

If the existing Nginx static root points at the H4G checkout, no proxy is required. Optionally make the slash redirect explicit in the existing `ch.zernanvash.dev` server block:

```nginx
location = /nthw {
    return 301 /nthw/;
}
```

This mirror must remain non-commercial and preserve attribution under the upstream CC BY-NC-ND 4.0 terms.
