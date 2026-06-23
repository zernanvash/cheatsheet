# CrackMe3 Writeup

## Overview

CrackMe3 is a 32-bit Windows GUI application protected with a custom packer/protector. The protector uses CPUID-based hardware fingerprinting (HWID) to lock the executable to a specific machine. The goals are:

1. Find the Original Entry Point (OEP) and run the program from there.
2. Remove all HWID checks.
3. Patch or keygen the key validation.
4. (Bonus) Restore all original (stolen) functions.

Tools used: Python with `pefile` and `capstone` for static analysis; `x64dbg` for dynamic verification.

## Step 1: Initial Reconnaissance

The PE header shows the entry point at RVA `0x74000`, landing in a section called `.xtls`. This immediately signals a packer: normal compilers place the entry point in `.text`.

```
Entry Point:    0x474000  (.xtls)
Image Base:     0x400000
Sections:       .text, .data, .rdata, .bss, .idata, .xdata, .xtls
```

Disassembling the entry point reveals a classic packer stub:

```asm
0x474000:  PUSHAD
0x474001:  SUB ESP, 0x100
0x47400C:  XOR EAX, EAX
0x47400E:  TEST EAX, EAX
0x474010:  JE 0x47405C         ; always-taken jump (obfuscation)
```

The `PUSHAD` followed by obfuscated control flow is a textbook unpacking stub signature.

## Step 2: Tracing the HWID Chain

Starting from the entry point, the stub executes a long chain of `CPUID` instructions using various leaves (`0x0`, `0x80000002`, `0x80000008`, etc.). The results are accumulated into `EDI` through arithmetic (ADD, SUB, XOR). Each block clears all other registers and ends with an always-taken `JE` to the next block:

```asm
0x47649E:  MOV EAX, 0x80000002
0x4764A3:  CPUID
0x4764A5:  SUB EAX, EBX
0x4764A7:  SUB EAX, ECX
0x4764A9:  SUB EAX, EDX
0x4764AB:  XCHG EAX, EDI        ; accumulate into EDI
0x4764AD:  XOR EAX, EAX         ; clear
           ...
0x4764B9:  JE next_block         ; always taken (EAX=0)
```

Multiple such blocks chain together across the `.xtls` and `.xdata` sections. Eventually they converge at HWID "gates" where `EDI` is compared against a computed constant.

## Step 3: Identifying the HWID Gates

Three HWID gates were found. Each one checks the accumulated `EDI` value against a hardcoded expected value. If the check fails, execution jumps to `0x4751D8` which calls `MessageBoxA("Invalid HWID")` and exits.

**Gate 1** at `0x475AC9` (protects string-assign and WndProc init):
```asm
0x475AC9:  SUB EDI, 0x6969BDAD
0x475ACF:  SUB EDI, 0x6969BDAD
0x475AD5:  SUB EDI, 1
0x475AD8:  MOV ESI, 0x23AB38
0x475ADD:  ADD ESI, 0x23AB38     ; ESI = 0x475671
0x475AE6:  CMP EDI, ESI
0x475AE8:  JE  success           ; EDI must equal 0x475671
0x475AEA:  JMP 0x4751D8          ; HWID fail
success:
0x475AEF:  JMP EDI               ; jumps to POPAL + function body
```

**Gate 2** at `0x475A18` (protects the validate function):
```asm
;  ESI = 0x23A98F + 0x23A98F = 0x47531E
;  EDI must equal 0x47531E
0x475A3E:  JMP EDI               ; -> POPAL + validate body at 0x47531F
```

**Gate 3** at `0x476018` (protects the key-table init function):
```asm
;  ESI = 0x23AA3E + 0x23AA3E + 1 = 0x47547D
;  EDI must equal 0x47547D
0x4745FA:  JMP EDI               ; -> POPAL + key-init body at 0x47547E
```

