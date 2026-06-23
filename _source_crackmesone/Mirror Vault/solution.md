# Mirror Vault Writeup

from the serial parsing code at 0x140001500 the serial must be exactly 32 bytes:
bytes  0-7:  "DONCRIS{"  (fixed)
bytes  8-30: 23 unknown printable ascii characters
byte   31:   "}"  (fixed)

the 32 bytes are then packed two ways for the two vms:
stage1 --> 4 x uint64 little-endian
stage2 --> 8 x uint32 little-endian

all four data blobs (two pools, two programs) are stored encrypted.
the decryption loop at 0x140001c00 is a splitmix64-based stream cipher

rax = start_seed
for each entry:
    rax = (rax + 0x9e3779b97f4a7c15) & 0xffffffffffffffff
    keystream = splitmix64(rax)
    *ptr ^= keystream
    if rax == end_seed: break

where splitmix64 is
x ^= x >> 30
x  = (x * 0xbf58476d1ce4e5b9) & mask64
x ^= x >> 27
x  = (x * 0x94d049bb133111eb) & mask64
x ^= x >> 31

the golden ratio constant 0x9e3779b97f4a7c15 is the 64-bit version used in
xxhash, wyrand, and similar mixers. using it as the accumulator increment
means the rax counter visits all 2^64 values before cycling.

the stage2 pool uses a 32-bit variant.
instead of XORing the full 64-bit keystream it XORs (lower32 ^ upper32)
of the splitmix64 output against each 32-bit pool entry:

# from asm at 0x140001c04:
# mov %rdx,%r14
# shr $0x20,%r14      --> r14 = upper32
# xor %r14d,%edx      --> edx = lower32 ^ upper32
key32 = (ks & 0xffffffff) ^ ((ks >> 32) & 0xffffffff)



stage1 pool     (44 x uint64)  0x14007c820  start=0xa55a5aa55cc33cf0  end=0xd6e346873d90908c
stage1 program  (47 x uint64)  0x14007c6a0  start=pool1_end           end=0xe3129f959c3d5867
stage2 pool     (88 x uint32)  0x14007c540  start=0x6d6972726f725632  end=0xd07b4a36310cfd6a
stage2 program  (115 x uint64) 0x14007c1a0  start=pool2_end           end=0xe366f88a5f82bad9

start=0x6d6972726f725632 decodes as "mirrorV2" (little endian ascii).
stage1 pool end feeds directly into the stage1 program start, and similarly for stage2..
doing this chains the decryption keys so neither blob can be decrypted in isolation


stage1 vm:
the stage1 vm at 0x140001580 operates on 8 x uint64 registers.
the serial packs as 4 x uint64 into regs[0..3]. regs[4..7] start as zero. regs[8..15]
are loaded from kExpectedTextHash[] at 0x14007c980. pool entries fill regs[16..59].

instructions are packed as a uint64:
bits  0-7:  opcode
bits  8-15: field f1 (dest register)
bits 16-23: f2
bits 24-31: f3
bits 32-39: f4
bits 40-47: f5 (rotation amount)
bits 48-55: f6 (rotation amount)
bits 56-63: f7 (pool index)

opcodes decoded:
0/1  xor:    reg[f1] ^= pool[f7]
2    add:    reg[f1] += pool[f7]
3    mix:    4-register ARX block (modifies reg[f1..f4])
4    check:  result_or |= (reg[f1] ^ pool[f7])
5    mix:    different 4-register rotation block
0xff halt

the check opcode accumulates a bitwise OR. stage1 passes when result_or == 0,
which means every check must satisfy reg[fi] == pool[f7]. the check targets
are pool1[40..43]:

pool1[40] = 0x069305795dddc4c3
pool1[41] = 0x2afa3378ade28817
pool1[42] = 0xf856eabd4db79358
pool1[43] = 0x3726c2fae01d77c7



before stage2 starts, run_stage2 at 0x140001a80 derives 8 x uint32 xor keys
from the stage1 result and a fingerprint. the fingerprint hash processes the
4 stage1 target values through an fnv-like loop:

r8  = 0x9e3779b97f4a7c15  (GOLDEN)
r9  = 0x6a09e667f3bcc909  (SHA-256 initial constant)
ecx = 9                   (rotation, increases by 11 each round)

for each of the 4 values v:
    v   = rotl64(v, ecx)
    v  ^= r9
    v   = (v * 0x100000001b3) & mask64   # FNV prime
    v  ^= r8
    r8 += GOLDEN
    r9  = v

