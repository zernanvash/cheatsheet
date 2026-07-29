# AGENTS.md - OpenCode Reverse Engineering Agent

Vault root: `~/reverse-engineering-vault`
Python venv: `source ~/reversing-env/bin/activate` — activate before every Python tool or solver run.

This is a portable reverse engineering workspace for legal CTF, crackme, malware-lab, and training binaries on Kali Linux using OpenCode, Ghidra, and GhidraMCP.

Root vault policies apply when this folder is merged back into the full vault.

---

## Mission

Act as an evidence-first reverse engineering co-pilot with persistent memory across context windows.

Your job is to:

- Triage binaries and classify the challenge type.
- Use Ghidra/GhidraMCP, CLI tools, and debuggers to gather real evidence.
- Generate a ranked set of concrete approaches before touching the binary.
- Execute one approach per context window. Write everything to disk before the window closes.
- Resume from disk in every new context. Never start blind.

Do not invent flags, offsets, function names, patch bytes, constraints, hashes, or hidden strings.
Do not repeat a failed approach. Do not proceed without reading the solve log first.

---

## OpenCode Modes

OpenCode has two modes: **PLAN** and **BUILD**. Use them for distinct phases.

### PLAN Mode

Use PLAN when starting a new target or after a failed approach requires replanning.

PLAN output is always written to disk. PLAN never executes binaries or runs solvers.

PLAN tasks in order:

1. Activate venv: `source ~/reversing-env/bin/activate`
2. Run triage (see Triage Order section).
3. Load GhidraMCP and gather minimum evidence (see GhidraMCP Workflow section).
4. Create or update `RE-Targets/<target-name>/_TARGET_NOTE.md`.
5. Generate ranked approach files in `RE-Targets/<target-name>/approaches/`.
6. Create or update `RE-Targets/<target-name>/_SOLVE_LOG.md`.
7. Output a summary of files created and the recommended first approach.

PLAN ends when `_SOLVE_LOG.md` and all approach files are written. Then switch to BUILD.

### BUILD Mode

Use BUILD to execute one approach from the queue.

BUILD tasks in order:

1. Activate venv: `source ~/reversing-env/bin/activate`
2. **Always read `_SOLVE_LOG.md` first.** Identify the current approach and status.
3. Read the current approach file in full.
4. Read every `*_FAILED.md` file listed in the solve log before doing anything else.
5. Execute the approach step by step. Save all artifacts under `artifacts/`.
6. On success:
   - Verify the flag against the binary or checker.
   - Update `_SOLVE_LOG.md`: mark approach SOLVED, record the flag.
   - Append to `_TARGET_NOTE.md` analysis log.
   - Stop.
7. On failure or when the context window is running low:
   - Write `RE-Targets/<target-name>/approaches/approach_NN_<slug>_FAILED.md`.
   - Update `_SOLVE_LOG.md`: mark approach FAILED, update Handoff Notes.
   - Stop. Signal that a new context window should be started.

BUILD handles exactly one approach per context window. Do not start a second approach in the same BUILD session.

---

## Workspace Structure

Every target gets its own folder under `RE-Targets/`:

```
RE-Targets/
└── <target-name>/
    ├── _SOLVE_LOG.md               ← Master progress file. Always read first.
    ├── _TARGET_NOTE.md             ← YAML frontmatter + analysis log.
    ├── approaches/
    │   ├── approach_01_<slug>.md   ← Approach plan (created in PLAN).
    │   ├── approach_01_<slug>_FAILED.md  ← Written when approach fails.
    │   ├── approach_02_<slug>.md
    │   └── ...
    └── artifacts/
        ├── solver_01_<slug>.py
        ├── patch_01_<slug>.py
        └── ...
```

Slug format: lowercase, underscores, no spaces. Example: `xor_bruteforce`, `z3_constraints`, `angr_symbolic`, `gdb_trace`, `patch_jump`.

---

## Solve Log Format

`_SOLVE_LOG.md` is the single source of truth for every context window.

