# Web Attack Alternatives

Integrated from Sec-Fortress web articles and writeups. Use in authorized labs and assessments.

## When Basic Fuzzing Stalls

Try alternate dimensions:

- virtual hosts
- HTTP methods
- parameters
- headers
- cookies
- API routes
- backup extensions
- source maps
- robots/sitemap
- framework-specific paths
- default credentials

## Access Control / IDOR

Checklist:

- change numeric IDs: `id=1 -> id=2`
- change UUIDs found in responses
- swap usernames in URL/body
- test object access after logout/login as lower user
- check redirects for leaked data
- test multi-step workflows where only the first step checks role
- try method override: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- check headers: `X-Original-URL`, `X-Rewrite-URL`, `X-Forwarded-For`
- inspect GraphQL object IDs and queries

Common signs:

- user-controlled `role`, `isAdmin`, `accountId`
- predictable filenames
- export/download endpoints
- profile image or attachment IDs

## Authentication Alternatives

Check:

- username enumeration by response length/status/time
- weak reset tokens
- password reset poisoning through host headers
- brute-force rate limit bypass by rotating username/IP/header
- response manipulation in client-side role checks
- default credentials
- password equals username
- reused creds from FTP/SMB/web configs

## Information Disclosure

Look for:

- verbose error messages
- debug pages
- `phpinfo()`
- backup files
- version control history
- `.git/`
- source maps
- hidden comments
- TRACE method headers
- config files and environment dumps

Alternative flow:

1. Identify exact framework/version.
2. Search local source/config leaks before exploit DB.
3. Use leaked credentials on SSH/SMB/database/admin panels.

## File Upload Alternatives

Test:

- extension allowlist bypass: `.phtml`, `.php5`, double extensions
- content-type mismatch
- magic bytes / polyglot files
- filename traversal
- filename command injection
- upload to WebDAV, then rename/move extension
- image processor vulnerabilities
- archive extraction traversal

Safer workflow:

1. Upload a harmless proof file.
2. Confirm reachable path.
3. Confirm execution only in lab scope.
4. Upgrade to shell only after proof.

## WebDAV

Discovery:

- Nmap `http-webdav-scan`
- `davtest -url http://ip/webdav/`
- `cadaver http://ip/webdav/`

Branches:

- upload allowed type -> test execution
- upload harmless file then rename to executable extension
- credentials reused from leaked config

## WordPress

- `wpscan --url http://host/wordpress/`
- enumerate plugins and themes
- check `readme.html`
- check `wp-content/uploads/` listing
- check `xmlrpc.php`
- try known vulnerable plugins by version

Alternative entry:

- valid admin/editor creds -> theme/plugin editor or upload path
- vulnerable plugin -> file upload/RCE
- exposed backup/config -> DB creds

## SSRF

Test locations:

- URL parameters
- webhook fields
- avatar/image fetchers
- PDF generators
- stock-check APIs
- `Referer` header
- XML/HTML importers

Variants:

- basic internal service access
- blacklist bypass
- whitelist bypass
- open redirect chained to SSRF
- blind SSRF with OAST/collaborator
- cloud metadata access in authorized cloud labs

Bypass ideas:

- decimal/hex/octal IP forms
- IPv6 forms
- DNS rebinding lab domains
- embedded credentials in URL
- redirect endpoints

## SSTI

Probe:

- `{{7*7}}`
- `${7*7}`
- `<%= 7*7 %>`
- `#{7*7}`

Then identify engine:

- Jinja2/Twig/Nunjucks
- ERB
- Freemarker
- Velocity

Workflow:

1. Confirm arithmetic evaluation.
2. Fingerprint engine.
3. Read safe variables/config first.
4. Attempt command execution only in lab scope.

## SQL Injection Alternatives

Manual checks:

- boolean-based
- union-based
- error-based
- time-based blind
- stacked queries
- JSON/unicode escaping bypass

SQLMap:

```bash
sqlmap -r req.request --level 5 --risk 3 --batch
sqlmap -r req.request --tamper=charunicodeescape --level 5 --risk 3 --batch
```

If WAF blocks characters:

- try unicode escaped characters
- try comments
- try case changes
- try alternate content types

## XSS To Session Theft In Labs

Check:

- stored profile fields
- support tickets
- admin review panels
- markdown renderers
- file names

Use OAST/collaborator or a controlled listener to prove execution. Do not collect real user cookies outside explicit scope.

## picoCTF Web Patterns

Integrated from `Cajac/picoCTF-Writeups`. Use this branch for CTF/lab web tasks where the challenge is intentionally puzzle-shaped.

### Static Source And Hidden Files

Check first:

- page source
- linked CSS
- linked JavaScript
- comments
- minified code after prettifying
- `/robots.txt`
- `/sitemap.xml`
- `/.htaccess`
- source maps

Common flow:

1. Search HTML for comments and hidden paths.
2. Open every linked CSS/JS file.
3. Decode suspicious Base64, hex, URL-encoded, or HTML entity strings.
4. Follow robots/sitemap hints and combine split flag fragments.

### Cookie And Storage Trust

Inspect:

- cookies
- localStorage
- sessionStorage
- JWT-like values
- URL/Base64 encoded fields

Try changing obvious client-side state in lab tasks:

- `admin`
- `isAdmin`
- `role`
- `user`
- numeric IDs

### Header-Gated Pages

Some tasks check request metadata instead of application logic.

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

Headers worth testing:

- `User-Agent`
- `Referer`
- `Date`
- `DNT`
- `X-Forwarded-For`
- `Accept-Language`
- `Host`

### Login, SQLi, SSTI, SOAP

When a form exists:

- capture with Burp
- test single quote behavior
- compare redirects, response length, and status code
- test template probes such as `{{7*7}}`
- inspect XML/SOAP requests for XXE-style parser behavior in labs
- keep SQLMap as a confirmation tool after manual parameter discovery

### WebAssembly-Backed Web Checks

If JavaScript loads `.wasm`, treat it as a reverse engineering task.

```bash
wget http://target/module.wasm
file module.wasm
strings -n 8 module.wasm
wasm-decompile module.wasm
```

Look for exported functions, constants, comparison loops, XOR, byte subtraction, and index shuffling. Rebuild the transform in Python when the check is deterministic.
