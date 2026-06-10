# Cloud and Misc Recon Alternatives

Integrated from Sec-Fortress cloud/misc notes and writeups.

## Google Cloud Storage

When a site references GCS buckets:

- inspect source for `storage.googleapis.com`
- try bucket URL patterns
- check object listing permissions
- use `gcloud` only with an authorized account

Commands:

```bash
gcloud auth login
gcloud config set project PROJECT_ID
gcloud storage buckets list
gcloud storage ls gs://bucket-name/
```

If listing is denied, test known object paths from source code, JS, or error messages.

## AWS Route 53 / DNS

Check:

- public hosted zones
- record types: A, AAAA, CNAME, MX, TXT, NS, SOA
- routing policy hints: weighted, latency, failover, geolocation
- stale CNAME records

Use with [Dig Cheat Sheet](Dig%20Cheat%20Sheet.md).

## Azure Automation Runbooks

If Azure Automation access is in scope:

- review runbooks for embedded credentials
- inspect managed identity permissions
- check variables, credentials, and schedules
- avoid printing secrets except in isolated labs

## ICMP / Packet Clues

Some CTF machines leak data through ICMP or packet captures.

- `sudo tcpdump -i tun0 icmp -A`
- `sudo tcpdump -i tun0 -w capture.pcap`
- open `pcap` in Wireshark
- inspect HTTP, FTP, DNS, ICMP payloads

Look for:

- credentials in cleartext
- hidden payloads in ICMP data
- hostnames
- file transfers

## Port Knocking

If ports appear closed but hints suggest knocking:

- inspect web/source/hints for ordered ports
- `knock ip port1 port2 port3`
- rescan after knocking

## TFTP

TFTP often has no authentication.

- `tftp ip`
- `get filename`
- try guessed filenames: `id_rsa`, `config`, `backup`, `flag.txt`

## NTLM Theft From Writable Shares

In AD labs with writable SMB shares and user interaction:

1. Generate a harmless LNK/SCF-style test artifact.
2. Start `responder`.
3. Place artifact in writable share.
4. Crack captured NetNTLMv2 offline if captured.

Tools seen in Sec-Fortress writeups:

- `ntlm_theft`
- `responder`
- `john --format=netntlmv2`

## Credential Dump Sorting

After authorized NTDS dumping:

- normalize output into columns
- separate enabled/disabled users
- prioritize admins/service accounts
- crack NT hashes offline
- validate only in scope

