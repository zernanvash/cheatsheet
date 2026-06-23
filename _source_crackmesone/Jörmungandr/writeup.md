# jormungandr Crackme Writeup

Challenge_URL: https://crackmes.one/crackme/6a1f32972b3df128c1df5d7a

## Summary

The visible serial `1331D66091E9E2E5` is a decoy. It prints `DONE`, then starts
a delayed crash thread. The real path is gated by a polymorphic ECC VM, a
JIT-compiled MBA predicate, and a second `.ouro` payload decrypt check.

Validated real serial:

```text
60D5AF5B1D5F45E0
```

Recovered real success hash:

```text
0x469CF364
```

No patching is required for the solve.

## Files

- `jormungandr.exe`
  - SHA-256: `d77e3c617f9051af15421811abe19666e79fc4de6cad22b9a14dc1a8a41c715f`
- `dummy_target.exe`
  - SHA-256: `b28d257a2877ceaed438150490a8fb3b29eda44549133988e8a39640b6292ab1`

Both files are Windows x86-64 PE console binaries compiled with MSVC. The main
program expects:

```text
jormungandr.exe <PID|ProcessName> <TargetString> <Serial>
```

The dummy target plants this string in memory:

```text
ouroboros_goat
```

## Dynamic Resolver

The binary resolves modules and exports through DJB2 hashes XORed with
`0x1337BEEF`.

Important resolver functions:

```text
resolve_module_by_hash  0x14000A6A0
resolve_export_by_hash  0x14000A708
djb2_hash_ascii         0x14000A860
djb2_hash_wide_lower    0x14000A878
```

Examples:

```text
0x065C9557 ^ 0x1337BEEF = djb2("printf")
0x6C3F4ABE ^ 0x1337BEEF = djb2("CreateThread")
0x197EB6A5 ^ 0x1337BEEF = djb2("NtDelayExecution")
0x8D39A4AB ^ 0x1337BEEF = djb2("NtGetContextThread")
0xC303428D ^ 0x1337BEEF = djb2("NtQueryInformationProcess")
```

## Parent Check

`main_crackme` calls `sub_1400096A0` at `0x140009A14` before VM or serial
validation. If it returns zero, execution prints:

```text
0xBAD01A -> Access Denied
```

`sub_1400096A0` resolves `NtQueryInformationProcess`, queries
`ProcessBasicInformation`, and reads the inherited parent PID. It then resolves
the Toolhelp/process APIs:

```text
CreateToolhelp32Snapshot
Process32FirstW
Process32NextW
VirtualAlloc
VirtualFree
OpenProcess
DuplicateHandle
```

It walks the process snapshot to locate the parent PID, copies the parent image
name into a local UTF-16 buffer, lowercases it, and hashes it with
`djb2_hash_wide_lower`. The allow-list constants are:

```text
0xBC4E8398
0x3FC2001F
0x485E9A92
0x00A026C1
0xBE46BA91
```

The practical bypass is to run the binary from a normal launcher instead of a
debugger or custom loader. The static analysis bypass point is the `test eax,
eax` at `0x140009A19`, after `sub_1400096A0`; forcing the nonzero path skips the
access-denied branch. I did not patch this for the final solve.

## Decoy Serial

The obvious check parses `argv[3]` as hex and compares it with:

```text
pow(2, 0x7E51, 2^64 - 59)
```

That value is:

```text
1331D66091E9E2E5
```

At `0x140009DDB`, this branch prints:

```text
0x1337 -> DONE
```

Then it calls `start_decoy_crash_thread` at `0x140009654`. The thread entry is
`decoy_delayed_crash_thread` at `0x1400093F8`:

```c
NtDelayExecution(FALSE, -300000000);
*(uint32_t *)0 = 0xDEADBEEF;
```

So `1331D66091E9E2E5` is not a valid solution.

## Anti-Debug and SMC

`sub_14000926C` checks debug registers. It resolves `NtGetContextThread`, asks
for context flags `0x100010`, and inspects the debug-register slots in the
returned context. If any watched debug register is nonzero, it sets
`dword_14001E4E0`.

`sub_14000ADE4` starts the guardian thread `sub_14000AC20`. The guardian repeats
the `NtGetContextThread` debug-register check and compares a live timing/CRC
value against the sampled value from setup. On mismatch it marks the shared
state as failed. This is why I avoided live debugger single-stepping and used
static extraction plus Unicorn harnesses for deterministic helper code.

The rolling SMC/JIT path is exception-handler driven. `sub_14000BF9C` handles
`STATUS_SINGLE_STEP` (`0x80000004`). Inside the protected JIT window it decrypts
the next instruction window, re-encrypts the previous one, mutates the rolling
key, and updates the trapped RIP in the exception context. On real success it
also applies the protected-state toggle used later for the success hash.

