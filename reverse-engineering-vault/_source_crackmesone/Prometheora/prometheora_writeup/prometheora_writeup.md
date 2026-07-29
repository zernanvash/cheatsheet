# Prometheora — Reverse Engineering Writeup

Challenge_URL: https://crackmes.one/crackme/697e95cb977274421cc111e1

**Analyst:** RootRevenant  
**Target:** `prometheora` (ELF64, stripped)  
**Method:** Binary Ninja-led static reverse engineering, plus controlled runtime confirmation.

---

## 1. Executive Summary

This crackme is a deliberately noisy, heavily obfuscated Rust binary with a multi-layer validation pipeline.  
The validation path is real and deterministic, but wrapped in large anti-analysis scaffolding:

- giant stack-frame state machine,
- repeated `_rdtsc` noise and timing arithmetic,
- decoy “dynamic” constants that are actually constant,
- UTF-8/re-encoding side paths,
- opaque arithmetic mix stages.

The true key checks are concentrated in two compact validators called from the core verifier:

- `sub_439610` (structured, deterministic staged checks),
- `sub_4261c0` (additional keyed transform/hash gate).

A third large state machine (`sub_435a20`) contributes additional nonlinear gating.

Deliverables included with this writeup:

- `prometheora_keygen.py` (deterministic key reconstruction + static verifier replay)
- `prometheora_runner.py` (clean-environment launcher with retry logic for timing-window success)

---

## 2. Binary Triage

- **Format:** ELF64 LSB (x86_64)
- **Language/runtime traits:** Rust runtime artifacts, panic paths, allocator wrappers
- **Symbols:** stripped (function names are auto-labeled `sub_xxx`)
- **UI strings present:**
  - `Enter key:`
  - `Incorrect key. Access denied.`
  - `Congratulations! ...`

Success output path resolves to `sub_423ba0`; failure paths route through nearby print helpers (`sub_423dd0`, `sub_424080`, `sub_424200`).

---

## 3. Control-Flow Overview

### 3.1 Front-end input handler

`sub_424910` handles user input parsing, normalization, and dispatch into the deep verifier:

- input is collected and transformed through Rust-style buffer/object plumbing,
- canonical validation call eventually lands in `sub_41a5e0(arg1, arg2)`.

### 3.2 Core verifier

`sub_41a5e0` is the main anti-analysis shell:

- huge local state region,
- frequent `_rdtsc` reads,
- nonlinear accumulator updates,
- multiple helper invocations (`sub_435a20`, `sub_439610`, `sub_4261c0`),
- UTF-8 validity checks (`sub_42acb0`) in side branches,
- final boolean derives from accumulated score and sentinel conditions.

It is designed to look dynamic/timing-unstable while still embedding deterministic key checks.

---

## 4. Deterministic Validation Core (`sub_439610`)

`sub_439610` is a strict pipeline:

```text
sub_4396a0
&& sub_439840
&& sub_4398e0
&& sub_439950
&& sub_4399c0
&& sub_439a30
&& sub_439be0
```

All must pass.

---

## 5. Stage-by-Stage Constraints

## 5.1 Format and character class (`sub_4396a0`)

Hard requirements:

- length must be **0x1c (28)**,
- every char must be in `[A-Z0-9_]`,
- key must contain at least:
  - one uppercase letter,
  - one digit,
  - one underscore,
- total underscore count must be exactly **3**,
- ASCII byte sum of all 28 chars must equal **0x778**.

## 5.2 Positional constraints + 4-byte tail hash (`sub_439840` + `sub_439888`)

Additional fixed rules:

- `key[10] == '_'`
- `key[15] == '_'`
- `key[23] == '_'`
- `key[24..27]` must all be decimal digits.

Then `sub_439888` hashes `key[24..27]` with `sub_43a320(..., k0=0x5945415248415348, k1=0x4b45593031303230)` and compares against `-0x3bcfeca119aaad63`.

Recovered deterministic 4-digit suffix from static reconstruction of `sub_43a320`:

- **`key[24..27] = "2027"`**

## 5.3 Whole-key keyed hash checks (`sub_4398e0`, `sub_439950`, `sub_4399c0`)

Each computes `sub_43a320` over the full 28-byte key with different key pairs and compares to fixed 64-bit constants:

- `sub_4398e0` target: `-0x06cfc51a936b765b`
- `sub_439950` target: `-0x3c8edae5d64f271e`
- `sub_4399c0` target: `-0x5b652c3d3ec4cea2`

(`sub_43a320` is SipHash-like / ARX-based keyed compression.)

## 5.4 4×7-byte segment checks (`sub_439a30`)

The 28-byte key is checked in 4 chunks of 7 bytes:

- `key[0..6]` against `sub_438070(0)`
- `key[7..13]` against `sub_438070(1)`
- `key[14..20]` against `sub_438070(2)`
- `key[21..27]` against `sub_438070(3)`

Important anti-analysis note:

- `sub_438070` appears to depend on `_rdtsc` (`sub_4306e0`) but zeroes the stack slot before use, so outputs are effectively **constant**.

