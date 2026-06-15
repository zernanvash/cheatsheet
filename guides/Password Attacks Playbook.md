# Password Attacks Playbook

# Standard Environment Variables
```bash
# Copy-paste this block into your terminal workspace before executing commands.
export TARGET="10.10.11.X"        # Target machine IP
export URL="http://10.10.11.X"     # Target base URL / endpoint
export LHOST="10.10.14.X"         # Attacker IP, usually tun0 / VPN interface
export LPORT="4444"               # Primary reverse shell listener port
export LPORT_ALT="4445"           # Secondary staging / shell listener port
```

---


## 9. Password Attacks

### 9.1 Hash Identification

```bash
hashid hash.txt
john --list=formats | grep -i nt
```

> **What to watch out for:** Context is often better than auto-detection. Know whether the hash came from Linux shadow, NetNTLM, Kerberos, ZIP, SSH, or a database.

### 9.2 Hashcat

```bash
hashcat -m <MODE> hash.txt /usr/share/wordlists/rockyou.txt
hashcat -m <MODE> hash.txt /usr/share/wordlists/rockyou.txt --show
```

- **Common Modes:**
  - `3200` = bcrypt (Blowfish)
  - `1000` = NTLM
  - `1800` = sha512crypt
  - `5600` = NetNTLMv2
  - `13100` = Kerberoast (TGS-REP)
- **Example (bcrypt):**
  ```bash
  hashcat -m 3200 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt
  ```

### 9.3 John the Ripper

```bash
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
john hash.txt --show
```

- **Extracting Non-Standard Hashes (Pre-processors):**
  - **ZIP Archives:** `zip2john archive.zip > zip.hash`
  - **SSH Keys:** `ssh2john id_rsa > ssh.hash`
  - **PDF Files:** `pdf2john document.pdf > pdf.hash`

### 9.4 Hydra & Medusa (Online Brute Force)

#### Hydra
```bash
# SSH brute force
hydra -l user -P /usr/share/wordlists/rockyou.txt ssh://$TARGET

# FTP brute force with thread throttling (-t 8)
hydra -l user -P /usr/share/wordlists/rockyou.txt ftp://$TARGET -t 8
```

#### Medusa
```bash
# SSH brute force with thread speed (-t 4)
medusa -h $TARGET -U users.txt -P /usr/share/wordlists/rockyou.txt -M ssh -t 4
```

> **What to watch out for:** Prefer offline cracking when possible. For online attacks, confirm scope and watch for lockouts, throttling, and false positives. Limit threads (`-t`) to prevent crash/denial of service on target ports.

### 9.5 Wordlists

```bash
cewl $URL -w words.txt
cat users.txt passwords.txt | sort -u > candidates.txt
```

### 9.6 Password Mutation

```bash
hashcat --stdout words.txt -r /usr/share/hashcat/rules/best64.rule > mutated.txt
```

> **What to watch out for:** Build target-specific lists from names, hostnames, domains, page text, comments, and discovered files.

[↑ Back to Table of Contents](#table-of-contents)

---



## Tool Reference

### Wordlists

Wordlists

```bash
ls /usr/share/wordlists
ls /usr/share/seclists
```

> **What to watch out for:** Match wordlists to the task: directory discovery, usernames, passwords, APIs, parameters, DNS, or fuzzing.



### External References

External References

- [Blueprint Index](../blueprints/Blueprint%20Index.md)
- [Learning Path Index](../learning/Learning%20Path%20Index.md)
- [Tools Index](../tools/Tools%20Index.md)
- [References Index](../references/References%20Index.md)
- [Challenge Use Cases](../references/Challenge%20Use%20Cases.md)

[↑ Back to Table of Contents](#table-of-contents)



---

[↑ Return to Hub](../H4G%20Training.md)
