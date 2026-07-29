# Writeup: "obfuscated" Crackme

Challenge_URL: https://crackmes.one/crackme/697f81c0e04ca145cd9d13c9

## Overview

The binary is a 64-bit Linux ELF that prompts for a serial number and prints "correct serial number!" or "wrong serial number!". It uses a ptrace-based virtual machine with overlapping instruction encoding (nanomites pattern) to validate the input character by character.

## Tools Used

- Ghidra / r2ghidra for decompilation
- radare2 for disassembly and raw byte inspection
- Custom `LD_PRELOAD` hooks for dynamic tracing (since the binary uses ptrace internally, a standard debugger cannot attach)
- Python scripts for constraint solving (brute-force XOR combinations, carry-propagating ADD solver, BFS for permutation search)

## Initial Analysis

Running `file` and examining imports reveals:
- ELF 64-bit, dynamically linked
- Imports: `fork`, `ptrace`, `waitpid`, `raise`, `fgets`, `calloc`, `puts`, `printf`, `exit`
- Strings: "enter serial number >", "correct serial number!", "wrong serial number!"

This immediately suggests a parent/child ptrace architecture. The presence of `raise` is notable: it's used by some handlers to generate signals that terminate validation early (a trap for wrong characters).

## Architecture

Decompiling `main` reveals the following structure:

1. Read up to 64 bytes of input via `fgets`
2. Allocate a dispatch table (256 entries × 8 bytes) mapping byte values to code addresses
3. `fork()`: the child calls `ptrace(PTRACE_TRACEME)` then executes an illegal instruction (`ud2`)
4. The parent enters a loop:
   - For each input character, look up its handler address in the dispatch table
   - `PTRACE_GETREGS`: read child's register state
   - `PTRACE_SETREGS`: set child's RIP to the handler address
   - `PTRACE_CONT`: resume the child
   - `waitpid`: child hits `ud2` at the end of the handler, generating SIGILL (signal 4)
   - If the wait status indicates SIGILL (0x400), continue to next character
   - If SIGTRAP (0x500), print "correct serial number!" and exit
   - Otherwise, print "wrong serial number!" and exit

The key insight is that the parent rewrites the child's instruction pointer before each resume. The child never executes sequentially: it's a pure dispatch VM where each "instruction" is selected by the corresponding input character.

## Overcoming Anti-Debug

Since the child calls `PTRACE_TRACEME` and the parent is the tracer, attaching GDB or any ptrace-based debugger to either process fails. The solution is to use `LD_PRELOAD` to interpose on the `ptrace` and `waitpid` libc calls in the parent process. This lets us observe:

- What handler address (RIP) is set for each character
- The register state (r12, r13, r14) before and after each handler executes
- What signal the child raises after each handler

Example hook (simplified):
```c
long ptrace(enum __ptrace_request request, ...) {
    long (*real_ptrace)(...) = dlsym(RTLD_NEXT, "ptrace");
    // ... forward call ...
    if (request == PTRACE_SETREGS) {
        struct user_regs_struct *regs = (struct user_regs_struct *)data;
        fprintf(stderr, "SET RIP=0x%llx R12=0x%08x R13=0x%08x R14=0x%08x\n",
                regs->rip, (uint32_t)regs->r12, (uint32_t)regs->r13, (uint32_t)regs->r14);
    }
    return ret;
}
```

By feeding repeated single characters (e.g., `0000000000`) and observing r12d toggling between 0 and a fixed value, I confirmed that each character XORs a constant into r12d. Running the same test for all printable ASCII characters mapped each one to its handler and its register effect.

## Decoding the Overlapping Instructions

The disassembler shows nonsense at many handler entry points because of a deliberate anti-disassembly trick. The pattern is:

```asm
cmp rbx, rax      ; 48 39 c3
je  +3            ; 74 03
jne +1            ; 75 01
<junk byte>       ; overlaps with the real instruction
<real instruction> ; e.g., 41 81 c6 XX XX XX XX (add r14d, imm32)
```

Since `je +3` and `jne +1` together always jump to the same target (one of them is always taken), the "junk byte" is never executed. But linear disassemblers see it as part of the instruction stream and produce garbage. The fix is to read the raw bytes at the actual execution offset (after the jump target) and decode manually.

For example, at handler 0x1343:
```
Raw bytes: 48 39 c3 74 03 75 01 0b 41 81 c6 b0 00 00 00 0f 0b
```
The `0b` at offset +7 is the junk byte. Real execution starts at offset +8: `41 81 c6 b0 00 00 00` = `add r14d, 0xb0`, followed by `0f 0b` = `ud2`.

I identified all hidden `add r14d` instructions by scanning the handler region for the byte pattern `41 81 c6` (the opcode for `add r14d, imm32`), which revealed 8 distinct ADD handlers that the disassembler had missed.

## Finding the Success Condition

