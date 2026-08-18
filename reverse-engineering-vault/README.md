# Reverse Engineering Vault

Portable RE-focused slice of the H4G CTF vault for Kali Linux, OpenCode, Ghidra, and GhidraMCP.

This folder is designed to be copied as-is to a Kali machine. It keeps the reverse engineering playbooks, tool references, target note workflow, practice material, and crackmes.one CTF 2026 binaries together without requiring the full vault.

## Start Here

- `RE-Targets/_SECOND_BRAIN.md` - active-target dashboard, session entry point, retrieval route, and memory-promotion loop.
- `Reverse Engineering Playbook.md` - main reversing workflow, triage commands, solver cookbook, and tool map.
- `blueprints/Reverse Engineering Blueprint.md` - decision tree for ELF, PE, bytecode, WASM, packed binaries, VM challenges, and more.
- `guides/Reverse Engineering Tool Workflow.md` - situation-driven tool selection for Kali and Windows-host PE work.
- `tools/Print and Format Specifiers Cheat Sheet.md` - C `printf`, Python `%` formatting, f-strings, shell `printf`, byte dumps, and reversing clues.
- `.agents/AGENTS.md` - OpenCode agent instructions for GhidraMCP-assisted solving.
- `references/CODEX_SYSTEM_PROMPT.md` - evidence-first note workflow used by the original vault.

## Folder Map

```text
reverse-engineering-vault/
├── .agents/                         # OpenCode agent instructions
├── RE-Targets/                       # Per-target analysis notes
├── blueprints/                       # RE decision trees
├── guides/                           # RE operational playbooks
├── tools/                            # Ghidra, GDB, x64dbg, Z3, CLI, and C reversing sheets
├── references/                       # x86, syscall, workflow, and use-case references
├── rev_source/                       # Z3 practice and RE study writeups
├── _source_crackmesone/              # crackmes.one CTF 2026 practice binaries/writeups
├── Reverse Engineering Playbook.md
├── REV Practice.md
└── Exercises.md
```

## Suggested Kali Setup

Install the common CLI and Python reversing stack:

```bash
sudo apt update
sudo apt install -y file binutils gdb ltrace strace binwalk radare2 rizin upx-ucl python3-pip
python3 -m pip install --user z3-solver pycryptodome pwntools angr capstone keystone-engine unicorn lief pefile pyelftools
```

Launch Ghidra normally, then let OpenCode use GhidraMCP according to `.agents/AGENTS.md`.

## Target Workflow

1. Open `RE-Targets/_SECOND_BRAIN.md` and resume an active target or pick a challenge from `REV Practice.md`.
2. Create `RE-Targets/<target-name>/`, including `approaches/` and `artifacts/`.
3. Create `_TARGET_NOTE.md` from `RE-Targets/_TARGET_TEMPLATE.md` and `_SOLVE_LOG.md` from `RE-Targets/_SOLVE_LOG_TEMPLATE.md`.
4. Run initial triage:

```bash
file ./challenge
sha256sum ./challenge
strings -n 8 ./challenge
checksec --file ./challenge
binwalk ./challenge
```

5. Import the binary into Ghidra and gather evidence with GhidraMCP.
6. Classify the logic type: `math`, `api-driven`, `crypto`, `state-machine`, `vm`, `anti-debug`, `mixed`, or `unknown`.
7. Rank evidence-backed approaches and execute one approach per session.
8. Append dated updates to the target note and maintain the solve log handoff.
9. After a verified solve, promote only reusable lessons into `RE-Targets/_PATTERN_MEMORY.md`.

## Practice

- `REV Practice.md` tracks the crackmes.one CTF 2026 set.
- `_source_crackmesone/` contains the offline binaries and source material.
- `rev_source/z3_practice.html` contains browser-based Z3 exercises.
- `tools/REV Python Toolkit.md` contains solver templates and common RE Python patterns.

## Safety

Run unknown binaries only inside a VM or disposable lab folder. Prefer static analysis first. Never run suspicious targets as root unless the challenge explicitly requires it and you understand the risk.