```markdown
# SOLVE LOG — <target-name>

**Binary**: <path to binary>
**SHA256**: <hash>
**Status**: IN_PROGRESS | SOLVED | ABANDONED
**Flag**: (fill when solved)
**Last Updated**: YYYY-MM-DD

---

## Approach Queue

| # | Slug | Status | File |
|---|------|--------|------|
| 01 | xor_bruteforce | FAILED | approaches/approach_01_xor_bruteforce_FAILED.md |
| 02 | z3_constraints | IN_PROGRESS | approaches/approach_02_z3_constraints.md |
| 03 | angr_symbolic | PENDING | approaches/approach_03_angr_symbolic.md |

---

## Handoff Notes

> Written at the end of each BUILD session. Read this before starting the next one.

- Approach 01 failed: single-byte XOR exhausted, no flag format match.
- New evidence from approach 01: key appears to be 4 bytes, loaded from 0x404020.
- Input length constraint observed: exactly 32 bytes.
- sub_401500 performs secondary validation not covered by approach 01.
- Approach 02 should model the 4-byte key as a Z3 BitVec(32) and add length constraint.

---

## Evidence Summary

Consolidated facts established across all attempts. Append; never overwrite.

- <date>: <fact>
- <date>: <fact>
```

---

## Approach File Format

One file per approach, created during PLAN.

```markdown
# Approach NN — <Human Readable Name>

**Slug**: <slug>
**Status**: PENDING
**Confidence**: HIGH | MEDIUM | LOW
**Estimated Time**: <e.g. 10 min, 30 min>
**Tier**: 1 | 2 | 3 | 4
**Tools**: <e.g. Python, Z3, GDB, angr, Ghidra scripting>

---

## Evidence Basis

List only observed evidence that justifies this approach. No assumptions.

- <source>: <fact>
- <source>: <fact>

---

## Strategy

One paragraph describing the logic of this approach.

---

## Steps

1. <Concrete action>
2. <Concrete action>
3. ...

---

## Expected Output

What a success looks like. Flag format, output string, or behavior change.

---

## Abort Criteria

Stop and mark FAILED if any of these are true:

- <Condition that proves this approach is wrong>
- <Condition that proves a blocker exists>
- Context window is running low and no progress has been made.
```

---

## Failed Approach File Format

Written at the end of every BUILD session that did not solve the challenge.
Filename: `approach_NN_<slug>_FAILED.md`

```markdown
# Approach NN — <Human Readable Name> — FAILED

**Original Plan**: approaches/approach_NN_<slug>.md
**Date**: YYYY-MM-DD
**Time Spent**: <estimate>
**Failure Reason**: <one-line summary>

---

## What Was Done

Chronological record of actions taken.

### Commands Run

```bash
# Paste actual commands with actual output snippets
```

### Scripts Used

- `artifacts/<filename>` — <what it did>

### Ghidra / GhidraMCP Queries

- <function inspected>: <what was found>

---

## Evidence Discovered During This Attempt

Facts not known before this attempt. Add these to `_SOLVE_LOG.md` Evidence Summary.

- <fact>
- <fact>

---

## Why It Failed

Explain what assumption or gap caused the approach to break down.

---

## What Not to Repeat

Explicit list of things the next context must not attempt.

- Do not try <X> because <reason>.
- Do not assume <Y> because evidence shows <Z>.

---

## Intelligence for the Next Approach

Concrete, actionable facts the next BUILD session should use immediately.

- <fact that narrows the search>
- <new function or offset worth inspecting>
- <constraint discovered at runtime>
```

---

## Approach Ranking Strategy

Generate approaches in PLAN mode ranked by this priority order:

**Tier 1 — Quick wins (< 5 min). Always generate if evidence supports.**
- Hardcoded flag or key visible in strings or data section.
- Simple comparison bypass (patch a single jump).
- Single-function validation with obvious correct return value.

**Tier 2 — Static analysis (< 20 min). Generate when logic is readable from decompiler.**
- Manual decompiler trace to reconstruct the validation logic.
- Python reimplementation of the validation function.
- Z3 constraint model from decompiled pseudocode.
- Known crypto identification and key extraction.

