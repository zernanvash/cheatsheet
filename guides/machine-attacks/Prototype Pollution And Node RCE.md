# Prototype Pollution And Node RCE

Use when a Node.js app merges user-controlled JSON, query parameters, or object paths into server-side objects.

## Signals

- Stack hints: Express, Node, npm packages, JSON APIs.
- Parameters such as `__proto__`, `constructor`, `prototype`, nested keys, or merge behavior.
- Source code shows lodash/merge-style object assignment or template rendering from polluted values.

## Main Path

```bash
curl -i -H 'Content-Type: application/json' -d '{"__proto__":{"polluted":"yes"}}' http://target/api
```

Prove pollution with a harmless property or behavior change first. Escalate only if the app routes polluted properties into templates, command execution, file paths, or auth logic.

## Options To Try

- Try JSON body, URL-encoded body, query string, and nested object notation.
- Test `constructor.prototype` when `__proto__` is filtered.
- Review `package.json` and lockfiles for vulnerable libraries.
- If source is unavailable, look for reflected behavior, debug routes, or errors after pollution.

## Study Examples

- Sec-Fortress `Kiba`: prototype pollution leads toward code execution.
- picoCTF and web challenge sources are useful practice for tracing JavaScript object flow.
