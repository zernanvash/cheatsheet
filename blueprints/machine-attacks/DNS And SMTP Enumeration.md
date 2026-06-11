# DNS And SMTP Enumeration

Use when DNS or SMTP exposes names, domains, users, or internal hosts that unlock the next attack.

## Signals

- DNS `53` open with domain names.
- SMTP `25/465/587` open.
- Nmap or TLS certs reveal domain and hostnames.
- Web content contains email addresses.

## Main Path

DNS:

```bash
dig NS domain.local
dig axfr domain.local @target
dnsrecon -d domain.local -n target
```

SMTP:

```bash
nc -nv target 25
smtp-user-enum -M VRFY -U users.txt -t target
smtp-user-enum -M RCPT -U users.txt -t target
```

## Options To Try

- If zone transfer works, add hosts to `/etc/hosts` and rescan hostnames/vhosts.
- Use email addresses to build usernames for SSH, SMB, Kerberos, and web auth.
- If SMTP VRFY is disabled, try RCPT or EXPN where allowed.
- Check SMTP banners for product/version CVEs.
- If domain names appear, switch to AD or vhost enumeration.

## Study Examples

- Cajac Fowsniff-style and service enumeration writeups use mail/user discovery to drive credential attacks.
- 0xb0b year indexes include AD and web challenges where DNS names determine the route.
