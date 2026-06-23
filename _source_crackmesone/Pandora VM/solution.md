# vm_crackme.exe Writeup

Author: Codex

## Result

The crackme accepts one unsigned 64-bit password:

```text
140692903388954
```

Hex:

```text
0x7FF59E87671A
```

## Target Overview

The binary is a 64-bit Windows PE crackme named `vm_crackme.exe`. It prints:

```text
[ABRAMS VM] Enter the password:
```

Then it reads an unsigned 64-bit integer from `std::cin`. The interesting part starts after input is collected: the real password check is not implemented as a normal native comparison. The checker is hidden inside a VM-protected code region.

IDA showed a suspicious RWX section:

```text
.pandora
```

The useful strings were easy to find:

```text
[ABRAMS VM] Enter the password:
[ABRAMS VM] Success
[ABRAMS VM] Wrong!
```

But the success and failure strings are reached through virtualized control flow, so simple xrefs do not immediately reveal the password logic.

## IDA Triage

The native entry path was renamed in IDA as:

```text
0x140001900  main_vm_entry
0x1400082AE  vm_entry_stub
0x14002400E  vm_dispatch_decode_and_jump
```

At a high level, `main_vm_entry` does the normal C++ I/O:

1. Print the prompt.
2. Read the user input as an unsigned 64-bit integer.
3. Enter the VM-protected checker.
4. Print success or failure depending on the VM result.

The function at `0x14002400E` behaved like a VM dispatcher: it decoded virtual instructions and jumped to native handler blocks. Fully lifting the VM would have worked, but it was unnecessary. The faster route was to find the native point where the VM's virtual comparison becomes a real CPU flags update.

## Finding the Decisive Comparison

The useful native helper was found around:

```text
0x14001AFAB
0x14001AFB3
```

This block performs the final comparison effect for the VM. In simplified form, the VM calculates a value derived from the password, transforms it, and saves the resulting flags. The important behavior is:

```text
not value
or  value, high
pushfq
```

The saved flags decide whether the VM takes the success path. For the correct password, the transformed comparison value becomes zero and the CPU Zero Flag is set.

The key comparison value was loaded around:

```text
0x1400259B3
```

The decisive bytecode location observed during the real password check was:

```text
r15 = 0x1400261E3
```

I annotated these addresses in the IDA database:

```text
vm_crackme.exe.i64
```

## Emulation Pass

I wrote a Unicorn-based emulator harness, `emulate_vm_crackme.py`, to run the VM code while hooking imports, memory accesses, and selected VM state. This helped identify which native flag write controlled the success branch.

Forcing the saved flags at `0x14001AFB3` to the success value made the VM print the success message. That confirmed this address was the right choke point.

However, the first emulated candidate key was wrong when tested against the real executable. The reason was that the VM check mixed in process/environment-dependent values, and the emulator's fake import addresses and runtime layout did not exactly match a real Windows process. The emulation was still useful, but it could not be trusted for the final numeric key.

## Real-Process Debugging

To remove the emulator mismatch, I wrote `debug_real_compare.py`, a small Windows debugging script. It launches the original `vm_crackme.exe`, feeds a test input, and places a breakpoint on the decisive native instruction:

```text
0x14001AFB3
```

Because that helper is used more than once by the VM, the debugger filters hits by the VM bytecode pointer:

```text
r15 == image_base + 0x261E3
```

On the decisive hit with input `0`, the real process had:

```text
rbx = 0xffff800a617898e6
r9  = 0x0
```

The VM comparison at that point is equivalent to checking that:

```text
input == (~rbx + 1) mod 2^64
```

So the password is:

```text
(~0xffff800a617898e6 + 1) mod 2^64
= 0x7FF59E87671A
= 140692903388954
```

## Verification

The recovered password was tested directly against the original unpatched binary:

```powershell
@'
140692903388954
'@ | .\vm_crackme.exe
```

Output:

```text
[ABRAMS VM] Enter the password:
Press any key to continue . . .
[ABRAMS VM] Success
```

The `pause` output appears before the success line because of the program's output buffering, but the final result is the success path.

## Takeaways

This crackme is a good example of why VM-protected checks should be approached by looking for semantic choke points instead of immediately trying to lift every opcode. The VM can obscure the control flow, but it still has to eventually express decisions through native state: flags, branches, memory writes, or output calls.

The fastest path was:

1. Identify the native VM dispatcher and protected section.
2. Trace from user input into the VM.
3. Find the native flags write that controls success.
4. Validate the choke point by forcing the success flags.
5. Use a real-process breakpoint to avoid emulator layout artifacts.
6. Derive and verify the final 64-bit key.
