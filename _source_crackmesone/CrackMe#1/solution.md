Challenge_URL: https://crackmes.one/crackme/6a00a162d7ff92e1214c008d

iseey0u-re CrackMe#1 Writeup

Challenge Information

Challenge Name: iseey0u-re's CrackMe#1

Platform: Windows x86-64

Difficulty: 2.0

Language: C/C++

Objective

The objective of this crackme was to recover the correct password and analyze the internal validation logic while understanding the anti-debugging mechanisms used by the executable.

Tools Used

Cutter

x64dbg

Hex/XOR analysis

Initial Analysis

The executable was loaded into Cutter for static analysis. The following views were used during the reversing process:

Disassembly View

Graph View

Strings View

Function Analysis

Control Flow Graph

The challenge description contained the following hints:

“things aren't always what they seem”

“Be careful with your debugger”

These hints strongly suggested the use of anti-debugging techniques.

Anti-Debugging Analysis

During static analysis, multiple debugger checks were identified.

Important locations:

0x140001fcc

0x140001ff5

0x140002082

0x1400020de

The executable directly accessed the Process Environment Block (PEB):

mov rax, qword gs:[0x60]

The program then checked debugger-related flags using the following instructions:

cmp byte [rax + 2], 0

cmp byte [rax + 0xbc], 0x70

These instructions determine whether the process is currently being debugged.

XOR Seed Manipulation

The crackme used an XOR-based decoding mechanism.

Two different XOR seeds were identified:

0x5d = 93

0x6d = 109

When the executable detected a debugger, it changed the decoding seed from:

0x5d → 0x6d

This behavior was implemented through instructions such as:

mov byte [var_80h], 0x6d

This intentionally generated an incorrect comparison string while debugging.

Encoded Password Data

The encoded bytes used for password generation were identified near:

0x14000213a

Encoded byte sequence:

3e 2f 3c 3e 36 30 38 2e

The executable later XORed these bytes using the decoding seed.

Password Decoding

Using the normal execution seed:

0x5d

The bytes decode as follows:

3e ^ 5d = 63 = c

2f ^ 5d = 72 = r

3c ^ 5d = 61 = a

3e ^ 5d = 63 = c

36 ^ 5d = 6b = k

30 ^ 5d = 6d = m

38 ^ 5d = 65 = e

2e ^ 5d = 73 = s

Recovered password:

crackmes

Additional Protection Logic

Another protection mechanism was also observed.

The executable inserted additional bytes:

0x14

into the comparison buffer using instructions such as:

mov word [rax + rcx], 0x14

This corrupted the generated comparison string during debugger execution.

Because of this:

execution inside x64dbg often resulted in incorrect validation,

the binary sometimes terminated unexpectedly,

and debugger execution produced misleading behavior.

Runtime Analysis

The executable was tested on:

Windows

x64dbg

Ubuntu using Wine

Observed behavior:

incorrect password → Fail

correct password outside debugger → normal exit

debugger execution → modified validation logic

The anti-debugging logic intentionally altered runtime behavior under debuggers.

Important Functions and Blocks

Anti-Debugging Blocks

0x140001fcc

0x140001ff5

0x140002082

0x1400020de

IsDebuggerPresent Call

0x14000205d

Password Generation Loop

0x140002150 → 0x1400021a1

Password Comparison

0x1400021c5 → 0x1400021d0

Success Block

0x1400021d9

Failure Block

0x1400021e2

Final Password

crackmes

Conclusion

This crackme demonstrated several important reverse engineering concepts:

static disassembly analysis

graph-based control flow tracing

anti-debugging through PEB checks

runtime debugger detection

XOR-based password decoding

conditional branch analysis

debugger-aware execution manipulation

The executable intentionally changed its logic when executed under a debugger, making runtime verification unreliable. However, through static analysis and XOR decoding, the correct password was successfully recovered.

The challenge provided practical experience in:

identifying anti-debugging mechanisms,

analyzing XOR encryption logic,

understanding Windows PEB structures,

and tracing validation logic through assembly code.