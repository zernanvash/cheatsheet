# Enigma CrackMe v1.0 — Solution

## TL;DR

Serial format: `XXXX-XXXX-XXXX-XXXX` (16 hex digits, four 16-bit chunks).

Given `name`, valid serial chunks are:

```
key = derive_key(name)                    # FNV-1a-ish 32-bit hash
c0  = transform(key)              & 0xFFFF
c1  = transform(key ^ 0xA5A5A5A5) & 0xFFFF
c2  = transform(key ^ c0)         & 0xFFFF
c3  = (c0 ^ c1 ^ c2)              & 0xFFFF
serial = "{c0:04X}-{c1:04X}-{c2:04X}-{c3:04X}"
```

Validation accumulates `acc |= parsed[i] ^ c[i]` over the four chunks then requires `acc == 0`, so every chunk must match exactly.

## Binary layout

| Symbol | Address (PE) | Role |
|---|---|---|
| `validate_serial` | `0x140005660` | Outer obfuscated FSM that parses input and computes expected chunks |
| `derive_key`      | `0x140008cd0` | FNV-1a-style hash of name |
| `transform`       | `0x1400092d0` | Thin wrapper around `__rt_transform.interp` |
| `__rt_transform.interp` | `0x140009340` | Register-based bytecode VM |
| `_init_rt`        | `0x1400092f0` | Sets `__ga = 0xE5A53755`, `__gb = 0xE0C5DCD3` |
| Bytecode blob     | `0x14000F0C8` | XOR-encrypted VM program |
| Opcode dispatch   | `&_rdata`    | 30-entry jump table (relative offsets) |
| VM syscall table  | `0x14000F260` | Helpers callable from VM |

Linux ELF `enigma_crackme_linux` is **not stripped** — same names available.

## Obfuscation

Two layers, both reduce to identities:

1. **Opaque algebraic predicates** scattered through the code:
   - `__ga * __ga - __ga * (__ga - 1) - __ga ≡ 0` for any `__ga`
   - `iVar4 = (...) + 2 ≡ 2`
   - `x * (x - 1) & 1 ≡ 0` (always)
   - Boolean → arithmetic encodings: `(a ^ b) + 2*(a & b) = a + b`, `(a + b) - 2*(a & b) = a ^ b`, `(a + b) - (a | b) = a & b`, `(a & b) + (a ^ b) = a | b`.

2. **Encrypted state-machine dispatch** in `validate_serial` and the VM:
   - `state` field (`local_28`) advanced by `state = state * 0x45D9F3B7 + const`
   - `next_state` (`local_24`) computed via XOR/add of `state` and a constant
   - The decompiler-visible `iVar2` simplifies to just the bare next-state constant — every `case 0x...` is one logical handler.

Once you collapse those, `validate_serial` is a clean 4-iteration loop:

```c
key = derive_key(name);
expect[0] = transform(key)              & 0xFFFF;
expect[1] = transform(key ^ 0xA5A5A5A5) & 0xFFFF;
expect[2] = transform(key ^ expect[0])  & 0xFFFF;
expect[3] = (expect[0] ^ expect[1] ^ expect[2]) & 0xFFFF;

acc = 0;
for (i = 0; i < 4; i++) acc |= parsed_chunk[i] ^ expect[i];
return acc == 0;
```

## `derive_key` — FNV-1a + post-mix

```c
uint32_t derive_key(const char *name, int len) {
    uint32_t h = 0x811C9DC5;
    for (int i = 0; i < len; i++) {
        h = (h ^ (uint8_t)name[i]) * 0x01000193;
        h ^= h >> 16;
    }
    return h;
}
```

## `transform` — register VM (not re-implemented)

VM specifics (extracted from `__rt_transform.interp`):

- 16 × `uint64` register file (`local_98[16]`)
- 32-bit instructions, fetched from `bytecode[pc]` then XOR-decrypted with `pc*0x45D9F3B7 ^ 0xD719AB91`
- Encoding: `opcode(8) | dst(4) | src1(4) | imm/src2(16)`
- ~28 ops including: `mov`, `add`, `xor`, `or`, `mul`, `shl`, `shr`, `sar`, `eq`, `neq`, `lt`/`ltu`/`le`/`leu`, sign-extend, bit-test, load/store, fetch immediate, conditional jump, syscall, halt-with-reg, halt-with-zero
- Loop guard: aborts after 10,000,000 ops or when next-pc ≥ 0x86

I did **not** reimplement the VM — instead the keygen calls the binary's own `transform` via `gdb`.

## Keygen strategy

Linux binary not stripped + MinGW `gdb` already on `$PATH` ⇒ run `enigma_crackme.exe` under gdb, break at `main` (so `_init_rt` has set `__ga`/`__gb`), then call `derive_key` + `transform` directly with `print`/`set`. Print formatted serial. Quit before continuing.

```bash
# keygen.sh "Name"
gdb -q ./enigma_crackme.exe <<EOF | tr -d '\r' \
  | grep -oE '[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}'
set pagination off
b main
run
set \$k  = (unsigned int)derive_key("$NAME", $LEN)
set \$c0 = (unsigned int)((unsigned long long)transform(\$k)              & 0xffff)
set \$c1 = (unsigned int)((unsigned long long)transform(\$k ^ 0xa5a5a5a5) & 0xffff)
set \$c2 = (unsigned int)((unsigned long long)transform(\$k ^ \$c0)        & 0xffff)
set \$c3 = (\$c0 ^ \$c1 ^ \$c2) & 0xffff
printf "%04X-%04X-%04X-%04X\n", \$c0, \$c1, \$c2, \$c3
quit
EOF
```

## Verified outputs

| Name              | Serial                  | Result   |
|-------------------|-------------------------|----------|
| `Alice`           | `1E4B-E68B-6B92-9352`   | SUCCESS  |
| `Bob`             | `4BB3-8F52-971C-53FD`   | SUCCESS  |
| `ReverseEngineer` | `399A-31DF-AFD3-A796`   | SUCCESS  |
| `Mike2026`        | `CC8C-3D49-0526-F4E3`   | SUCCESS  |

## Files

- `keygen.sh` — keygen (gdb wrapper)
- `enigma_crackme.exe` — target (Windows PE)
- `enigma_crackme_linux` — target (ELF, unstripped)
- `SOLUTION.md` — this file

## Reversing notes / pitfalls

- Ghidra's decompiled `validate_serial` looks ~600 lines of nonsense. ~95% is opaque predicates. Always simplify `(__ga*__ga - __ga*(__ga-1)) - __ga` → `0` and `iVar4` → `2` before reading flow.
- The `state * 0x45D9F3B7 + const` chains are dead — only the constants on each `case` matter.
- `transform` is the only real puzzle piece; everything else is wrapping. A pure-Python re-impl is feasible but not necessary when the binary itself is the cheapest VM.
- `_init_rt` sets `__ga`/`__gb` to non-zero values — don't bypass CRT init when calling functions, or the VM uses bogus seed `local_18`. Breaking at `main` is sufficient.
