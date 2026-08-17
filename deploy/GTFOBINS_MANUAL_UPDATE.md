# Manually update the GTFOBins snapshot

The standalone reader is published at `https://ch.zernanvash.dev/gtfobins/`. It uses an attributed snapshot of the official GTFOBins repository and does not require Jekyll on the server.

Install PyYAML once on the machine used to refresh the data, then run the builder from the H4G checkout:

```bash
python3 -m pip install PyYAML
python3 scripts/build_gtfobins_snapshot.py
git status --short gtfobins/data.json gtfobins/LICENSE-GTFOBINS.txt
```

Review the recorded revision and executable count before committing. Deployment only needs the static `gtfobins/` directory. If the existing Nginx static root points to the H4G checkout, no proxy is required. An optional canonical redirect is:

```nginx
location = /gtfobins {
    return 301 /gtfobins/;
}
```

The upstream material is GPL-3.0. Keep `LICENSE-GTFOBINS.txt`, the upstream attribution, and the educational/authorized-use notice with the mirror.
