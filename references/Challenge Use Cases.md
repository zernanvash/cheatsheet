# Challenge Use Cases

Use this page when a tool or technique is in a path note but you want examples of when it appears and how it is used in real lab-style challenges. These are study references, not target instructions.

## Web Use Cases

### SQL Injection

Use when a form, parameter, cookie, or API field appears to influence a database query. Signals include SQL errors, printed backend queries, login behavior that changes after a quote, numeric IDs, CMS versions with known SQLi, or time delays after `SLEEP`.

Examples:

- picoCTF `Irish-Name-Repo 1`: login form prints or implies a query like `SELECT * FROM users WHERE name='admin' AND password='...'`; bypass is done by changing the password field into a tautology and SQL comment.
- picoCTF `Irish-Name-Repo 2`: same login pattern, but the useful injection is in the username path; `admin' --` style payloads bypass the password check.
- picoCTF `Web Gauntlet`: repeated SQLi rounds with filters; study this for how comments, blocked keywords, and alternate syntax change payload shape.
- TryHackMe `Simple CTF`: web discovery identifies CMS Made Simple 2.2.8, then a public unauthenticated SQLi is used to extract credentials.
- TryHackMe `Plotted-TMS`: directory fuzzing finds an app panel, then a login bypass with `admin' OR 1=1#` gives access to the management app.

How it is used:

1. Confirm injection with a harmless quote or boolean difference.
2. Identify whether the context is string, numeric, login, search, JSON, or cookie.
3. Use comments to remove the rest of the backend query when needed.
4. Prefer manual proof first, then SQLMap on a captured request for enumeration.
5. Use recovered data for the next branch: admin login, SSH credential reuse, password cracking, or app config review.

Path references:

