# C Reversing Cheat Sheet

Use this when a native ELF/PE decompiler shows C-like validation logic and you need to translate it into a solve path. The goal is to recognize common compiler output, unsafe input patterns, C library calls, integer behavior, and data transforms.

## First Questions

| Question | Why it matters |
|---|---|
| Is the binary ELF or PE? | Determines calling convention, library names, and debugger choice. |
| 32-bit or 64-bit? | Affects pointer width, stack layout, and argument passing. |
| Stripped or symbols present? | Symbols can reveal `main`, `check`, `verify`, `win`, `print_flag`. |
| Dynamically linked? | Imports reveal `strcmp`, `memcmp`, `scanf`, `fgets`, `srand`, `rand`, `crypt`, `system`. |
| Does it read stdin, argv, file, env, or network? | Determines how to feed candidates and trace input. |

## C Type Sizes To Watch

Common CTF assumptions on x86/x86-64:

| C type | Typical size | Reversing note |
|---|---:|---|
| `char` / `uint8_t` | 1 | Signedness may change comparisons. |
| `short` / `uint16_t` | 2 | Watch zero/sign extension. |
| `int` / `uint32_t` | 4 | Arithmetic often wraps at 32 bits. |
| `long` | 4 on Windows x64, 8 on Linux x64 | Do not assume without ABI context. |
| `long long` / `uint64_t` | 8 | Often appears in packed constants. |
| pointer | 4 or 8 | Architecture dependent. |

Compiler clues:

```c
(char)x      // low 8 bits only
(short)x     // low 16 bits only
(uint32_t)x  // wraps modulo 2^32
```

Python modeling:

```python
x8 = value & 0xff
x32 = value & 0xffffffff
```

## Input Functions

| Function | Reversing meaning |
|---|---|
| `scanf("%s", buf)` | Whitespace-delimited string; likely overflow if no width. |
| `scanf("%d", &x)` | Integer parsing; reproduce signed decimal behavior. |
| `fgets(buf, n, stdin)` | Keeps newline if room; strip or include `\n` depending on check. |
| `read(0, buf, n)` | Raw bytes; may accept null bytes. |
| `gets(buf)` | Classic stack overflow target. |
| `argv[1]` | Command-line argument validation. |
| `getenv("KEY")` | Environment variable challenge. |
| `fopen` / `fread` | Flag/key may come from file path. |

Newline trap:

```c
fgets(buf, 32, stdin);
if (strcmp(buf, "secret") == 0) ...
```

This fails for `secret\n`. Check whether the code strips newline with `strcspn`, `strlen`, or manual null termination.

## String And Memory Checks

| C call | What to inspect |
|---|---|
| `strcmp(a, b)` | Zero means equal. Strings stop at `\0`. |
| `strncmp(a, b, n)` | Only first `n` bytes matter. |
| `memcmp(a, b, n)` | Raw byte compare; null bytes matter. |
| `strlen(s)` | Stops at first null byte. |
| `strstr(s, needle)` | Substring gate. |
| `strchr(s, c)` | Character membership or delimiter parsing. |

Branch shape:

```c
if (strcmp(input, "secret") == 0)
    success();
else
    fail();
```

Assembly clue:

```asm
call strcmp
test eax, eax
je success
```

## Signedness And Extension

Decompiled checks may lie about signedness. Watch instructions:

| Instruction | Meaning |
|---|---|
| `movzx eax, byte ptr [...]` | zero-extend unsigned byte |
| `movsx eax, byte ptr [...]` | sign-extend signed byte |
| `cmp al, imm8` | 8-bit comparison |
| `and eax, 0xff` | byte truncation |

Python helpers:

```python
def u8(x):
    return x & 0xff

def s8(x):
    x &= 0xff
    return x - 0x100 if x & 0x80 else x

def u32(x):
    return x & 0xffffffff

def s32(x):
    x &= 0xffffffff
    return x - 0x100000000 if x & 0x80000000 else x
```

