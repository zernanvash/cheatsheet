# Reporting and Remediation Playbook

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


## 11. Reporting and Remediation

### 11.1 Finding Format

Use one finding per vulnerability or attack path.

### 11.2 Evidence Collection

```bash
mkdir -p evidence
cp nmap/*.gnmap nmap/*.nmap evidence/ 2>/dev/null
```

> **What to watch out for:** Save commands, timestamps, screenshots, request/response samples, hashes, user context, and proof output.

### 11.3 Screenshots

Capture proof screens for:

- initial access
- privilege level
- flags/proof files
- sensitive data exposure
- vulnerable request/response
- remediation-relevant configuration

### 11.4 Remediation Notes

Write remediation as engineering actions, not generic advice. Include config files, code patterns, permissions, patch versions, and validation steps when possible.

### 11.5 Final Report Template

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
```

[↑ Back to Table of Contents](#table-of-contents)

---




---

[↑ Return to Hub](../H4G%20Training.md)
