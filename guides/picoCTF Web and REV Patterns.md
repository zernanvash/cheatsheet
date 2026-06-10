# picoCTF Web and REV Patterns

Source analyzed: local clone of `Cajac/picoCTF-Writeups`.

Use this as a CTF/lab checklist for picoCTF-style web exploitation and reverse engineering. Keep it separate from real assessment notes because many picoCTF tasks reward puzzle recognition, client-side trust mistakes, and intentionally exposed challenge artifacts.

## Web Exploitation

### Source Scavenger Flow

Use when the challenge looks simple, static, or "nothing is here".

1. Open DevTools and view page source.
2. Check linked CSS and JavaScript files.
3. Search for flags, comments, base64, URLs, hidden paths, and odd constants.
4. Visit common hint files:
   - `/robots.txt`
   - `/sitemap.xml`
   - `/.htaccess`
   - `/index.css`
   - `/script.js`
5. If JavaScript is minified, prettify or unminify it before reading logic.

Common picoCTF signal:

- challenge names about inspection, scavenger hunts, search source, includes, unminify, or web decode
- important values split across HTML, CSS, JavaScript, and metadata

### Cookies And Client-Side Trust

Use when login/admin state is controlled by browser storage.

Checklist:

- inspect cookies, localStorage, and sessionStorage
- URL-decode and Base64-decode suspicious values
- change boolean or role-like fields such as `admin`, `isAdmin`, `role`, or `user`
- check JWT-like tokens for weak validation in CTF labs
- compare a guest cookie against an authenticated cookie

Do not assume a server-side session. In picoCTF web tasks, the "admin" decision is often exposed in a cookie or client-side value.

### Header Gates

Use when the page says the request must come from a specific browser, site, date, language, or country.

Useful curl pattern:

```bash
curl -s \
  -A "PicoBrowser" \
  -e "http://target/" \
  -H "Date: Mon, 1 Apr 2018 00:00:00 GMT" \
  -H "DNT: 1" \
  -H "X-Forwarded-For: 213.89.89.89" \
  -H "Accept-Language: sv" \
  "http://target/"
```

Headers to test:

- `User-Agent`
- `Referer`
- `Date`
- `DNT`
- `X-Forwarded-For`
- `Accept-Language`
- `Host`

### Request Tampering With Burp

Use Burp or a saved request file when the challenge has forms, JSON APIs, redirects, or hidden POST bodies.

Checklist:

- intercept the request before redirects
- change hidden fields and JSON values
- test different HTTP methods
- replay with modified cookies and headers
- compare status, response length, and body differences

JSON request pattern:

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  --data-binary '{"input":"test"}' \
  "http://host/check"