Disassembling handler 0x1401 reveals the success check:
```asm
0x1401: cmp r12d, 0xdeadbeef
0x1408: jne 0x141d          ; → hlt (crash)
0x140a: cmp r13d, 0x42318657
0x1411: jne 0x141d
0x1413: cmp r14d, 0xcafebabe
0x141a: jne 0x141d
0x141c: int3                ; SIGTRAP → "correct serial number!"
0x141d: hlt                 ; SIGSEGV → "wrong serial number!"
```

This gives us three concrete targets to satisfy simultaneously.

## Handler Classification

The handler region (0x11b9–0x14a8) contains ~25 distinct handlers, each ending with `ud2`. Many use overlapping instruction encoding to hide their true behavior: a `cmp rbx,rax; je +3; jne +1` sequence causes the disassembler to show garbage, but execution always falls through to the real instruction.

After decoding the overlapping bytes, handlers fall into these categories:

### XOR Handlers (modify r12d)

Each performs two XOR operations on `r12d` with immediate constants, producing a net XOR value:

| Handler | Net XOR      | Characters |
|---------|-------------|------------|
| 0x11ca  | 0x87e78e82  | `I`        |
| 0x1220  | 0x1c71472b  | `#`, `3`, `~` |
| 0x126a  | 0x90bfe692  | `Y`, `m`, `t` |
| 0x1299  | 0xfdcc2231  | `<`        |
| 0x13a8  | 0x9a379ae0  | `9`        |
| 0x1421  | 0x0117131f  | `"`, `(`, `0`, `?`, `\`, `c` |
| 0x1434  | 0xd58491d4  | `1`, `M`, `O` |
| 0x1447  | 0x756cfd53  | `u`, `y`   |

### ADD Handlers (modify r14d)

Each adds a constant to `r14d`:

| Handler | ADD Value    | Characters |
|---------|-------------|------------|
| 0x11b9  | 0x0000000e  | `)`, `:`, `v` |
| 0x1233  | 0x0a000000  | `$`, `A`, `q`, `}` |
| 0x1247  | 0xc0000000  | `Q`        |
| 0x12bf  | 0x000e0000  | `f`        |
| 0x12ea  | 0x0000b000  | `5`, `F`, `X` |
| 0x1343  | 0x000000b0  | ` `, `+`   |
| 0x13d2  | 0x00f00000  | `8`, `e`   |
| 0x145a  | 0x00000a00  | `,`, `R`, `W`, `i` |

### Stack Handlers (for r13d)

| Handler | Operation | Characters |
|---------|-----------|------------|
| 0x146e  | PUSH 1–8 onto stack | `*`, `h`, `x`, `z` |
| 0x11f3  | POP 8 values → r13d (nibble packing) | `d` |
| 0x1281/0x132c/0x12fe | swap positions 4,6 | `!`, `J`, `K`, `` ` ``, `p`, `%`, `U`, `b`, `g` |
| 0x1315  | swap positions 6,7 | `'`, `4`, `G`, `[`, `s`, `\|` |
| 0x1357  | swap positions 3,6 | `P`, `S`, `w` |
| 0x136e  | swap positions 3,7 | `=`, `L` |
| 0x1389  | swap positions 0,3 | `@`, `a`, `{` |
| 0x13bb  | swap positions 4,7 | `-`, `T` |

### CHECK Handler (0x1401)

Characters: `H`, `j`, `r`

Compares all three registers against target values:
```asm
cmp r12d, 0xdeadbeef
jne fail
cmp r13d, 0x42318657
jne fail
cmp r14d, 0xcafebabe
jne fail
int3            ; triggers SIGTRAP → success
```

### Other Handlers

- **NOP**: `]`, `^`, `;`: no register effect
- **CRASH**: `&`, `N` (infinite recursion), `2`, `>` (raise SIGBUS), `Z`, `k` (null deref)

## Solving the Three Constraints

### r12d = 0xdeadbeef

**Approach:** Each XOR handler toggles a fixed bitmask into r12d. Using the same handler twice cancels out (A XOR A = 0), so each handler is either used once or not at all. With only 8 distinct XOR values, there are only 2^8 = 256 possible combinations to check.

I confirmed the XOR behavior dynamically by feeding repeated characters (e.g., `00000000`) through the LD_PRELOAD hook and observing r12d alternate between 0x00000000 and 0x0117131f: proving that `0` XORs 0x0117131f into r12d each time it executes.

A Python script iterates all 256 bitmask combinations:
```python
for mask in range(256):
    val = 0
    for i in range(8):
        if mask & (1 << i):
            val ^= xor_list[i]
    if val == 0xdeadbeef:
        # found it
```

Result:
```
0x87e78e82 ^ 0x1c71472b ^ 0x90bfe692 ^ 0xd58491d4 = 0xdeadbeef
```

Solution: use handlers 0x11ca, 0x1220, 0x126a, 0x1434 → characters `I`, `#`, `Y`, `1` (order irrelevant since XOR is commutative).

