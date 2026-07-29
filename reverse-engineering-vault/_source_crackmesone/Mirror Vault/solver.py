import struct
from z3 import *

MASK32 = 0xFFFFFFFF
MASK64 = 0xFFFFFFFFFFFFFFFF
GOLDEN = 0x9e3779b97f4a7c15
GOLDEN_HI = 0x9e3779b9  # upper 32 bits
FNV_PRIME = 0x100000001b3


def va_to_file(va):
    if 0x140001000 <= va < 0x140078000:
        return va - 0x140001000 + 0x600
    if 0x14007c000 <= va < 0x14008e000:
        return va - 0x14007c000 + 0x79e00
    raise ValueError(f"unknown VA {hex(va)}")


def splitmix64(x):
    x ^= x >> 30
    x  = (x * 0xbf58476d1ce4e5b9) & MASK64
    x ^= x >> 27
    x  = (x * 0x94d049bb133111eb) & MASK64
    x ^= x >> 31
    return x


def decrypt64(data, start, end):
    out = list(data)
    rax = start
    for i in range(len(out)):
        rax = (rax + GOLDEN) & MASK64
        out[i] ^= splitmix64(rax)
        if rax == end:
            break
    return out


def decrypt32(data, start, end):
    # stage2 pool variant: key = lower32(ks) ^ upper32(ks)
    out = list(data)
    rax = start
    for i in range(len(out)):
        rax = (rax + GOLDEN) & MASK64
        ks = splitmix64(rax)
        out[i] ^= (ks & MASK32) ^ ((ks >> 32) & MASK32)
        if rax == end:
            break
    return out


def rotl64(x, n):
    n &= 63
    return x if n == 0 else ((x << n) | (x >> (64 - n))) & MASK64


def fingerprint(vals):
    # fnv-like hash over the 4 stage1 check targets
    r8  = GOLDEN
    r9  = 0x6a09e667f3bcc909
    ecx = 9
    for v in vals:
        v   = rotl64(v, ecx)
        ecx += 11
        v  ^= r9
        v   = (v * FNV_PRIME) & MASK64
        v  ^= r8
        r8  = (r8 + GOLDEN) & MASK64
        r9  = v
    return r9


with open('doncris_mirror_vault.exe', 'rb') as f:
    raw = f.read()

# stage1 pool --> extract check targets (pool1[40..43])
pool1 = decrypt64(
    [struct.unpack_from('<Q', raw, va_to_file(0x14007c820) + i*8)[0] for i in range(44)],
    0xa55a5aa55cc33cf0, 0xd6e346873d90908c
)
s0, s1, s2, s3 = pool1[40], pool1[41], pool1[42], pool1[43]
fp = fingerprint([s0, s1, s2, s3])

# stage2 xor keys (derived from stage1 targets + fingerprint, all concrete)
key = [
    (s0 ^ fp)                    & MASK32,
    ((fp + s1) >> 32)            & MASK32,
    (rotl64(fp, 13) ^ s2)        & MASK32,
    ((rotl64(fp, 29) + s3) >> 32)& MASK32,
    (s0 + s2)                    & MASK32,
    ((s1 ^ s3) >> 32)            & MASK32,
    (0xa5a5f00dd00df00d ^ fp)    & MASK32,
    ((0x3c6ef372fe94f82b + fp) >> 32) & MASK32,
]

# stage2 pool (88 x uint32) and program (115 x uint64)
pool2 = decrypt32(
    [struct.unpack_from('<I', raw, va_to_file(0x14007c540) + i*4)[0] for i in range(88)],
    0x6d6972726f725632, 0xd07b4a36310cfd6a
)
prog2 = decrypt64(
    [struct.unpack_from('<Q', raw, va_to_file(0x14007c1a0) + i*8)[0] for i in range(115)],
    0xd07b4a36310cfd6a, 0xe366f88a5f82bad9
)

# regs[8..15] = key[i] ^ pool2[80+i]
extra = [(key[i] ^ pool2[80+i]) & MASK32 for i in range(8)]


# stage2 vm

