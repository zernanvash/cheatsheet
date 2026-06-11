# Restricted Shell Escape

Use after SSH or command access lands in rbash, a menu shell, a jailed command, or a limited web terminal.

## Signals

- Shell blocks `/`, `cd`, `PATH`, redirection, or common binaries.
- Login drops into a menu, editor, backup script, or custom command loop.
- `echo $SHELL`, `id`, or `env` show constrained environment.

## Main Path

```bash
echo $SHELL
echo $PATH
pwd
ls -la
env
```

Identify allowed binaries and whether the restriction is shell-level, application-level, or filesystem jail.

## Options To Try

- SSH command override: `ssh user@target -t bash`, `sh`, or an allowed full path.
- Editors/pagers: `vi`, `less`, `man`, `find`, `awk`, `python`, `perl`, `tar` if allowed.
- PATH repair if only command lookup is restricted.
- SFTP/SCP file write when SSH shell is restricted but file transfer works.
- If jail is real, enumerate writable files and scheduled jobs from inside the jail.

## Study Examples

- Sec-Fortress and HMV machines often use restricted shells before a Linux privesc branch.
- Pair with [Environment Variable And Library Hijack](Environment%20Variable%20And%20Library%20Hijack.md) when allowed commands run privileged helpers.
