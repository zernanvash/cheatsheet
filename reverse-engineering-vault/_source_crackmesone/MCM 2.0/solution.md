# CrackMe "MCM v2.0" — Detailed Writeup

Challenge_URL: https://crackmes.one/crackme/698d9ebd3eb49a23d3417763

## Overview

This is my walkthrough for the MCM v2.0 CrackMe. The binary is a 64-bit Windows PE (`CrackMe.exe`) that employs several advanced protection layers:

1. **Multi-process architecture** — Parent acts as a debugger for a child process
2. **TLS callback anti-debugging** — Environment variable checks, `BeingDebugged` flag, hardware breakpoint detection
3. **Custom RISC-V-like VM** — Instruction virtualization with a custom interpreter
4. **Matrix-based mathematical protection** — 64×64 matrix generated via LCGs, dot-product verification mod 1024
5. **XOR-based bytecode transformation** — VM bytecodes are dynamically XOR'd with keys derived from process ID, debug registers, and the matrix result

I solved this by fully reverse-engineering the protection scheme and patching the final VM result check.

---

## Step 1 — Initial Reconnaissance

I opened `CrackMe.exe` in IDA Pro 9.0. The binary is a 64-bit PE compiled with MSVC.

### Entry Point & main()

The `main` function checks `argc`. If there is a command-line argument, it compares `argv[1]` against the string `"--3a1f9b"`. This is the **child process flag**:

- **No arguments** → call `sub_140011400()` (Parent mode)
- **Argument == "--3a1f9b"** → Child mode (password prompt, VM execution, matrix check)
- **Argument != "--3a1f9b"** → also calls `sub_140011400()` (Parent mode)

So the binary serves as both parent and child. The parent spawns itself with `--3a1f9b` as a debuggee.

### String Search

Searching for strings, I found:
- `"=== MCM v2.0 ===\nEnter Password: "` — the prompt
- `"CreateProcessA"`, `"WaitForDebugEvent"`, `"GetThreadContext"`, `"SetThreadContext"`, `"WriteProcessMemory"`, `"ReadProcessMemory"`, `"ContinueDebugEvent"` — all resolved dynamically via FNV-1a hash lookups at runtime (no direct IAT imports)
- `"KERNEL32.DLL"` — used for module lookup during API resolution
- `"X_TOKEN"` and `"DEADBEEF1337"` — anti-debug environment variable

---

## Step 2 — TLS Anti-Debug Callback

The binary has a TLS callback (`TlsCallback_0`) that runs before `main()`:

```c
if (DLL_PROCESS_ATTACH) {
    // 1. Resolve GetEnvironmentVariableA via FNV-1a hash + PEB walk
    // 2. Check env var "X_TOKEN" == "DEADBEEF1337"
    // 3. If mismatch → ExitProcess(0xDEAD)
    // 4. Check NtCurrentPeb()->BeingDebugged
    // 5. If debugged → ExitProcess(0xDEAD)
    // 6. Additional hardware breakpoint checks via GetThreadContext
}
```

This means any external debugger would be detected. The parent process works around this by setting the `X_TOKEN` environment variable before creating the child, and by being the debugger itself (so it can handle the anti-debug gracefully).

---

## Step 3 — Parent Process Analysis (sub_140011400)

This is a massive function (~8000+ lines of decompiled code). I traced through it step by step.

### API Resolution

All Windows API functions are resolved at runtime using **FNV-1a hashing**:
1. Hash the target API name (case-insensitive variant)
2. Walk the PEB → `InMemoryOrderModuleList` to find `KERNEL32.DLL`
3. Walk the export table, hash each export name, compare with target hash
4. Return the function pointer

The resolved APIs are:
- `GetModuleFileNameA` — get the path to itself
- `CreateProcessA` — spawn the child with `DEBUG_PROCESS` flag
- `WaitForDebugEvent` — main debug event loop
- `GetThreadContext` / `SetThreadContext` — read/modify child's CPU state
- `WriteProcessMemory` / `ReadProcessMemory` — modify child's memory
- `ContinueDebugEvent` — resume child execution

