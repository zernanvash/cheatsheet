# SSH Key And Credential Reuse

Use when you find passwords, usernames, private keys, or password-protected archives during service enumeration.

## Signals

- `id_rsa`, `.ssh`, backup archives, KeePass, configs, database dumps, scripts.
- Same username appears across web, SMB, FTP, Linux `/home`, or AD.
- Passwords are found in web configs, source, logs, or notes.

## Main Path

```bash
chmod 600 id_rsa
ssh -i id_rsa user@target
ssh user@target
hydra -L users.txt -P passwords.txt ssh://target
```

Crack protected keys:

```bash
ssh2john id_rsa > id_rsa.hash
john id_rsa.hash --wordlist=/usr/share/wordlists/rockyou.txt
```

## Options To Try

- Try credentials across SSH, FTP, SMB, WinRM, RDP, web admin, database, and `su`.
- Build username formats from full names: `first.last`, `f-last`, `flast`, `first`, `last`.
- If key auth fails, check allowed username and key permissions.
- If password works for low-priv user, enumerate local privesc immediately.
- If creds are domain creds, branch into Kerberoasting and SMB share enumeration.

## Study Examples

- Cajac John the Ripper basics covers `ssh2john`, archives, NTLM, and unshadow cracking workflows.
- Many TryHackMe easy rooms progress through credential reuse rather than direct exploit.