Recovered constants:

- `sub_438070(0) = 0x64ab81fecce00947`
- `sub_438070(1) = 0x6836a10a23dd8e77`
- `sub_438070(2) = 0xb4a1e70dff5ec991`
- `sub_438070(3) = 0x53966b588e01c554`

## 5.5 Polynomial fingerprint stage (`sub_439be0`)

This stage interprets all 28 key bytes as polynomial coefficients and evaluates at five fixed points:

- `x ∈ {0x17, 0x2b, 0x3d, 0x4f, 0x61}`

Each polynomial value is avalanche-mixed and must equal `sub_439ff0(i)` for `i=0..4`.

Same anti-analysis trick as above: `sub_439ff0` includes dead `_rdtsc`-looking setup but resolves to fixed constants.

Recovered targets:

- `sub_439ff0(0) = 0xd6f3ad7fcf60e599`
- `sub_439ff0(1) = 0x61af7543c53e1e80`
- `sub_439ff0(2) = 0x2b54ef961abdf2af`
- `sub_439ff0(3) = 0x6d7b46529261b90e`
- `sub_439ff0(4) = 0xf0983fe510642916`

---

## 6. Additional High-Complexity Gate (`sub_435a20`)

`sub_435a20` is a large custom state machine with:

- state IDs as 64-bit magic constants,
- ARX transforms (`rol/ror/xor/add/sub`),
- periodic integrity-like conditions,
- branch-dependent transitions,
- side checks tied to selected key structure bytes.

It acts as a second nonlinear acceptance filter beyond `sub_439610`.

---

## 7. Anti-Analysis Characteristics

Observed patterns:

1. **RDTSC noise flooding:** frequent timestamp reads injected into unrelated arithmetic.
2. **Dead dynamic dependencies:** helper functions call `_rdtsc` but later overwrite the source variable, yielding constants.
3. **Massive stack/zero-fill regions:** intended to hide signal in volume.
4. **Runtime-like control wrappers:** Rust panic/alloc/thread scaffolding obscures core logic.

This design is meant to waste analyst time with high apparent entropy while preserving deterministic predicates.

---

## 8. Practical Keygen Implications

A working keygen must satisfy all deterministic constraints simultaneously:

- strict format/charset/position/sum rules,
- 4-byte suffix hash condition (`2027` for tail),
- multiple full-key keyed hash equalities,
- 4 segment keyed hash equalities,
- polynomial fingerprint equalities,
- plus acceptance through the larger nonlinear gate path.

The fastest reliable implementation path is:

1. Re-implement `sub_43a320`, `sub_438070`, `sub_439ff0`, and stage predicates exactly.
2. Encode hard format constraints first (positions + charset + suffix).
3. Solve remaining constraints with SAT/SMT + meet-in-the-middle on segmented predicates.
4. Validate candidate against reconstructed `sub_435a20` transitions.

---

## 9. Conclusion

This crackme is not cryptographically random; it is a deterministic, multi-layer constraint system hidden behind deliberate static-analysis friction.

Key reverse-engineering outcome:

- core checks are extractable and structured,
- fake timing-dependency exists but collapses to constants,
- suffix constraint is concretely recoverable (`2027`),
- full solve requires systematic constraint solving rather than brute force.

---

## 10. Recovered Valid Key

Recovered key candidate (from direct verifier reconstruction):

- `PR0M3TH30R_F1R3_UNL34SH_2027`

Derivation path (static):

1. `sub_430410` reconstructs a 28-byte target buffer via LCG stream XOR `data_40d993`.
2. That buffer is compared against user input in `sub_41a5e0`.
3. The recovered bytes simultaneously satisfy all extracted `sub_439610` constraints and hash stages.

## 11. Runtime Behavior Clarification (Important)

Empirical runtime validation shows a timing-sensitive acceptance layer:

- wrong formats/short keys reliably produce explicit fail banner,
- the recovered 28-byte key can enter a deeper path and may fail silently (`exit=1`) on many runs,
- repeated fresh runs eventually hit the success window and print the congratulations banner.

This matches challenge hints about timing-based mutation and non-linear validation behavior.

## 12. Keygen + Reliable Runner Artifacts

Companion scripts (same folder):

- `prometheora_keygen.py`
  - reconstructs/prints key from recovered algorithm
  - replays static verifier checks for confidence
- `prometheora_runner.py`
  - runs the target in a clean minimal environment
  - submits the recovered key and retries until success window is hit

## 13. Reproduction (Operator Quick-Start)

From the binary folder:

```bash
python3 prometheora_keygen.py
python3 prometheora_runner.py
```

Expected behavior:

- `prometheora_keygen.py` prints `PR0M3TH30R_F1R3_UNL34SH_2027` and static-check PASS.
- `prometheora_runner.py` may require multiple attempts due to timing window, then prints the success banner.

## 14. Analyst Notes

- Core reverse engineering was done statically in Binary Ninja.
- Additional runtime confirmation was used only to validate timing-window behavior and successful acceptance path.