## VM Key Recovery

The VM bytecode decodes to:

```text
push 0x0ACE6D66
push 9
push 2
push 0
op 0x72
op 0xFF
```

Opcode `0x72` calls `ecc_scalar_multiply_vmop` at `0x14000B148`. Running the
original helper under Unicorn with scalar `0x0ACE6D66` and point `(2, 9, 0)`
produced:

```text
X    = A0D7AF5B1D5F45E0
Y    = 5D0973E7B7EA94BB
flag = 0
```

The VM key used by the JIT gate is therefore:

```text
A0D7AF5B1D5F45E0
```

## Modular Division

The field modulus is:

```text
p = 2^64 - 59 = 0xFFFFFFFFFFFFFFC5
```

`sub_14000B260` is modular addition without overflow:

```c
add_mod(a, b, p):
    a %= p
    b %= p
    if a >= p - b:
        return a - (p - b)
    return a + b
```

`mul_mod_2_64_minus_59` at `0x14000B290` is double-and-add multiplication:

```c
mul_mod(a, b, p):
    result = 0
    a %= p
    while b != 0:
        if b & 1:
            result = add_mod(result, a, p)
        a = add_mod(a, a, p)
        b >>= 1
    return result
```

`sub_14000B2F4` is square-and-multiply exponentiation. The point-add/double
routine at `0x14000AEA4` recovers division by computing the denominator inverse
as `den^(p-2) mod p`. Since `p` is prime, Fermat's little theorem gives:

```text
num / den mod p = num * pow_mod(den, p - 2, p) mod p
```

This is the modular division needed to reproduce the ECC VM result.

## Real Serial Gate

For non-decoy serials, `main_crackme` calls:

```c
run_real_serial_jit(parsed_serial, vm_key)
```

at `0x140009E79`. Failure starts the same delayed crash thread. Success toggles
the protected state and enters the process-memory wipe path.

The JIT body generated by `build_real_serial_jit` at `0x14000BDE8` implements:

```text
x = serial XOR vm_key
((x XOR 0x75A55AA512345678)
 + (x AND 0xECC8411076543210)
 - (x OR  0xDEADBEEFCAFEBABE)) mod 2^64
 == 0x096F79BB547359BBA
```

This MBA predicate has multiple satisfying high bits, so it is not enough by
itself. The `.ouro` runner adds a second constraint. `main_crackme` first
encrypts `.ouro` with:

```c
(uint32_t)vm_key ^ 0x55AA55AA
```

Then `sub_14000A48C` decrypts it with:

```c
(uint32_t)serial ^ 0x55AA55AA
```

The payload is valid only when:

```text
(uint32_t)serial == (uint32_t)vm_key
```

With the recovered VM key, the low 32 bits must be:

```text
serial low32 = 1D5F45E0
```

Solving the MBA predicate with this low-32 constraint gives valid real
candidates. The first validated one is:

```text
60D5AF5B1D5F45E0
```

## Payload Validation

The `.ouro` payload resolves:

```text
NtQueryVirtualMemory
NtReadVirtualMemory
NtWriteVirtualMemory
NtProtectVirtualMemory
```

It converts the target string to UTF-16, walks committed target memory, reads
chunks, searches for ASCII and UTF-16 copies of the target, and writes zeroes
over matches.

Wine on this host is not a reliable final validator: `jormungandr.exe` exits
before argument handling with `0xDEAD` because its dynamic CRT resolver fails to
resolve `printf`. Instead, I validated the decrypted `.ouro` payload in Unicorn
with mocked native syscalls and a fake target process region containing three
ASCII and three UTF-16 copies of `ouroboros_goat`.

Clean harness result:

```text
serial=60D5AF5B1D5F45E0
queries=2 reads=6 writes=6
remaining_ascii_hits=0 remaining_utf16_hits=0
remaining_chunks=0000000000000000000000000000,0000000000000000000000000000,0000000000000000000000000000
```

The six writes are the three ASCII matches and the three UTF-16 matches. This is
the real wipe behavior, not the delayed-crash decoy path.

## Success Hash

After the payload returns, the program decrypts the protected 56-byte state blob
and prints the dword at offset `44`:

```c
sub_14000C1A0(local_state);
hash = local_state.dword_at_44;
sub_14000C1D4(local_state);
printf("0x%X -> DONE\n", hash);
```

The state blob is XOR-protected with the key at `0x14001D040`:

```text
AA 55 AA 55
```

The initial decrypted dword at offset `44` is:

```text
0x55AB4D8B
```

The real-JIT success path toggles it once:

```c
state_dword ^= 0x1337BEEF;
```

Therefore the real success hash is:

```text
0x55AB4D8B ^ 0x1337BEEF = 0x469CF364
```