### Debug Event Loop

The parent implements a classic debug loop:

```
CreateProcessA(self_path + " --3a1f9b", DEBUG_PROCESS)
first_bp = true
while WaitForDebugEvent(&event):
    if event == EXCEPTION_DEBUG_EVENT:
        if exception_code == EXCEPTION_BREAKPOINT (0x80000003):
            if first_bp:
                first_bp = false   // skip system breakpoint
                ContinueDebugEvent(DBG_CONTINUE)
                continue
            
            // Handle the int 3 from sub_1400161F0
            GetThreadContext(child_thread)
            
            // 1. Compute PID-dependent value
            P = child_process_id
            t = P ^ 0x5A5
            step1 = ((9 * t) << 32) | t
            step2 = step1 ^ 0x9F2D38B17C6A4E5F
            step3 = step2 ^ 0xF0F0F0F00F0F0F0F
            step4 = 0xEDCBA98765432110 + step3
            r13_value = step4 ^ 0x5A5A5A5A5A5A5A5A
            
            // 2. Write 8 bytes to child's stack (arg_18)
            WriteProcessMemory(child, context.Rcx, &r13_value, 8)
            
            // 3. Check for 0xCC byte at RIP, skip past int 3
            ReadProcessMemory(child, context.Rip, &byte, 1)
            if byte == 0xCC: context.Rip++
            
            // 4. Set debug registers for anti-debug bypass
            context.Dr2 = 0x1337C0DE
            context.Dr3 = 0xDEAD1337
            context.Dr7 |= 0x50
            
            SetThreadContext(child_thread, &context)
            ContinueDebugEvent(DBG_CONTINUE)
```

### The "int 3" Trap — sub_1400161F0

This small function is the communication bridge between parent and child:

```asm
sub_1400161F0:
    nop
    push    rbx
    mov     rbx, 1234h
    add     rbx, rbx        ; rbx = 0x2468 (dummy)
    pop     rbx
    xor     rax, rax         ; rax = 0
    xchg    r8, r8           ; nop
    int     3                ; BREAKPOINT TRAP!
    nop
    mov     rax, [rcx]       ; return *arg (value written by parent)
    add     rax, 0
    retn
```

When executed normally (without a debugger), `int 3` would crash. But since the parent is the debugger:
1. The parent catches the `EXCEPTION_BREAKPOINT`
2. Writes a computed PID-dependent value to the child's stack via `WriteProcessMemory`
3. Sets `DR2 = 0x1337C0DE`, `DR3 = 0xDEAD1337` via `SetThreadContext`
4. Increments RIP to skip past `int 3`
5. The child resumes, reads the written value via `mov rax, [rcx]`, and returns it as `r13`

---

## Step 4 — Child Process Flow

After the parent handles the breakpoint, the child continues execution:

### 4.1 — VM Call 1: GetCurrentProcessId

```c
// Initialize VM context (all registers = 0, PC = 0)
// Bytecodes from sub_14000EFA0: {0x5A5204CF, 0x00351A4F, 0x00C5099A, 0x0000001C}
vm_result_1 = sub_140010020(&bytecodes, &vm_context);  // Returns ProcessId
```

The first VM call returns the current process ID. The bytecodes for this call were initialized by `sub_14000EFA0`.

### 4.2 — Password Input

```
"=== MCM v2.0 ==="
"Enter Password: "
// Read user input into a std::string
```

### 4.3 — Anti-Debug Register Check

```c
// r13 = return value from sub_1400161F0 (set by parent)
// Check DR2 and DR3 (set by parent via SetThreadContext)
if (context.Dr2 == 0x1337C0DE && context.Dr3 == 0xDEAD1337)
    r15 = 0xB3E192F8A4D5C6B7;   // correct value
else
    r15 = 0x0BADF00D;            // wrong value (no debugger help)
```

### 4.4 — Matrix Check (sub_140010A70)

