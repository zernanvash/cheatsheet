## Tooling & Environment

**OS**: Windows 10 Virtual Machine

**Static Analysis**: Ghidra and IDA

**Dynamic Analysis**: x64dbg

**Hex Editing**: HxD

**Automation**: Python 3 (z3-solver)

 

## Defeating the Anti-Disassembly Traps (Opaque Predicates)

The author utilized a classic x86 variable-length instruction exploit to desynchronize static analysis tools. The pattern consisted of two complementary conditional jumps

(e.g., `JO` and `JNO`) targeting the exact same destination, followed immediately by a rogue multi-byte opcode (such as `E8` for `CALL` or `E9` for

`JMP`).


**assembly**

0040115C | 70 03 | jo 141161

0040115E | 71 01 | jno 141161

00401160 | E9    |(Fake JMP Opcode)

00401161 | C7 45 | (Start of real code: MOV DWORD PTR...)


Because the CPU evaluates the jumps dynamically, execution is mathematically forced to bypass the E9 byte. However, Ghidra's linear sweep attempts to parse the dead space, consuming the E9 and the subsequent four bytes of actual code to form a massive, fabricated JMP instruction.
To resolve this, First I manually changed some bytes then after finding the pattern I made a Python script (patcher.py) to scan the memory boundaries for the exact byte signatures of these traps and overwrite the rogue opcodes with 0x90 (NOP). This forced the disassembler to drop the fake references and perfectly realign the legitimate instructions.


## Bypassing the Dynamic Anti-Debug Trap:

Once the static view was restored, the core verification function (sub_401150) became visible. It revealed a highly aggressive anti-debugging trap leveraging the PEB.

**Disassembly**

dword_406018 ^= NtCurrentPeb()->BeingDebugged;

Prior to evaluating user input, the program XORs the target memory hashes against the BeingDebugged flag located at FS:[0x30] + 0x2. If the binary is run inside a visible debugger, this flag evaluates to 1, silently corrupting the target hashes and guaranteeing a validation failure even if the correct input is provided.

As, I statically solved this , I didn’t had to bypass the anti-debugger.

 

## Constraint

Solving via Z3 SMT. The core logic mandates a 49-character input string that must satisfy 54 separate mathematical equations. Attempting to reverse this algebraically is inefficient.

I extracted the 54 target DWORDs directly from the .data section. I then mapped the C pseudo-code constraints into a Python script leveraging the z3-solver library (solver.py). By constraining the 49 input bytes to printable ASCII ranges and feeding the equations into the solver engine, the exact string required to satisfy the system was generated.

 

**Execution was verified dynamically by passing the string via the command line and getting output: You are correct, your flag is FUSec{Ch1ll1ng_w1th_Ant1-D1s4ss3mbly_t3chn1qu3_83f52144}**