# luv4u Crackme Writeup

Challenge_URL: https://crackmes.one/crackme/69889a90fb46458f1ef6cecf

## Overview

luv4u is a Linux x86_64 PIE binary that generates a random 32 character uppercase license key, asks you to enter it, and validates your input. After three wrong attempts it generates a new license. The binary packs multiple anti debug and anti VM layers, a custom S Box crypto pipeline, self modifying code, and a small bytecode VM. I solved it with an LD_PRELOAD hook library that captures the generated license from rand() outputs, patches out an unsolvable VM checksum condition, and auto injects the correct key.

## Tools Used

Ghidra 11.x for static analysis, GCC for building the hook library, a Linux host (CachyOS) for testing.

## Static Analysis

### Finding main

The binary is stripped. I started at the entry point and traced into `__libc_start_main` to find main at offset 0x1014e0.

### Function Discovery

I identified and renamed about 15 functions through cross references and behavioral analysis.

The important ones at their ELF virtual addresses (Ghidra image base 0x100000)

- `main` at 0x1014e0
- `generate_license` at 0x1038d0
- `validate_license` at 0x103ba0
- `hash_input` at 0x103990
- `init_sbox_tables` at 0x101a10
- `vm_execute` at 0x102540
- `init_vm_bytecode` at 0x102430
- `anti_debug_vm_check` at 0x101d90
- `self_modify_and_exec` at 0x102100
- `_INIT_0` (constructor) at ~0x101200
- `_INIT_1` (constructor) at ~0x101380

### Anti Debug / Anti Tamper Layers

The binary has three layers of protection that run at different stages.

**Constructor _INIT_0** runs before main. It stores an rdtsc timestamp in a global (used later for a timing check in validate_license). It calls ptrace(TRACEME) and if that fails, reads /proc/self/status to check TracerPid. If a debugger is attached, it exits.

**Constructor _INIT_1** also runs before main. It checks the CPUID hypervisor bit. It calls getenv("LD_PRELOAD") and getenv("LD_DEBUG") and exits if either returns non null. It opens /proc/self/maps and scans every line for the strings "frida", "xposed", "inject", and "hook". It reads /proc/self/exe via readlink and checks for "qemu" or "wine". If any check triggers, it calls _exit(1).

**anti_debug_vm_check** gets called repeatedly during execution (before, during, and after license validation). It calls uname() and checks the kernel release and sysname for "Microsoft", "WSL", and "QEMU". It does an rdtsc timing check around a usleep(100) call to detect single stepping. It reads /sys/class/dmi/id/product_name and checks for "VirtualBox", "VMware", "QEMU", "KVM", "Bochs", and "Xen". It scans /proc/cpuinfo for "hypervisor", "QEMU", "TCG", and "AuthenticAMD Virtual". It checks access() on /.dockerenv and /run/.containerenv.

**self_modify_and_exec** generates x86_64 shellcode at an RWX mprotect'd page (0x12a000) using rdtsc based seeds. It calls srand() internally (which matters for our hook approach later).

### License Generation (generate_license at 0x1038d0)

The function creates a 32 character uppercase key.

1. Compute seed as `getpid() ^ time(NULL) ^ (uint32_t)rdtsc()`
2. Call srand(seed)
3. Generate 32 characters. Each character is `(rand() % 26) + 'A'`
4. Shuffle 16 times. Each shuffle swaps `license[rand() % 32]` with `license[rand() % 32]`

That means generate_license makes exactly 1 srand call followed by 64 rand calls (32 for characters, 32 for 16 swaps of 2 indices each).

I verified the modulo operation in the disassembly. The compiler uses IMUL with the magic constant 0x4ec4ec4f for division by 26 on signed integers. The full assembly sequence `IMUL RDX,RDX,0x4ec4ec4f; SAR RDX,0x23; SUB EDX,ECX; IMUL EDX,EDX,0x1a; SUB EAX,EDX; ADD EAX,0x41` confirms this is standard `rand() % 26 + 'A'` with full int arithmetic.

### S Box Construction (init_sbox_tables at 0x101a10)

The function builds a 256x256 S Box (65536 bytes) at 0x119000 and its inverse at 0x109000. The seed data at file offset 0x5210 is the identity sequence (0x00, 0x01, ..., 0xFF). The formula becomes `sbox[row][col] = col ^ row ^ ((col + row) & 0xFF)`. This produces a degenerate S Box where row 0 maps everything to 0. The S Box turns out to be irrelevant for the keygen because both sides of the comparison hash the same string.

### Hash Function (hash_input at 0x103990)

A custom sponge style hash function. Takes an arbitrary length string, outputs 32 bytes.

1. Initialize a 32 byte buffer with 0x5A
2. Run 8 rounds. Each round has an absorption phase that processes each input byte through triple S Box lookups, XORs, and cross position mixing. Then a diffusion phase mixes all 32 positions using S Box lookups with offset dependent keys.

### Validation (validate_license at 0x103ba0)

This is where it gets interesting. I spent a lot of time here figuring out why correct licenses were being rejected.

The function hashes both inputs, then builds a 128 byte working buffer containing the two 32 byte hashes plus 64 bytes of rdtsc generated random data. It applies forward transforms (S Box lookups with different keying strategies, SIMD byte rotations using ROL 3, and a full buffer reversal). Then it runs a small VM (vm_execute) on 6 channels of 16 bytes each with randomly generated bytecodes. Then it applies inverse transforms to undo the forward step.

The return condition has two parts ANDed together at offset 0x4607.

```
PCMPEQB + horizontal sum -> matching_bytes
SETG AL            ; AL = 1 if matching_bytes > 27
; ...
XOR of 6 vm_execute results
CMP EAX, 0x42
SETZ DL            ; DL = 1 if XOR == 0x42
; ...
AND EAX, EDX       ; final result = both must be true
```