The matrix function:
1. **Generates a 64×64 matrix** via `sub_1400104D0` using a seed
2. The **seed** is computed as **FNV-1a hash** of the 29 bytes of `sub_1400161F0` (0x1400161F0 to 0x14001620C) → seed = **0x412DF8B0**
3. **Converts the password** to a 64-element DWORD vector via `sub_1400107B0` (each byte → one DWORD, padded with zeros)
4. **Computes dot products**: for each row i, `dp[i] = Σ(matrix[i][j] * password[j]) mod 1024`
5. **Returns residuals**: `result[i] = (expected[i] - dp[i]) & 0xFF` as a byte vector

The expected values are stored at `byte_140036C90` (64 DWORDs).

#### Matrix Generation Details (sub_1400104D0)

Each row is generated in 4 chunks of 16 elements. For each chunk:
- Elements 0–14: chain of `val = (26125 * prev - 3233) & 0x3FF` starting from `LOWORD(a2)`
- Element 15: same chain but starting from `LOWORD(LCG(a2))` where `LCG(x) = 1664525*x + 1013904223`
- `a2` advances by 16 LCG steps per chunk

### 4.5 — XOR Bytecode Transformation

After the matrix check, the VM bytecodes are XOR-transformed:

```c
// r10 computation (PID-dependent key)
temp = r13 ^ 0x5A5A5A5A5A5A5A5A;       // undo parent's final XOR
temp = 0x123456789ABCDEF0 + temp;        // cancels parent's addition
                                          // (0x123... + 0xEDCBA... = 0 mod 2^64)
r10 = temp ^ 0xF0F0F0F00F0F0F0F;        // undo parent's mask
r10 ^= ProcessId;                         // XOR with PID

// Result: r10 lower 32 bits = 0x7C6A4BFA (CONSTANT — PID cancels out!)
//         r10 upper 32 bits = 9*(PID^0x5A5) ^ 0x9F2D38B1 (PID-dependent)

// XOR loop: transform 16 bytecode bytes
for (i = 0; i < block_size; i++) {
    r10_byte = (r10 >> ((i & 7) * 8)) & 0xFF;
    r15_byte = (r15 >> ((i & 7) * 8)) & 0xFF;
    matrix_byte = matrix_result[i % 64];
    block[i] ^= r10_byte ^ r15_byte ^ matrix_byte;
}
```

**Key insight**: Since `r10` and `r15` are 64-bit values, the XOR key repeats every 8 bytes:
- Bytes 0–3 and 8–11: use the **constant** lower 32 bits of r10 → **deterministic** regardless of PID
- Bytes 4–7 and 12–15: use the PID-dependent upper 32 bits → **vary per execution**

### 4.6 — VM Call 2: The Final Check

```c
vm_result_2 = sub_140010020(&transformed_block, &vm_context_2);
if (vm_result_2 == 1)
    // SUCCESS — decrypt and display message
else
    // FAIL
```

The comparison is at **VA 0x14001439C**:
```asm
0x14001439C:  cmp  eax, 1
0x14001439F:  jnz  loc_14001460A    ; jump to FAIL
```

### 4.7 — Success Message Decryption

The success message is XOR-encrypted at `xmmword_14000D680` (30 bytes). It's decrypted with a simple loop:
```c
for (i = 0; i < 30; i += 2) {
    decrypted[i]   = (i + 0x46) ^ encrypted[i];
    decrypted[i+1] = (i + 0x47) ^ encrypted[i+1];
}
```
Decrypted message: **`\n[+] SUCCESS! ACCESS GRANTED.\n`**

---

## Step 5 — The VM Interpreter (sub_140010020)

The VM is a custom RISC-V-like interpreter with 32 general-purpose registers (x0–x31) plus a PC register at offset 128. x0 is hardwired to 0 (any write is discarded).

### Instruction Format

Each instruction is 32 bits. The opcode is in bits 6:0.

### Opcode Groups