def rotl32_z3(x, n):
    n &= 31
    return x if n == 0 else RotateLeft(x, n)

solver = Solver()
solver.set("timeout", 600000)

# 8 x uint32 symbolic registers (serial packed little-endian)
R = [BitVec(f'R{i}', 32) for i in range(8)]

# fixed serial bytes
solver.add(R[0] == 0x434e4f44)          # "DONC"
solver.add(R[1] == 0x7b534952)          # "RIS{"
solver.add(Extract(31, 24, R[7]) == 0x7d)  # byte 31 = '}'

# printable ascii for the 23 unknown bytes
for ri in range(2, 8):
    for bp in range(4):
        if ri == 7 and bp == 3:
            continue
        b = Extract(bp*8 + 7, bp*8, R[ri])
        solver.add(UGE(b, 0x20))
        solver.add(ULE(b, 0x7e))

# initial register state
regs = list(R) + [BitVecVal(extra[i], 32) for i in range(8)]
P2   = [BitVecVal(v, 32) for v in pool2]
K    = [BitVecVal(k, 32) for k in key]
chk  = BitVecVal(0, 64)

for instr in prog2:
    op = instr & 0xFF
    f1, f2, f3, f4, f5, f6, f7 = [(instr >> (8*(j+1))) & 0xFF for j in range(7)]

    if op == 0xFF:
        break
    elif op in (0, 1):
        regs[f1] = regs[f1] ^ P2[f7]
    elif op == 2:
        regs[f1] = regs[f1] + P2[f7]
    elif op == 3:
        eax = P2[24+f7] + regs[f2] + K[(f7+f6)&7]
        eax = eax ^ rotl32_z3(regs[f1] + P2[f7], f5)
        eax = eax + regs[f3]
        regs[f1] = eax
        regs[f4] = regs[f4] ^ rotl32_z3(eax ^ (K[(f5^f6)&7] ^ P2[40+(f7&7)]), f6)
    elif op == 4:
        eax = rotl32_z3(regs[f2] ^ K[f7&7] ^ P2[48+(f7&0xf)], f5)
        eax = eax + regs[f1] + P2[32+(f7&0xf)]
        regs[f1] = eax
        regs[f3] = regs[f3] ^ rotl32_z3(eax + P2[56+(f7&7)] + regs[f4], f6)
    elif op == 5:
        case = f7 & 3
        a, b, c, d = regs[f1], regs[f2], regs[f3], regs[f4]
        if case == 0:
            regs[f1], regs[f2], regs[f3], regs[f4] = c, d, a, b
        elif case == 1:
            regs[f1], regs[f2], regs[f3] = b, c, a
        elif case == 2:
            regs[f1], regs[f2], regs[f3], regs[f4] = c, a, d, b
        elif case == 3:
            regs[f1] = rotl32_z3(a ^ d, 7)
            regs[f2] = b + c
    elif op == 6:
        chk = chk | ZeroExt(32, regs[f1] ^ P2[f7])
    elif op == 7:
        esi   = rotl32_z3(regs[f2] + P2[80+(f7&7)], f5)
        r13d  = P2[40+(f7&7)] ^ regs[f3]
        regs[f1] = regs[f1] + (esi ^ BitVecVal(GOLDEN_HI, 32))
        r13r  = rotl32_z3(r13d, f6)
        regs[f2] = regs[f2] ^ (K[(f7+3)&7] + r13r)
        esi   = rotl32_z3(esi ^ r13r, 11)
        regs[f3] = regs[f3] + P2[(f7%24)+24]
        regs[f4] = regs[f4] ^ esi

solver.add(chk == 0)

print("solving...")
if solver.check() == sat:
    m = solver.model()
    serial = bytearray(32)
    for i in range(8):
        v = m[R[i]]
        val = v.as_long() if v is not None else ([0x434e4f44, 0x7b534952] + [0]*6)[i]
        for bp in range(4):
            serial[i*4 + bp] = (val >> (bp*8)) & 0xff
    print(f"serial: {bytes(serial).decode()}")
else:
    print("no solution")
