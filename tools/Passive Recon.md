# Passive Recon

Offline-friendly passive recon commands for authorized targets and labs.

## DNS And Registration

```bash
nslookup example.com
dig example.com A +short
dig example.com MX +short
dig example.com NS +short
dig example.com TXT +short
whois example.com
dnsrecon -d example.com
```

Try zone transfer only against scoped nameservers:

```bash
for ns in $(dig example.com NS +short); do dig axfr example.com @$ns; done
```

## Subdomains And People

```bash
theHarvester -d example.com -b all
recon-ng
shodan host 203.0.113.10
```

Use results to build hostnames, emails, usernames, technology clues, and password-spray lists only when authorized.

## Metadata And Public Files

```bash
exiftool file.pdf
exiftool image.jpg
strings -n 8 file
```

Check authors, software versions, usernames, timestamps, GPS data, and internal hostnames.

## Search Operators

```text
site:example.com filetype:pdf
site:example.com inurl:admin
site:example.com intitle:index.of
site:example.com ext:sql OR ext:bak OR ext:zip
```

## Email And Breach Clues

```bash
h8mail -t user@example.com
h8mail -t emails.txt
```

Use breach-derived data carefully; in labs, use it to guide username lists and password policy guesses rather than uncontrolled credential testing.

## Related

- [Dig Cheat Sheet](Dig%20Cheat%20Sheet.md)
- [Networking](Networking.md)
- [Cloud and Misc Recon Alternatives](Cloud%20and%20Misc%20Recon%20Alternatives.md)
