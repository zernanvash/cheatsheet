# Dig Cheat Sheet

## Basic Queries

- `dig domain.com` - default A record lookup
- `dig domain.com A` - IPv4 address
- `dig domain.com AAAA` - IPv6 address
- `dig domain.com MX` - mail records
- `dig domain.com NS` - name servers
- `dig domain.com TXT` - TXT records
- `dig domain.com CNAME` - canonical name
- `dig domain.com SOA` - zone authority record

## Short Output

- `dig domain.com +short`
- `dig domain.com MX +short`
- `dig domain.com NS +short`
- `dig domain.com TXT +short`

## Query A Specific DNS Server

- `dig @8.8.8.8 domain.com`
- `dig @1.1.1.1 domain.com`
- `dig @dns.server.ip domain.com A`

## Reverse DNS

- `dig -x 8.8.8.8`
- `dig -x ip +short`

## Trace Resolution

- `dig domain.com +trace` - show recursive path from root servers
- `dig domain.com +trace +nodnssec` - trace without DNSSEC noise

## Zone Transfer Test

- `dig axfr domain.com @nameserver`
- `dig axfr domain.com @ns1.domain.com`

If AXFR works, inspect exposed hosts, subdomains, mail servers, and internal naming patterns.

## Useful Options

- `+short` - compact output
- `+noall +answer` - only answer section
- `+noall +authority` - authority section only
- `+noall +additional` - additional section only
- `+norecurse` - disable recursive query
- `+tcp` - force TCP DNS
- `+time=3` - timeout in seconds
- `+tries=1` - retry count

## Recon Patterns

Find name servers:

```bash
dig domain.com NS +short
```

Check each name server:

```bash
dig @ns1.domain.com domain.com A
dig @ns1.domain.com domain.com MX
dig @ns1.domain.com domain.com TXT
```

Try zone transfer:

```bash
for ns in $(dig domain.com NS +short); do dig axfr domain.com @$ns; done
```

Check SPF/DMARC/DKIM hints:

```bash
dig domain.com TXT +short
dig _dmarc.domain.com TXT +short
dig selector._domainkey.domain.com TXT +short
```

## Common Findings

- exposed internal hostnames
- old mail or VPN records
- cloud verification TXT records
- weak SPF policy
- zone transfer enabled
- stale CNAME pointing to unclaimed service