| Type | Opcodes | Function |
|------|---------|----------|
| I-Type | 0x10, 0x22, 0x4F | ADDI, SLTI, XORI, ORI, ANDI, shifts (funct3 selects) |
| R-Type | 0x55, 0xAA, 0xB2, 0x66, 0xE5, 0x77 | ADD, SUB, AND, OR, XOR, shifts |
| B-Type | (default case) | BEQ, BNE, BLT, BGE, BLTU, BGEU |
| J-Type | (0x7788 dispatch) | JAL |
| System | 0x1C, 0x88, 0x99 | ECALL/EBREAK (exit if rd==0 && imm≤1) |

### VM Exit Conditions

1. **Unknown opcode** → immediate exit, returns `x10`
2. **System instruction** with `rd == 0` and `imm ≤ 1` → exit, returns `x10`
3. **PC out of bounds** (PC + 4 > buffer size) → exit, returns `x10`

The return value is always register **x10** (a0 in RISC-V convention).

---

## Step 6 — The Patch

Since the XOR transformation makes the VM bytecodes partially PID-dependent (upper 32 bits of r10 change with each execution), statically determining the correct password requires solving a complex modular linear system where some instruction bytes are non-deterministic. The CrackMe likely relies on the correct password producing bytecodes where:
- Instruction 0 (bytes 0–3, deterministic) sets x10 = 1
- Instruction 1 (bytes 4–7, PID-dependent) has an unknown opcode → VM exits immediately with x10 = 1

Rather than brute-forcing the password across all possible instruction combinations, I chose to **patch the binary**.

### Patch Location

| Field | Value |
|-------|-------|
| Virtual Address | `0x14001439F` |
| File Offset | `0x1379F` |
| Original Bytes | `0F 85 65 02 00 00` (`jnz +0x265`) |
| Patched Bytes | `90 90 90 90 90 90` (6× NOP) |

This NOPs out the conditional jump after `cmp eax, 1`, so the code always falls through to the success path regardless of the VM return value.

### Applying the Patch

```python
import shutil

src = 'CrackMe.exe'
dst = 'CrackMe_patched.exe'
shutil.copy2(src, dst)

with open(dst, 'r+b') as f:
    f.seek(0x1379F)
    original = f.read(6)
    assert original == b'\x0F\x85\x65\x02\x00\x00', "Unexpected bytes!"
    f.seek(0x1379F)
    f.write(b'\x90\x90\x90\x90\x90\x90')

print("Patch applied!")
```

### Result

```
> echo test | CrackMe_patched.exe
=== MCM v2.0 ===
Enter Password:
[+] SUCCESS! ACCESS GRANTED.
```

Any password triggers the success message.

---

## Summary of Protection Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CrackMe.exe                          │
│                                                         │
│  ┌──────────────┐         ┌──────────────────────────┐  │
│  │ PARENT MODE  │         │      CHILD MODE          │  │
│  │              │ spawns  │ (--3a1f9b)               │  │
│  │ sub_140011400├────────►│                          │  │
│  │              │ DEBUG   │ 1. TLS anti-debug        │  │
│  │ Debug Loop:  │ PROCESS │ 2. VM Call 1 (GetPID)    │  │
│  │  Wait event  │         │ 3. "Enter Password:"     │  │
│  │  Handle int3 │◄────────┤ 4. int 3 trap ──────────►│  │
│  │  Write r13   ├────────►│ 5. r13 = parent value    │  │
│  │  Set DR2/DR3 ├────────►│ 6. r15 = DR2/DR3 check  │  │
│  │  Resume      │         │ 7. Matrix check          │  │
│  │              │         │ 8. XOR transform bytes   │  │
│  │              │         │ 9. VM Call 2             │  │
│  │              │         │ 10. cmp eax, 1 ◄─PATCHED │  │
│  │              │         │ 11. SUCCESS/FAIL         │  │
│  └──────────────┘         └──────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Tools Used

- **IDA Pro 9.0** with Hex-Rays decompiler
- **Python** for patch scripting and matrix analysis