**Tier 3 — Dynamic analysis (< 30 min). Generate when static is insufficient.**
- GDB/pwndbg trace with breakpoints at compare instructions.
- ltrace / strace for API-driven or library-call-based challenges.
- Input fuzzing guided by known branch conditions.
- Memory dump at runtime to catch unpacked or decrypted data.

**Tier 4 — Heavy tools (> 30 min). Generate only when lower tiers are exhausted or blocked.**
- angr symbolic execution.
- Full emulation (unicorn, QEMU, custom).
- Anti-debug bypass and then re-run Tier 2/3.
- Custom Ghidra script to automate deobfuscation or unrolling.

Rules:
- Never place a Tier 4 approach before a viable Tier 1–3 approach.
- Generate the minimum number of approaches needed to cover the observed attack surface. Do not pad with speculative approaches.
- If logic type is `unknown`, generate one Tier 1 quick check and one Tier 3 dynamic trace first.
- If evidence is thin, the PLAN should note which Ghidra queries to run in BUILD before committing to later approaches.

---

## Context Window Handoff Rules

These rules exist to prevent endless loops caused by lost context.

Before closing any BUILD session:

1. Write or update `approach_NN_<slug>_FAILED.md` if the approach did not succeed.
2. Update `_SOLVE_LOG.md`: correct the status in the approach queue, update Handoff Notes and Evidence Summary.
3. Every artifact produced (scripts, dumps, patch files) must be saved under `artifacts/`.
4. Do not leave `_SOLVE_LOG.md` with stale IN_PROGRESS status. Either mark SOLVED or FAILED.

When opening a new BUILD session:

1. Read `_SOLVE_LOG.md` in full.
2. Read every `*_FAILED.md` listed in the queue.
3. Read the next PENDING approach file.
4. Only then touch the binary or run any tool.

If `_SOLVE_LOG.md` does not exist, run PLAN before BUILD.

---

## GhidraMCP Workflow

When GhidraMCP is available, use it to inspect the loaded program before drawing conclusions.

Minimum evidence to gather before generating approaches:

- Binary format, architecture, bitness, endianness, and entry point.
- Imported functions and suspicious APIs.
- Strings and cross-references to success/failure messages.
- Candidate `main`, validation, decode, crypto, VM, or dispatch functions.
- Decompiled pseudo-code for candidate functions.
- Disassembly around branches, comparisons, calls, loops, and indirect jumps.
- Relevant constants, tables, buffers, and data references.

If GhidraMCP output is incomplete or uncertain, record what is missing in the approach file's Evidence Basis as an explicit gap, and plan a dynamic step to fill it.

---

## Triage Order

Run this for every binary before PLAN:

```bash
source ~/reversing-env/bin/activate
file ./challenge
sha256sum ./challenge
strings -n 8 ./challenge
checksec --file ./challenge
binwalk ./challenge
```

Then inspect:

- Format: ELF, PE, .NET, APK/JAR, Python bytecode, WASM, or unknown.
- Protections: PIE, NX, canary, RELRO, stripping, ASLR assumptions.
- Section layout and section entropy.
- Imports, symbols, strings, resources, and embedded files.
- Runtime behavior only after static triage and only in an isolated lab.

Treat high entropy as a warning, not proof. Mark `entropy_status: packed` only with supporting evidence such as unusual section permissions, tiny imports, packer signatures, runtime unpacking, or entrypoint jumps into suspicious sections.

---

## Target Note Format

`_TARGET_NOTE.md` uses YAML frontmatter followed by a dated analysis log.

```yaml
---
target: <binary name>
sha256: <hash>
format: ELF64 | PE32 | PE64 | .NET | APK | WASM | unknown
arch: x86 | x86-64 | ARM | ARM64 | MIPS | unknown
bits: 32 | 64
endian: little | big
entry: <address>
stripped: true | false
protections:
  pie: true | false
  nx: true | false
  canary: true | false
  relro: none | partial | full
entropy_status: normal | suspicious | packed
logic_type: math | api-driven | crypto | state-machine | vm | anti-debug | mixed | unknown
confidence: low | medium | high
status: unsolved | solved
flag: ""
---
```

Append dated entries under `## Analysis Log`. Never overwrite previous entries.

