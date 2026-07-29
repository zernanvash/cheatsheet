# Reverse Engineering Second Brain

This is the operational home page for active reversing work. Reference material explains techniques; this page answers four immediate questions:

1. What am I solving?
2. What is known from evidence?
3. What is the next smallest useful action?
4. What should never be repeated?

## Start Or Resume

### Existing target

1. Open the target's `_SOLVE_LOG.md`.
2. Read every failed approach named in its queue.
3. Open the current `IN_PROGRESS` approach, or the first `PENDING` approach.
4. Perform exactly one approach and save every artifact under the target's `artifacts/` directory.
5. End by marking the approach `SOLVED` or `FAILED`; never leave stale `IN_PROGRESS` state.

### New target

1. Create `RE-Targets/<target-name>/` with `approaches/` and `artifacts/` subdirectories.
2. Copy [[RE-Targets/_TARGET_TEMPLATE]] to `RE-Targets/<target-name>/_TARGET_NOTE.md`.
3. Create `_SOLVE_LOG.md` using [[RE-Targets/_SOLVE_LOG_TEMPLATE]].
4. Perform static triage before runtime analysis.
5. Record observed facts, classify the logic, and create the smallest evidence-backed approach queue.

## Active Target Dashboard

Update this table whenever a solve log changes state. This is an index, not the source of truth; the target's `_SOLVE_LOG.md` remains authoritative.

| Target | Status | Logic | Current approach | Blocker | Next action | Updated |
|---|---|---|---|---|---|---|
| _None yet_ | — | — | — | — | Create or select a target | — |

## Retrieval Route

Use this order instead of searching the whole vault blindly:

| Need | Open first | Then |
|---|---|---|
| Resume a target | Target `_SOLVE_LOG.md` | Failed file, current approach, artifacts |
| Choose a method | [[blueprints/Reverse Engineering Blueprint]] | Relevant tool cheat sheet |
| Recall a reusable pattern | [[RE-Targets/_PATTERN_MEMORY]] | Linked solved target and artifact |
| Learn a tool | `tools/` cheat sheet | Main playbook |
| Compare with prior challenges | `rev_source/` | Read-only `_source_crackmesone/` material |

## Evidence Discipline

- Observations must name their source: command output, file offset, address, decompiler view, debugger trace, or runtime behavior.
- Hypotheses are explicitly labeled and never promoted to facts without verification.
- Unknown widths, signedness, offsets, constants, and branch conditions remain `unknown`.
- A flag is recorded only after the original binary or checker accepts it.
- Failed approaches are permanent memory. Record why they failed and what must not be repeated.

## Memory Promotion

After a verified solve:

1. Finish the target note and solve log.
2. Keep the successful scripts and debugger commands under `artifacts/`.
3. Add one compact, generalized entry to [[RE-Targets/_PATTERN_MEMORY]].
4. Link the pattern back to the target so the evidence remains inspectable.
5. Update the dashboard above and the relevant practice tracker.

Only promote a technique when it is reusable. Challenge-specific secrets, flags, offsets, and constants stay in the target folder.
