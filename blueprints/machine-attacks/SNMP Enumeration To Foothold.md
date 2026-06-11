# SNMP Enumeration To Foothold

Use when UDP SNMP is open or hinted by scans.

## Signals

- UDP `161` open or `open|filtered`.
- `public` community works.
- SNMP leaks users, process args, routes, installed packages, or service configs.

## Main Path

```bash
snmpwalk -v2c -c public target
snmpwalk -v2c -c public target 1.3.6.1.2.1.25.4.2.1.2
snmpwalk -v2c -c public target 1.3.6.1.2.1.25.4.2.1.5
onesixtyone -c community-strings.txt target
```

Extract:

- usernames
- process command lines with credentials
- internal IPs/routes
- installed software and versions
- listening services missed by TCP scan

## Options To Try

- If `public` fails, brute community strings carefully in lab scope.
- Use leaked usernames for SSH/SMB/AD user lists.
- Use process args to recover database, web, backup, or service credentials.
- Use routes/internal IPs to branch into pivoting.
- Cross-check software versions with [Known CVE Service Exploitation](Known%20CVE%20Service%20Exploitation.md).

## Study Examples

- Cajac source set includes SNMP and network enumeration material in service and network modules.
