# SQL Injection To Credentials

Use when a database-backed web endpoint changes behavior with quotes, booleans, numeric IDs, or time delays.

## Signals

- Login bypass behavior.
- SQL errors.
- ID parameter returns different records.
- Time delay functions produce measurable response delay.

## Main Path

```text
'
' or 1=1-- -
' OR SLEEP(5)-- -
```

```bash
sqlmap -u "http://target/item.php?id=1" --batch --dbs
sqlmap -r req.request --level 5 --risk 3 --batch
```

Prioritize:

- users and password hashes
- admin credentials
- app config tables
- file read/write only if authorized and necessary

## Options To Try

- Capture with Burp and use `sqlmap -r` for cookies, JSON, and headers.
- Try boolean, union, error-based, stacked, and time-based approaches.
- Crack hashes with `john`/`hashcat`, then test SSH/SMB/WinRM/web admin reuse.
- If SQLi only leaks usernames, branch to password spray, AS-REP, or Kerberoasting where AD is present.
- If WAF/filtering appears, try tamper scripts or manual payload shaping.

## Study Examples

- 0xb0b TryHackMe index includes SQL injection-focused rooms such as `prioritise` and `sch3ma-d3mon`.