- [Web Exploit Path - SQL Injection](../guides/Web%20Exploit%20Path.md#5-sql-injection)
- [Web Testing - SQL Injection](../tools/Web%20Testing.md#sql-injection)

### Content Discovery With Gobuster Or ffuf

Use when the web root is sparse, a default page hides the real app, or you need files/extensions/vhosts.

Examples:

- TryHackMe `Simple CTF`: `gobuster` finds CMS paths that lead to version identification and SQLi.
- TryHackMe `Lian_Yu`: `ffuf` is used repeatedly, including extension-focused fuzzing after a `.ticket` hint.
- TryHackMe `Publisher`: `ffuf` with multiple extensions discovers useful files and app routes.
- HackMyVM `Decode`: `gobuster` and `ffuf` are used to find nested paths and filesystem-style LFI hints.
- HackMyVM `Demons`: `gobuster` finds hidden paths while page comments contain an encoded route clue.

How it is used:

1. Start with common paths and a small wordlist.
2. Add extensions based on stack hints: `.php`, `.txt`, `.bak`, `.zip`, `.sql`, `.aspx`.
3. Filter known false positives by status, size, words, or lines.
4. Re-run inside discovered directories.
5. Switch to vhost fuzzing when hostnames or virtual hosting appear.

Path references:

- [Web Exploit Path - Content Discovery](../guides/Web%20Exploit%20Path.md#2-content-discovery)
- [Web Testing - Directory And Parameter Discovery](../tools/Web%20Testing.md#directory-and-parameter-discovery)

### LFI And Directory Traversal

Use when a parameter looks like it selects a page, template, document, language, or file. Signals include paths in errors, `?page=`, `?file=`, `?view=`, and source code that passes user input into file reads.

Examples:

- HackMyVM `Greatwall`: `page` parameter reads `/etc/passwd`, confirms local users, and leads to RFI/SSRF-style follow-up.
- HackMyVM `Observer`: custom app exposes LFI, which is used to extract SSH keys and history.
- HackMyVM `Decode`: robots and path clues lead into LFI-style enumeration.
- TryHackMe `Smol`: WordPress plugin LFI reads configuration and supports code review.
- HackTheBox/TryHackMe `Beep`: Elastix-era LFI is used to read sensitive files.

How it is used:

1. Prove file read with `/etc/passwd` or a safe known file.
2. Read app source and config before trying exploitation.
3. Pull usernames, keys, database credentials, and log paths.
4. Consider log poisoning only after confirming a readable log and lab authorization.

Path references:

- [Web Exploit Path - LFI And Directory Traversal](../guides/Web%20Exploit%20Path.md#7-lfi-and-directory-traversal)
- [Web Testing - LFI And Traversal](../tools/Web%20Testing.md#lfi-and-traversal)

### Command Injection

Use when a web app wraps a system command: ping, traceroute, DNS lookup, image conversion, compiler, archive processing, YAML/template execution, or scheduled scripts.

Examples:

- picoCTF `caas`: command-as-a-service challenge where shell metacharacters are the core path.
- HackMyVM `Baseme`: encoding manipulation leads into command injection.
- HackMyVM `CVE1`: unsafe YAML deserialization gives a reverse shell, then OpenSSL `c_rehash` command injection is abused through a crafted filename in a writable cron-controlled directory.

How it is used:

1. Test with `id`, `whoami`, or `sleep`, not a shell.
2. Try separators such as `;`, `|`, `&&`, command substitution, and newline where relevant.
3. If input is filtered, check space bypasses and encoding.
4. Convert proof into a controlled shell only in the lab scope.

Path references:

- [Web Exploit Path - Command Injection](../guides/Web%20Exploit%20Path.md#8-command-injection)
- [Web Testing - Command Injection](../tools/Web%20Testing.md#command-injection)

### SSTI

Use when the app reflects input through a template engine, especially Flask/Jinja2, Twig, Nunjucks, ERB, Freemarker, or Velocity.

Examples:

- HackTheBox `Templated`: Flask/Jinja2 SSTI progresses from arithmetic proof to server-side code execution.
- picoCTF `SSTI1`: challenge designed around detecting and escalating template expression evaluation.

How it is used:

1. Prove evaluation with `{{7*7}}` or equivalent syntax.
2. Fingerprint the template engine.
3. Read safe variables and config first.
4. Escalate to command execution only in authorized labs.

Path references:

- [Web Exploit Path - SSTI](../guides/Web%20Exploit%20Path.md#10-ssti)
- [Web Testing - SSTI](../tools/Web%20Testing.md#ssti)

### XSS

Use when user-controlled input is rendered into HTML, JavaScript, markdown, filenames, support tickets, comments, or admin panels.

Examples:

- Proving Grounds `Pebbbles`: reflected XSS appears with LFI and SQLi-to-RCE in the same web chain.
- CTF admin-review patterns: stored XSS is commonly used when a bot or admin later views submitted content.

How it is used:

1. Prove execution with a harmless `alert(1)` or controlled callback.
2. Determine reflected, stored, or DOM-based behavior.
3. Check context: HTML body, attribute, script string, URL, markdown.
4. In labs, use it to reach the challenge objective; do not collect real user sessions outside scope.

Path references:

- [Web Exploit Path - XSS](../guides/Web%20Exploit%20Path.md#6-xss)
- [Web Testing - XSS](../tools/Web%20Testing.md#xss)

### WebAssembly Checks

Use when the page loads a `.wasm` file or JavaScript calls exported validation functions.

Examples:

- picoCTF WebAssembly-backed web checks: `.wasm` module stores comparison logic or expected bytes; solving becomes a reverse engineering task.

How it is used:

1. Download the `.wasm` module.
2. Run `strings`, `wasm2wat`, or `wasm-decompile`.
3. Locate exported functions, constants, byte arrays, XOR/add/subtract transforms, and index shuffles.
4. Rebuild the check in Python.

Path references:

- [Web Exploit Path - WebAssembly-Backed Web Challenges](../guides/Web%20Exploit%20Path.md#12-webassembly-backed-web-challenges)
- [Reverse Engineering Path - WebAssembly](../guides/Reverse%20Engineering%20Path.md#8-webassembly)

## Machine And Service Use Cases

### Nmap

Use at the start of nearly every machine to identify live hosts, open ports, service versions, OS hints, and script findings.

Examples:

- HackMyVM `Greatwall`: ping sweep and full TCP scan identify the web service that leads to LFI.
- HackMyVM `Demons`: full scan identifies FTP anonymous login, SSH, and HTTP.
- TryHackMe `Simple CTF`: initial and targeted scans show FTP, HTTP, and SSH on nonstandard port `2222`.

How it is used:

1. Discover hosts with `-sn` or ARP.
2. Find all TCP ports with `-p-`.
3. Run `-sC -sV -O` on discovered ports.
4. Use NSE scripts only when the service and scope justify it.

Path references:

- [Machine Exploit Path - Port Scanning](../guides/Machine%20Exploit%20Path.md#2-port-scanning)
- [Nmap Cheat Sheet](../tools/Nmap%20Cheat%20Sheet.md)

### SMBClient And SMB Enumeration

Use when ports `139` or `445` are open, especially with anonymous shares, readable files, writable shares, Windows hosts, Samba, or AD environments.

Examples:

- HackMyVM `Crossroads`: `smbclient -L` lists shares, anonymous share access exposes files, and later authenticated access is used with found credentials.
- TryHackMe `Reset`: `smbclient` finds a writable `Data` share, which supports NTLM capture and cracking.

How it is used:

1. Try anonymous share listing.
2. Connect to readable shares and recursively list/download.
3. Search files for credentials, scripts, backups, and user lists.
4. If writable and in scope, consider controlled file-placement or NTLM capture workflows.

Path references:

- [Machine Exploit Path - Service Enumeration](../guides/Machine%20Exploit%20Path.md#3-service-enumeration)
- [SMBClient Cheat Sheet](../tools/SMBClient%20Cheat%20Sheet.md)

### Hydra

Use when you have a likely username, a scoped service, and authorization to test passwords. Prefer this in labs after user enumeration or leaked usernames.

Examples:

- TryHackMe `Year of the Rabbit`: a discovered `ftpuser` is tested against FTP with a generated password list.
- HackMyVM `Friendly3`: Hydra tests FTP for a known user.
- HackMyVM `Gameshell2`: Hydra tests an HTTP basic/auth-protected terminal path.
- HackMyVM `Darkside`: Hydra tests a web login form with a known user and failure string.

How it is used:

1. Confirm the service and login syntax manually.
2. Use one known username or a small user list.
3. Match the protocol module to the real login flow.
4. For web forms, identify the failure string accurately.
5. Stop when a valid credential is found; reuse carefully across scoped services.

Path references:

- [Machine Exploit Path - Credential Attacks](../guides/Machine%20Exploit%20Path.md#5-credential-attacks)
- [Password Attacks - Hydra](../tools/Password%20Attacks.md#hydra)

### John And Hashcat

Use when you have an offline hash or encrypted file. This is safer than online guessing and should be preferred when the challenge gives hash material.

Examples:

- TryHackMe `Tomghost`: `john` cracks an `.asc`/GPG-related hash workflow.
- TryHackMe `Smol`: `john` cracks WordPress phpass hashes and a password-protected ZIP via `zip2john`.
- TryHackMe `LazyAdmin`: `hashcat -m 0` cracks an MD5-style hash.
- HackMyVM `Deeper`: `zip2john` converts a ZIP hash, then `john` cracks it.
- Vulnyx `Air`: wireless capture material is converted and cracked with John.

How it is used:

1. Identify hash type with context or a hash identifier.
2. Convert files with `ssh2john`, `zip2john`, `keepass2john`, or similar.
3. Crack offline with a wordlist.
4. Test recovered passwords against only relevant scoped accounts/services.

Path references:

- [Machine Exploit Path - Credential Attacks](../guides/Machine%20Exploit%20Path.md#5-credential-attacks)
- [Password Attacks - John](../tools/Password%20Attacks.md#john)
- [Password Attacks - Hashcat](../tools/Password%20Attacks.md#hashcat)

### Metasploit

Use when the module provides reliable version checks, exploit setup is complex, or the lab clearly expects a known framework path.

Examples:

- MS17-010/EternalBlue-style labs: use the auxiliary scanner first, then the exploit module only after `check` confirms likely vulnerability.
- IPMI labs: auxiliary modules enumerate versions or dump challenge hashes for offline cracking.

How it is used:

1. Use scanner/auxiliary modules before exploit modules.
2. Set `RHOSTS`, `RPORT`, `LHOST`, and payload deliberately.
3. Run `check` where supported.
4. Keep session actions focused on lab proof and next-step enumeration.

Path references:

- [Machine Exploit Path - Metasploit Decision Points](../guides/Machine%20Exploit%20Path.md#6-metasploit-decision-points)
- [Metasploit](../tools/Metasploit.md)
- [EternalBlue Cheat Sheet](../tools/EternalBlue%20Cheat%20Sheet.md)

## Reverse Engineering Use Cases

### GDB And Assembly

Use when a binary asks for input, stores constants, compares registers/memory, or asks for a value at a specific address.

Examples:

- picoCTF `GDB baby step` series: break at requested addresses and inspect registers or memory.
- picoCTF `Bit-O-Asm` series: read small assembly snippets and infer return values or arithmetic.

How it is used:

1. Run `file` and `strings` first.
2. Break at `main` or the requested address.
3. Inspect registers with `info registers`.
4. Inspect memory with `x/s`, `x/16xb`, or `x/gx`.
5. Convert decimal, hex, or ASCII exactly as the challenge asks.

Path references:

- [Reverse Engineering Path - GDB Workflow](../guides/Reverse%20Engineering%20Path.md#4-gdb-workflow)
- [REV Python Toolkit - picoCTF REV Patterns](../tools/REV%20Python%20Toolkit.md#picoctf-rev-patterns)

### Python Solver Scripting

Use when the challenge is a reversible transform: XOR, Caesar/ROT, index shuffle, byte addition/subtraction, Base64/hex layers, or constraints.

Examples:

- picoCTF `vault-door` series: Java/Python-like validation functions map to byte transforms and index checks.
- picoCTF `reverse_cipher`: reverse a deterministic character transform.
- HackMyVM Temperance solvers: remote services send encoded or transformed challenges and expect scripted answers.

How it is used:

1. Extract expected bytes or constants.
2. Rewrite the validation logic as a Python transform.
3. Reverse the operation where possible.
4. Use Z3 when constraints are relational rather than direct transforms.

Path references:

- [Reverse Engineering Path - Solver Scripting](../guides/Reverse%20Engineering%20Path.md#10-solver-scripting)
- [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md)