```

### SQL Injection In Login Forms

Use when login behavior differs by username, error message, or redirect.

Checklist:

- test a single quote in username and password fields
- try comment-based login bypasses in the username field
- compare response length and status code
- capture the request and test with SQLMap only after understanding the parameter
- check if filters are bypassed by comments, casing, or alternate whitespace

Common picoCTF signal:

- challenge names mentioning login, SQL, Irish names, gauntlets, or "more SQL"
- form accepts username/password but no registration path

### SSTI

Use when user input is reflected into a rendered page.

Probe:

```text
{{7*7}}
${7*7}
<%= 7*7 %>
#{7*7}
```

If arithmetic evaluates, fingerprint the template engine before escalating. picoCTF examples commonly reward recognizing Flask/Jinja-style rendering.

### SOAP / XXE

Use when the application sends XML, SOAP actions, or structured XML API requests.

Checklist:

- capture XML request in Burp
- test whether external entities are parsed in the lab
- check if the response leaks local file content or parser errors
- use minimal proof reads before trying broader file discovery

### File Upload Puzzles

Use when the app accepts images or uploaded files.

Checklist:

- identify allowed extensions and MIME checks
- test harmless files first
- check upload path and whether files are renamed
- inspect client-side validation and server error messages
- test alternate extensions only inside lab scope
- check whether the file is interpreted or only stored

### Debug And Memory Artifacts

Use when the challenge name hints at dumps, heap, debug, or head-dump behavior.

Checklist:

- search JavaScript for API endpoints
- check framework debug endpoints
- download exposed dump files only from the challenge host
- search dump content for flags, secrets, URLs, and environment values

### WebAssembly In Web Challenges

Use when JavaScript loads `.wasm` or a binary-looking module.

Workflow:

```bash
wget http://target/module.wasm
file module.wasm
strings -n 8 module.wasm
wasm-decompile module.wasm
```

Look for:

- exported functions
- hardcoded check strings
- XOR constants
- index shuffling
- comparison loops

If the module applies a byte transform, reproduce it in Python instead of solving by hand.

## Reverse Engineering

### First Triage

Run this before opening a debugger:

```bash
file ./challenge
strings -n 8 ./challenge
chmod +x ./challenge
./challenge
```

Then branch:

- readable strings reveal flag or password -> confirm and submit
- ELF asks for input -> use GDB or static disassembly
- Python source -> read and patch checks
- Java/APK -> decompile with jadx
- WebAssembly -> use WABT tools
- packed binary -> check UPX or entropy

### GDB Baby-Step Workflow

Use when the task asks for a register value, memory value, or instruction result.

```bash
gdb ./challenge
layout asm
break *main
run
info registers
x/s 0xADDRESS
x/16xb 0xADDRESS
disassemble main
```

Common picoCTF pattern:

- set a breakpoint at the requested address
- run until the breakpoint
- inspect `eax`/`rax` or the requested register
- convert decimal/hex to the required output format

### Assembly Reading

Focus on comparisons and transformations:

- `cmp` / `test` - branch condition
- `je` / `jne` / `jg` / `jl` - success or failure path
- `mov` - value copy
- `lea` - address math
- `xor` - zeroing or byte transform
- `add` / `sub` - offset transform
- `shl` / `shr` / `rol` / `ror` - bit transform

When reading x86-64, remember that arguments usually start in `rdi`, `rsi`, `rdx`, `rcx`, `r8`, and `r9` on Linux.

### Python Source Challenges

Use when source code is provided or recovered.

Checklist:

- read constants before running the file
- identify password checks and comparison functions
- decode Base64/hex values
- reverse string slicing such as `[::-1]`
- patch out sleeps, network waits, and failure exits
- use `dis` when bytecode or obfuscated functions hide logic

Small transform skeleton:

```python
from pathlib import Path

data = Path("input.bin").read_bytes()
out = bytearray()

for i, b in enumerate(data):
    out.append((b ^ 0x42) & 0xff)

print(bytes(out))
```

### XOR, Index Shuffle, And Character Math

Common picoCTF reversing tasks use:

- single-byte XOR
- repeating-key XOR
- `ord()` / `chr()` arithmetic
- string reversal
- array index reordering
- split flag fragments
- decimal, hex, or ASCII conversions

Repeating-key helper:

```python
def xor_key(data, key):
    key = key if isinstance(key, bytes) else key.encode()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
```

### Java And APK

Workflow:

```bash
jadx-gui app.apk
```

Check:

- `MainActivity`
- hardcoded strings
- resource files
- comparison functions
- native libraries loaded by Java

For `.class` or `.jar`, use a Java decompiler and inspect constants plus validation methods.

### Packed Binaries

If `strings` shows UPX or output is unusually sparse:

```bash
upx -d ./challenge
file ./challenge
strings -n 8 ./challenge
```

If unpacking fails, compare original and unpacked behavior in a debugger and look for runtime-decrypted strings.

### WebAssembly Reverse Engineering

Use WABT:

```bash
wasm2wat module.wasm -o module.wat
wasm-decompile module.wasm > module.c
strings -n 8 module.wasm
```

Then search for:

- memory offsets
- exported check functions
- expected byte arrays
- XOR or subtraction loops

### Visual And Nonstandard Artifacts

Some picoCTF REV tasks are not classic binaries.

Check file type first:

- Blender files may hide visual clues or scripts
- CNC/G-code can reveal paths, text, or coordinates
- images may hide values in pixels or metadata
- CoreWars/Redcode tasks require reading tiny assembly-like programs

## Quick Decision Tree

1. If it is a web page with no obvious feature, inspect source, JS, CSS, robots, and storage.
2. If access depends on identity, try cookies and headers before heavy exploitation.
3. If a form behaves oddly, capture it in Burp and test SQLi/SSTI/XML based on content type.
4. If JavaScript loads WebAssembly, reverse the module as a binary.
5. If a REV file is executable, run `file`, `strings`, then GDB.
6. If source is provided, patch or reproduce the check in Python.
7. If a transform appears, script byte operations and verify against known flag format.
