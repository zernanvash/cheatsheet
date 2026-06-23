# Monster CrackMe 1.0 (MCM) Writeup

child validation logic in FUN_140004d00
parent debugger logic in FUN_140005490

the binary launches a child process and the parent debugs it

flow:
parent process --> child process
child executes int3
parent catches breakpoint and reads child thread context
if child rax == 0, parent writes rax = 0x9f2d38b17c6a4e5f
parent adjusts rip to skip the trap when needed
child resumes with injected value

the child computes part of the decode mask from anti debug state

-decode model:
child side anti debug constant:
0xb3e192f8a4d5c6b7

parent forced value:
0x9f2d38b17c6a4e5f

effective mask:
mask = 0xb3e192f8a4d5c6b7 xor 0x9f2d38b17c6a4e5f

vm encrypted blob bytes are stack initialized in FUN_140001000, then copied into DAT_140035310

encrypted blob:
48d9ed8a1dff9a7bb0d1e57c15f7927388e9ddbb2dcfaa4b80e1d5b325c7a243

- key generation model:
the program builds
    a fixed 4096 entry matrix from an lcg with seed 0xdeadbeef
    a 64 byte input matrix from password bytes with zero padding

for each n in 0..63:
edx = sum over 4 rows of dot products
edx = edx mod 1024
key[n] = (data[n*4] - (edx & 0xff)) mod 256
decoded[n] = blob[n] xor mask[n & 7] xor key[n]

vm loader reads 11 byte instructions:
byte 0 --> opcode
byte 1 --> reg1
byte 2 --> reg2
bytes 3..10 --> little endian imm64

for a valid password the first decoded instruction starts with success opcode:
ins[0] op=0xf0 imm=1
ins[1] op=0xff

solving:
constrain only the first instruction bytes that must match success semantics, creating modular linear constraints on password bytes
z3 solves the system for shortest printable input length
lenght 2
>>> y5
