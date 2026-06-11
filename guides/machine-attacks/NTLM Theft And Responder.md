# NTLM Theft And Responder

Use in Windows or AD labs when you can make a target authenticate to your listener and capture NetNTLM material.

## Signals

- Writable SMB share, document upload, LNK path, UNC injection, printer/web callback, or SSRF to `\\attacker\share`.
- Challenge hints mention hashes, responder, relay, or captured authentication.
- SMB signing status and scope permit capture or relay testing.

## Main Path

```bash
responder -I tun0
hashcat -m 5600 netntlmv2.hash /usr/share/wordlists/rockyou.txt
```

After cracking, test the credential against SMB, WinRM, LDAP, RDP, MSSQL, and web admin panels.

## Options To Try

- Use SMB file references, LNK files, SCF files, or UNC paths only in scoped labs.
- Check SMB signing before considering relay.
- If cracking fails, try username-specific wordlists from the target site.
- If a password is recovered, check for password reuse and Kerberoasting/ADCS expansion.

## Study Examples

- Sec-Fortress `Nara`: LNK-style NTLM theft contributes to an AD chain.
- TryHackMe `Reset`: writable SMB share supports NTLM capture and cracking workflows.
