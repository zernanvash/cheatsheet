# SSTI To RCE

Use when user input is evaluated by a server-side template engine.

## Signals

- Reflected `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`, or template errors.
- Flask/Jinja2, Twig, Nunjucks, ERB, Freemarker, Velocity, or similar stack hints.
- Profile, name, search, email template, or preview fields render server-side.

## Main Path

```text
{{7*7}}
${7*7}
<%= 7*7 %>
```

Prove evaluation, fingerprint the engine, then read config or safe variables before moving to command execution in a lab.

## Options To Try

- Check multiple contexts: URL parameter, JSON body, form field, header, and cookie.
- If arithmetic is filtered, try engine-specific syntax or encoded payloads.
- Look for config secrets, debug mode, and app paths before shell.
- If the template engine is sandboxed, search for known sandbox escape primitives by version.

## Study Examples

- Sec-Fortress `Templated`: Flask/Jinja2 SSTI progresses to RCE.
- picoCTF `SSTI1`: useful support practice for template fingerprinting.