### r14d = 0xcafebabe

**Approach:** Initially I only found 5 ADD handlers (the ones with `add r14d, imm8` or obvious `add r14d, imm32` patterns). No solution existed with just those 5. I then performed a byte-pattern scan of the entire handler region searching for the opcode `41 81 c6` (`add r14d, imm32`), which revealed 3 additional handlers hidden behind the overlapping-jump anti-disassembly trick. With all 8 handlers identified, the problem becomes: find non-negative integers n1..n8 such that:

```
n1×0x0e + n2×0x0a000000 + n3×0xc0000000 + n4×0x0e0000 +
n5×0xb000 + n6×0xb0 + n7×0xf00000 + n8×0x0a00 ≡ 0xcafebabe (mod 2^32)
```

I solved this with a carry-propagating approach, working byte-by-byte from LSB to MSB. Each byte of the target constrains which multipliers are valid, and carries propagate upward:

```python
# Byte 0: (n1×0x0e + n6×0xb0) mod 256 = 0xbe, carry0 = sum>>8
# Byte 1: (n5×0xb0 + n8×0x0a + carry0) mod 256 = 0xba, carry1 = sum>>8
# Byte 2: (n4×0x0e + n7×0xf0 + carry1) mod 256 = 0xfe, carry2 = sum>>8
# Byte 3: (n2×0x0a + n3×0xc0 + carry2) mod 256 = 0xca
```

The unique minimal solution is n1=n2=n3=n4=n5=n6=n7=n8=1: each ADD handler used exactly once:
```
0x0e + 0x0a000000 + 0xc0000000 + 0x0e0000 + 0xb000 + 0xb0 + 0xf00000 + 0x0a00 = 0xcafebabe
```

One character from each ADD group, in any order.

### r13d = 0x42318657

**Approach:** The PUSH handler (0x146e) pushes the constants 1 through 8 onto the x86 stack. The POP handler (0x11f3) pops 8 values and packs them into r13d as nibbles:

```asm
mov rbx, 8
loop:
  dec rbx              ; rbx = 7, 6, 5, ..., 0
  pop rax              ; pop next value
  mov rcx, rbx
  shl rcx, 2           ; shift amount = rbx * 4
  shl rax, cl          ; shift value into position
  or  r13d, eax        ; merge into result
  cmp rbx, 0
  je  done
  jmp loop
```

This produces: `r13d = pop[0]<<28 | pop[1]<<24 | ... | pop[7]<<0`

With no swaps, the default result is 0x12345678 (values popped in order 1,2,3,...,8).

The target 0x42318657 has nibbles `[4,2,3,1,8,6,5,7]`, meaning we need to rearrange the stack so that position 0 holds 4, position 3 holds 1, position 4 holds 8, position 6 holds 5, and position 7 holds 7.

The SWAP handlers operate on specific stack offsets (rsp+0x18, rsp+0x20, rsp+0x30, rsp+0x38), which after the PUSH correspond to stack positions 3, 4, 6, and 7. I modeled each swap as a permutation and ran BFS from the initial state `[1,2,3,4,5,6,7,8]` to the target `[4,2,3,1,8,6,5,7]`:

```python
swaps = ['swap46', 'swap76', 'swap63', 'swap73', 'swap30', 'swap47', 'rot374']
# BFS over permutation space
queue = deque([(start_state, [])])
visited = {start_state}
# ... standard BFS ...
```

The shortest solution is 3 swaps:
1. swap46 (positions 4↔6): `[1,2,3,4,7,6,5,8]`
2. swap30 (positions 0↔3): `[4,2,3,1,7,6,5,8]`
3. swap47 (positions 4↔7): `[4,2,3,1,8,6,5,7]`

Sequence: PUSH, swap46, swap30, swap47, POP → e.g. `*!@-d`

I verified this dynamically with the LD_PRELOAD hook: feeding `*!@-dH` and observing r13d = 0x42318657 at the CHECK handler.

## Final Serial Construction

Concatenate all parts (XOR and ADD in any order, stack ops in sequence, CHECK last):

```
I#Y1v$Qf5+8i*!@-dH
```

Verification:
```
$ echo 'I#Y1v$Qf5+8i*!@-dH' | ./obfuscated
enter serial number > correct serial number!
```

## Keygen

The included `keygen.c` generates random valid serials by:
1. Picking one character from each required XOR group (shuffled)
2. Picking one character from each ADD group (shuffled)
3. Emitting the fixed-order stack sequence with random character choices
4. Optionally inserting NOP characters
5. Appending a CHECK character

Compile: `gcc -o keygen keygen.c`

Example output:
```
$ ./keygen
OIt~Qi 5f})8zg@-d]H
$ ./keygen
1#It QvXfie$zb{TdH
```

Both produce "correct serial number!" when fed to the binary.