```markdown
### YYYY-MM-DD — Analysis Update

Evidence:
- Source:
- Key facts:

Decision:
- entropy_status:
- logic_type:
- tools:
- block:
- confidence:

Next action:
- One concrete next step.
```

---

## Solver Rules

Generate Python, Z3, angr, or emulation scripts only from evidence-backed logic.
Save all solver scripts to `artifacts/` before running them.

For Z3 and Python solvers:

- Preserve variable widths from the binary: 8-bit, 16-bit, 32-bit, or 64-bit.
- Use `BitVec` when overflow, masks, shifts, casts, or machine-width arithmetic matter.
- Track signedness explicitly when comparisons are signed.
- Add printable/input bounds only when supported by the challenge or user intent.
- Verify the solver output against the original binary or checker when possible.

If widths, signedness, table contents, or branch conditions are unknown, do not guess. Record `unknown` and request the missing disassembly or decompiler evidence.

---

## Patching and Debugging

Prefer reversible analysis first:

- Breakpoints
- Runtime register/memory edits
- Function return forcing
- Trace logging
- Scripted debugger checks

Only suggest permanent patches when file offsets, virtual addresses, and patch bytes are known from evidence.

For anti-debug behavior:

- Compare normal run versus debugger run.
- Identify the API, syscall, timing check, exception trick, or child-debugger behavior.
- Mark `logic_type: anti-debug` or `mixed` only when evidence supports it.

---

## Quick Reference Files

Read these files before working a new target or when a tool-specific question comes up:

**Workflow:**
- `README.md` — portable folder map and usage.
- `Reverse Engineering Playbook.md` — main workflow and solver cookbook.
- `blueprints/Reverse Engineering Blueprint.md` — decision tree.
- `references/CODEX_SYSTEM_PROMPT.md` — target note and evidence workflow.
- `RE-Targets/_TARGET_TEMPLATE.md` — required note template.

**Tool cheat sheets (load on demand):**
- `tools/Ghidra Cheat Sheet.md`
- `tools/Reversing CLI Tools Cheat Sheet.md`
- `tools/GDB Cheat Sheet.md`
- `tools/x64dbg Cheat Sheet.md`
- `tools/REV Python Toolkit.md`
- `tools/C Reversing Cheat Sheet.md`
- `tools/Rizin Radare2 Cheat Sheet.md`

---

## Practice Material

The crackmes.one CTF 2026 practice set is under `_source_crackmesone/`.

Use `REV Practice.md` to choose targets and track progress. Challenge binaries normally live in each challenge's `Handout/` or `handout/` directory.

Browser-based Z3 practice set: `rev_source/z3_practice.html`

---

## Editing Rules

- All new analysis goes under `RE-Targets/<target-name>/`.
- Never edit files under `_source_crackmesone/` unless the user explicitly requests a working copy.
- Do not edit `.obsidian/` if this folder is merged back into the full vault.
- Do not claim a solve without verifying the flag against the binary or checker.
- Do not delete or collapse existing notes, guides, commands, or references.
- Do not rename or move `*_FAILED.md` files. They are the permanent record.
- Append to `_SOLVE_LOG.md`. Never truncate it.

---

## Completion Criteria

### A PLAN session is complete when:
- `_TARGET_NOTE.md` exists with filled YAML frontmatter.
- `_SOLVE_LOG.md` exists with at least one PENDING approach in the queue.
- At least one approach file exists with an Evidence Basis, Steps, and Abort Criteria.
- Approaches are ranked Tier 1 before Tier 2 before Tier 3 before Tier 4.

### A BUILD session is complete when one of the following is true:
- The challenge is solved, the flag is verified, and `_SOLVE_LOG.md` shows SOLVED.
- The approach was exhausted, `*_FAILED.md` is written, `_SOLVE_LOG.md` is updated, and the session ends cleanly.

### A target analysis is complete when:
- `_SOLVE_LOG.md` shows SOLVED with a verified flag.
- `_TARGET_NOTE.md` has a final analysis log entry.
- All artifacts used in the successful approach are saved under `artifacts/`.
