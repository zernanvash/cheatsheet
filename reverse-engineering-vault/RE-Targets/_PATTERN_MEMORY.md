# Reverse Engineering Pattern Memory

This file stores compact, reusable lessons from verified target work. It is not a generic glossary and must not contain guessed facts.

## Promotion Standard

Add a pattern only when all of the following are true:

- It was observed in a real target or controlled exercise.
- The technique produced useful evidence or a verified solve.
- The entry links to the target note, solve log, or saved artifact.
- Challenge-specific offsets, flags, keys, and constants have been generalized or omitted.

## Pattern Index

| Signal | Classification | First useful action | Evidence source |
|---|---|---|---|
| _No promoted patterns yet_ | — | — | — |

## Pattern Entry Template

### Pattern: Short descriptive name

**Signals**

- Observable clue from strings, imports, control flow, data layout, or runtime behavior.

**Interpretation**

- Evidence-backed meaning and important alternatives.

**Fast test**

```bash
# Minimal command that confirms or rejects the pattern.
```

**Reliable approach**

1. First evidence-gathering action.
2. Transformation, trace, model, or bypass.
3. Verification against the original target.

**Failure modes**

- A misleading signal or assumption to avoid.

**Provenance**

- Target: `[[RE-Targets/target-name/_TARGET_NOTE]]`
- Solve log: `[[RE-Targets/target-name/_SOLVE_LOG]]`
- Artifact: `RE-Targets/target-name/artifacts/example.py`