## Common Validation Patterns

### Direct String Compare

```c
if (!strcmp(input, "flag{...}")) success();
```

Solve path:

```bash
strings -n 4 ./challenge
ltrace ./challenge
```

### Byte Transform

```c
for (int i = 0; i < n; i++)
    out[i] = (input[i] ^ 0x42) + i;
memcmp(out, expected, n);
```

Invert in reverse order:

```python
expected = [0x31, 0x28, 0x35]
plain = bytes(((b - i) ^ 0x42) & 0xff for i, b in enumerate(expected))
print(plain)
```

### `srand()` / `rand()`

```c
srand(0x1337);
for (int i = 0; i < n; i++)
    input[i] == ((rand() % 256) ^ expected[i]);
```

Solve path:

- Identify the seed.
- Identify the modulo/truncation.
- Replay with the same C runtime when possible.
- Linux glibc and Windows MSVCRT `rand()` are different.

See [REV Python Toolkit](REV%20Python%20Toolkit.md) for replay snippets.

### Checksum Gate

```c
sum += input[i];
x ^= input[i];
prod *= input[i];
```

Solve path:

- If input length and charset are small, brute force.
- If constraints are arithmetic, use Z3.
- If checksum is rolling or CRC-like, search constants and polynomial logic.

### Lookup Table

```c
if (table[(unsigned char)input[i]] != expected[i]) fail();
```

Solve path:

- Dump `table`.
- Build reverse map from output byte to possible input bytes.
- If multiple candidates exist, combine with length/charset/checksum constraints.

### Index Shuffle

```c
out[i] = input[order[i]];
memcmp(out, expected, n);
```

Solve path:

- Extract `order`.
- Invert the permutation.
- Verify duplicate or missing indexes before trusting the decompiler.

## C Library Calls Worth Naming

| Call | Meaning |
|---|---|
| `atoi`, `strtol` | Numeric input; base and signedness matter. |
| `tolower`, `toupper` | Case normalization before compare. |
| `qsort`, `bsearch` | Array reorder/search; inspect callback. |
| `time` | Often seed for `srand`. |
| `sleep` | Delay or anti-bruteforce; patch or skip in local copy. |
| `ptrace` | Linux anti-debug check. |
| `IsDebuggerPresent` | Windows anti-debug check. |
| `CreateFile`, `ReadFile` | Windows file input or flag storage. |
| `RegOpenKey`, `RegQueryValue` | Windows registry gate. |
| `system` | Command execution; useful for pwn/path hijack challenges. |

## Decompiler Cleanup

Rename aggressively:

| Bad name | Better name |
|---|---|
| `v3` | `input_len` |
| `v7` | `i` |
| `sub_401220` | `check_password` |
| `byte_404060` | `expected_bytes` |
| `unk_404100` | `lookup_table` |

Before solving:

- Identify input buffer.
- Identify expected constants.
- Rename loop counters and output buffers.
- Separate transform from compare.
- Write the equivalent Python check.

## Patch Targets

Patch only copies of lab binaries.

| Pattern | Patch idea |
|---|---|
| `jne fail` after compare | Flip to `je` or NOP branch. |
| `call exit` | NOP or jump over. |
| `sleep(999)` | Patch argument or call. |
| anti-debug returns failure | Force success return value. |

Prefer solver scripts when the goal is learning the validation. Use patching when the challenge is specifically about bypassing or when you need to reveal later-stage logic.

## Related

- [REV Python Toolkit](REV%20Python%20Toolkit.md)
- [Reversing CLI Tools Cheat Sheet](Reversing%20CLI%20Tools%20Cheat%20Sheet.md)
- [GDB (gef) Cheat Sheet](GDB%20Cheat%20Sheet.md)
- [Rizin / Radare2 Cheat Sheet](Rizin%20Radare2%20Cheat%20Sheet.md)
- [Reverse Engineering Playbook](../Reverse%20Engineering%20Playbook.md)