**The hash comparison** compares the ORIGINAL hashes at [RSP+0x20] and [RSP+0x40], not the transformed working copies. So the forward and inverse transforms are a red herring for the hash match. If you enter the correct license, both hashes are identical and all 32 bytes match, passing the >27 threshold easily.

**The VM checksum** is the problem. init_vm_bytecode seeds the bytecodes with `srand(channel * -0x21524111 ^ param2 ^ rdtsc())` followed by 512 rand() calls for shuffling. Since rdtsc varies every execution, the bytecodes are effectively random. The VM (24 opcodes including XOR, ADD, rotations, conditional jumps, stack operations, and cross channel recursion) produces a uint32 checksum per channel. The XOR of all 6 checksums must equal 0x42.

With random bytecodes, this is a ~1 in 2^32 probability. It essentially never passes. Even with 662 attempts in automated testing, zero succeeded. The crackme appears to be designed this way intentionally as an additional protection layer.

### The VM Architecture

vm_execute at 0x102540 implements a register machine with an 8 byte register, a 30 entry stack, and 24 opcodes (0x00 through 0x17). Opcodes include XOR between register bytes, ADD, XOR with constant 0xAA, conditional jumps, left and right rotations, bitwise NOT, AND, OR, NEG, stack push/pop, and opcode 0x17 which does recursive cross channel execution ((channel + 1) % 6) with a depth limit of 3. The opcode for each step is determined by an inverse S Box triple lookup combining the current bytecode byte with the current input data byte.

## Solution Strategy

Since the VM checksum condition can not be satisfied reliably, I needed to patch it out. The approach uses LD_PRELOAD to hook library calls and patch the binary in memory.

### Bypassing Anti Debug

I hook these functions to get past all protection layers.

**getenv()** returns NULL for "LD_PRELOAD" and "LD_DEBUG" to hide the hook library from _INIT_1.

**ptrace()** always returns 0 to satisfy _INIT_0's PTRACE_TRACEME check.

**fopen()** returns NULL for "/proc/self/maps" (prevents _INIT_1's string scanning) and "/sys/class/dmi/id/product_name" (prevents anti_debug_vm_check's VM detection).

**access()** returns -1 for "/.dockerenv" and "/run/.containerenv" to prevent container detection.

The library file is named luv4u_support.so, not keygen_hook.so. The original name contained "hook" which _INIT_1 would detect when scanning /proc/self/maps.

### Capturing the License

I hook both srand() and rand() to detect the license generation pattern.

The rand() hook records every return value in a buffer and increments a counter. The srand() hook checks the counter from the previous srand. If it was 64 or 65 (generate_license produces exactly 64 rand calls, but the first license generation has 65 because FUN_001022b0 adds one extra rand() before the next srand), we reconstruct the license.

Reconstruction logic matches the binary exactly. For each of the first 32 rand values compute `(value % 26) + 'A'`. Then apply 16 swaps using pairs of `rand_value % 32` as indices.

### Patching the VM Checksum

A constructor function in the hook library runs before main. It uses dl_iterate_phdr() to find the executable's ASLR base address, then patches the `AND EAX, EDX` instruction at ELF offset 0x4607 to `NOP NOP` (0x90 0x90). This removes the VM checksum requirement so only the hash comparison determines the result.

The constructor calls mprotect() to make the target page writable before patching (the binary's own mprotect_rwx() call happens later in main).

### Auto Injection

The fgets() hook checks if the stream is stdin (using `fileno(stream) == STDIN_FILENO`, not pointer comparison, because the stdin symbol resolves to a different address in the shared library). When a license has been captured, it writes it into the fgets buffer instead of reading from the terminal.

## Running It

```
gcc -shared -fPIC -o luv4u_support.so keygen_hook.c -ldl
LD_PRELOAD=./luv4u_support.so ./luv4u
```

Output looks like this.

```
  [+] Patched VM checksum check (AND EAX,EDX -> NOP NOP)

  ╔══════════════════════════════════════════╗
  ║         luv4u KEYGEN - ACTIVE            ║
  ╠══════════════════════════════════════════╣
  ║  License: VLDJASRQCOXAIKIFYYGRYFHXMGLVQYWP  ║
  ╚══════════════════════════════════════════╝

Welcome to love4u!

Enter your license key there:
==>
[V] The key is correct, welcome to application!
```

I tested it multiple times and it succeeds on every run with a different license each time.

## Bugs I Hit Along the Way

**stdin pointer mismatch.** My first fgets hook compared `stream == stdin` which never matched. The stdin pointer in the shared library resolves to a different address than in the main binary. Using `fileno(stream) == STDIN_FILENO` fixed it.

**Wrong srand counted.** self_modify_and_exec calls FUN_00102090 which calls srand() internally. So there are many srand calls besides generate_license's. My first approach tried counting srand calls (expecting the 8th one to be generate_license) which was fragile and wrong. Switching to rand() count detection (64 or 65 calls between srand calls is unique to generate_license) solved it.

**Library name detected.** Naming the library keygen_hook.so put "hook" in /proc/self/maps, which _INIT_1 scans for. Renaming to luv4u_support.so and blocking /proc/self/maps via the fopen hook fixed both issues.

**First license missed.** FUN_001022b0 calls rand() after generate_license but before the next srand (from self_modify_and_exec). This makes the first license show 65 rand calls instead of 64. Accepting both counts fixed it.

## Files

- `keygen_hook.c` is the complete LD_PRELOAD hook source (anti debug bypass, license capture, VM checksum patch, auto injection)
- `keygen.py` is a standalone Python reimplementation of the crypto pipeline (glibc PRNG, S Box construction, hash function, license generation from seed)