The success paths all do `JMP EDI`, which lands at `POPAL` (restoring the registers saved by the wrapper's `PUSHAL`) followed by the real function body.

## Step 4: Finding the OEP

After the EP's HWID chain passes, the stub reaches:

```asm
0x474591:  POPAD
0x474592:  SUB ESP, 0xC
0x474595:  MOV DWORD PTR [0x46F034], 1    ; HWID flag = valid
0x47459F:  JMP 0x4014CD
```

At `0x4014CD`:
```asm
0x4014CD:  CALL 0x40D4A0         ; __security_init_cookie
0x4014D2:  ADD ESP, 0xC
0x4014D5:  JMP 0x401180          ; __tmainCRTStartup
```

So `0x4014CD` is the effective OEP (the MinGW CRT entry stub).

## Step 5: Understanding the Two-Phase CRT Startup

A critical discovery: `__tmainCRTStartup` at `0x401180` reads the HWID flag and branches on it:

```asm
0x4011E1:  MOV ESI, [0x46F034]   ; read flag
0x4011E7:  TEST ESI, ESI
0x4011E9:  JNE 0x401470          ; flag=1 -> phase-2 path
```

The protector splits CRT initialization into two phases:
- **Phase 1** (flag=0): runs the first pass of CRT init
- **Phase 2** (flag=1): calls `GetStartupInfoA`, continues startup, calls `WinMain`

Phase 1 ends at `0x4014C0` which jumps to `0x474591` (the `POPAD + flag=1 + JMP 0x4014CD` stub), re-entering `__tmainCRTStartup` for phase 2.

The `PUSHAD` at the entry point and `POPAD` at `0x474591` are matched: they save and restore the register state across the entire CRT phase-1 execution. Any EP patch must preserve this `PUSHAD`/`POPAD` pairing or the stack will be corrupted.

## Step 6: Stolen Functions

The protector "steals" several functions from `.text` by replacing their first instruction with a `JMP` into `.xdata`. Each wrapper does `PUSHAL`, runs a CPUID chain, checks the HWID gate, and on success does `POPAL` followed by the real function body.

| Address | Original function | Wrapper | Gate | Body |
|---------|------------------|---------|------|------|
| `0x42133C` | WndProc init (WM_CREATE) | `0x47649C` | Gate 1 | `0x475672` (string assign) |
| `0x44A430` | String assign helper | `0x4760BE` | Gate 1 | `0x475672` (string assign) |
| `0x421578` | Key validate | `0x475998` | Gate 2 | `0x47531F` (check key) |

A fourth stolen function at `0x47547E` is the key-table initializer, protected by Gate 3.

## Step 7: Key Validation Logic

The WndProc dispatches `WM_COMMAND` from the "Validate" button:

```asm
0x421297:  CALL 0x44A430          ; string assign (get input text)
0x42129C:  ...
0x4212A1:  CALL 0x421578          ; validate(key) -> AL
0x4212A6:  TEST AL, AL
0x4212A8:  JE   show_incorrect
           PUSH 0x468031          ; "Correct"
           JMP  show_message
show_incorrect:
           PUSH 0x468048          ; "Incorrect"
```

The validate function at `0x47531F` (body in `.xdata`) performs string comparison against a key generated at startup.

## Step 8: Key Generation (LCG)

The key-table init function at `0x47547E` generates a 32-character key using:

```
seed = time(0) ^ GetTickCount()
for i in 0..31:
    seed = (seed * 0x19660D + 0x3C6EF35F) mod 2^32    // LCG
    key[i] = charset[seed % 62] ^ 0x5A
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
```

The XOR-encoded key is stored at `0x466B80` (32 bytes).

## Step 9: The Patch

Five patches are applied. The key insight is to let the CPUID wrapper chains run (they set up the register and stack state that the function bodies expect) but force the final comparison to always pass by hardcoding the correct `EDI` value.

**Patch 1: EP bypass** (file offset `0x6F000`, 19 bytes)

Replace the CPUID chain with a minimal stub that preserves the two-phase CRT startup:
```asm
PUSHAD                              ; match POPAD at 0x474591
SUB ESP, 0xC
MOV DWORD PTR [0x46F034], 0         ; flag=0 (phase-1 first)
JMP 0x4014ED                        ; OEP
```

**Patch 2: Gate 1 bypass** (file offset `0x0700C9`, 7 bytes)
```asm
MOV EDI, 0x475671                   ; expected value
JMP 0x475AEF                        ; -> JMP EDI -> POPAL + body
```

**Patch 3: Gate 2 bypass** (file offset `0x070018`, 7 bytes)
```asm
MOV EDI, 0x47531E
JMP 0x475A3E
```

**Patch 4: Gate 3 bypass** (file offset `0x070618`, 10 bytes)
```asm
MOV EDI, 0x47547D
JMP 0x4745FA
```

**Patch 5: Validate always true** (file offset `0x020978`, 5 bytes)
```asm
MOV AL, 1
RET
NOP
NOP
```

## Step 10: Keygen

The key can be read directly from the running patched process memory:

```python
python keygen.py read <PID>
```

This reads 32 bytes from `0x466B80`, XORs each byte with `0x5A`, and prints the valid key.

Alternatively, given a seed value:
```python
python keygen.py generate 0xDEADBEEF
```

## Lessons Learned

1. **Do not skip the wrapper chains.** Early attempts to redirect stolen functions directly to their bodies (bypassing the `PUSHAL`/`POPAL` pair) crashed because the register state was wrong. The correct approach is to let the wrappers run and only patch the final HWID comparison.

2. **Preserve the PUSHAD/POPAD pairing.** The protector splits CRT startup into two phases using a `PUSHAD` at the EP and a matching `POPAD` deep inside the CRT code. Removing `PUSHAD` from the EP patch caused stack corruption when phase-1 tried to `POPAD`.

3. **Multiple gates.** The protector uses three separate HWID gates for different stolen functions. Missing even one (gate 3, which protects key-table init) causes the program to show "Invalid HWID" at runtime even though the EP check was bypassed.

4. **The flag controls CRT branching.** The global at `0x46F034` is not just a marker. `__tmainCRTStartup` reads it to decide which initialization path to take. Setting it to the wrong value at the wrong time breaks the startup sequence.

## Files

- `crack.py` - Patcher script (5 patches, produces `crackme3_cracked.exe`)
- `keygen.py` - Key reader/generator