fingerprint = r9

using s0..s3 for pool1[40..43] and fp for the fingerprint, the 8 keys are:

key[0] = (s0 ^ fp)            & 0xffffffff
key[1] = ((fp + s1) >> 32)    & 0xffffffff
key[2] = (rotl64(fp,13) ^ s2) & 0xffffffff
key[3] = ((rotl64(fp,29)+s3)  >> 32) & 0xffffffff
key[4] = (s0 + s2)            & 0xffffffff
key[5] = ((s1 ^ s3) >> 32)    & 0xffffffff
key[6] = (0xa5a5f00dd00df00d ^ fp)    & 0xffffffff
key[7] = ((0x3c6ef372fe94f82b + fp) >> 32) & 0xffffffff

!! these formulas use s0..s3 which are pool1[40..43], constants from the binary.
the keys are therefore fully concrete regardless of the actual serial.
the two vms are structurally independent.
so stage2 does not depend on stage1 outputs at runtime, only on the hardcoded targets.


stage2 vm
the stage2 vm at 0x140001a80 operates on 16 x uint32 registers.
the serial packs as 8 x uint32 into regs[0..7]. regs[8..15] initialize as
key[i] ^ pool2[80+i] (an extra mixing step before the vm starts)

vm stack layout (rsp-rel):
0x00-0x1f  keys[0..7]
0x20-0x3f  regs[0..7]   <-- the serial, modified by the vm
0x40-0x5f  extra[0..7]  <-- regs[8..15]
0x60-0x1bf pool2[0..87]
0x1c0+     program

instructions use the same 8-byte packed format as stage1.

opcodes decoded:
0/1  xor:    reg[f1] ^= pool2[f7]
2    add:    reg[f1] += pool2[f7]
3    mix:    complex mix, writes to reg[f1] and reg[f4]
4    mix:    complex mix, writes to reg[f1] and reg[f3]
5    perm:   4-register swap/rotate (4 sub-cases via f7&3)
6    check:  result_or |= (reg[f1] ^ pool2[f7])
7    mix:    4-register ARX using extra registers (regs 8-15)
0xff halt

opcode 3 in detail (here i got stuck xd):

pool_a = pool2[24+f7]
pool_b = pool2[f7]
pool_c = pool2[40 + (f7&7)]
key_a  = key[(f7+f6) & 7]
key_b  = key[(f5^f6) & 7]

eax = pool_a + reg[f2] + key_a
eax = eax ^ rotl32(reg[f1] + pool_b, f5)
eax = eax + reg[f3]
reg[f1] = eax                          # writes f1

edx = key_b ^ pool_c
reg[f4] ^= rotl32(eax ^ edx, f6)      # writes f4  (NOT f3 - i misread in asm)

that last line looked like it modified f3 when i was reading the asm without paying good attention. :(
because both rbx (f3) and r8 (f4) appear nearby. the actual instruction is
xor [rsp + r8*4 + 0x20], eax where r8 holds f4.

the 115-instruction program runs through 24 rounds of mixing (opcodes 3/4/5/7
interleaved) then applies 8 final xor/add transformations (instructions
98-105) followed by 8 check instructions (instructions 106-113):

CHECK reg[0] ^ pool2[72]  (target 0x972ed016)
CHECK reg[1] ^ pool2[73]  (target 0x80612adf)
CHECK reg[2] ^ pool2[74]  (target 0xc3e8df7d)
CHECK reg[3] ^ pool2[75]  (target 0xb2ea64e8)
CHECK reg[4] ^ pool2[76]  (target 0x469908df)
CHECK reg[5] ^ pool2[77]  (target 0xac896adb)
CHECK reg[6] ^ pool2[78]  (target 0x94ebf061)
CHECK reg[7] ^ pool2[79]  (target 0x1b0bfaf3)


the solver:
stage2 vm contains only addition, xor, and rotation. no data-dependent branches.
perfect for a smt solver :-o

8 x uint32 as z3 BitVec(32) variables, run all 115
instructions symbolically, and add the constraint result_or == 0.
also constrain all unknown serial bytes to printable ascii.

since stage2 alone uniquely determines the serial, stage1 constraints are not needed.


------------------------------------------------------------------------------------------------------------------------


Serial: DONCRIS{v1rtu4l_m4zes_x0r_b17s!}
