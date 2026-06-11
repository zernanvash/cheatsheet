# Windows Fundamentals

Use this before Windows privilege escalation and AD blueprints. The goal is to recognize Windows structure, users, permissions, UAC, and common administration surfaces.

Source summarized:

- Esther7171 TryHackMe walkthrough: [Windows Fundamentals 1](https://github.com/Esther7171/TryHackMe-Walkthroughs/blob/main/Room/Windows%20Fundamentals%201/readme.md)

## Core Concepts

- NTFS: Windows file system with permissions, ownership, alternate data streams, and auditing features.
- `%windir%`: system variable that usually points to `C:\Windows`.
- `System32`: core binaries, libraries, drivers, and administrative tools.
- User profiles: normally under `C:\Users\username`.
- Groups: local or domain groups control permissions and logon rights.
- UAC: User Account Control, a boundary that affects admin token behavior.

## Accounts And Groups

Commands to understand:

```cmd
whoami
whoami /priv
whoami /groups
net user
net localgroup
net localgroup administrators
```

Important groups:

- Administrators: local admin control.
- Remote Desktop Users: RDP logon permission.
- Remote Management Users: WinRM-related access on many systems.
- Backup Operators: can become high impact because of backup/restore rights.
- Users: normal low-privilege group.
- Guest: built-in guest access account, usually disabled.

## UAC And Privileges

UAC means local administrators may run with a filtered token until elevated.

Useful checks:

```cmd
whoami /priv
whoami /groups
systeminfo
```

High-signal privileges:

- `SeImpersonatePrivilege`
- `SeBackupPrivilege`
- `SeRestorePrivilege`
- `SeDebugPrivilege`
- `SeAssignPrimaryTokenPrivilege`

## File System And Config Places

Check carefully in CTF labs:

- `C:\Users\*\Desktop`
- `C:\Users\*\Documents`
- `C:\inetpub\wwwroot`
- `C:\Program Files`
- `C:\Program Files (x86)`
- `C:\Windows\Temp`
- scheduled task paths
- service executable paths
- web `web.config` files

## Task Manager And Process Thinking

Task Manager shortcut: `Ctrl+Shift+Esc`.

What to learn from processes:

- Which user owns the process.
- Whether it runs as `SYSTEM`, service account, app pool, or normal user.
- Command line and executable path.
- Network connections and listening services.

## When To Jump To Blueprints

- Windows shell landed -> [Windows Privilege Escalation Blueprint](../blueprints/machine-attacks/Windows%20Privilege%20Escalation%20Blueprint.md).
- WinRM/RDP credential found -> [WinRM And RDP Access](../blueprints/machine-attacks/WinRM%20And%20RDP%20Access.md).
- Domain ports present -> [Active Directory Attack Path Cheat Sheet](../tools/Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md).
- MSSQL present -> [MSSQL To Command Execution](../blueprints/machine-attacks/MSSQL%20To%20Command%20Execution.md).
