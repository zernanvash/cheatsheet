import struct
from z3 import BitVec, BitVecVal, RotateLeft, Solver, sat, Extract, ZeroExt


# xor (key = 0x13)
def deobf(data, key=0x13):
    return bytes([b ^ key for b in data])


# blob at 0x140005050
BLOB = b"P|wvQavdv`cav``|rarqzprQAVD>"

espresso = deobf(BLOB[8:16])   # "espresso"
arabica  = deobf(BLOB[16:23])  # "arabica"


# brew_hash: custom hash used by check3
# init = 0xC0FFEE42, per byte: h ^= b*0x9E3779B1; h = rol32(h,13); h -= 0x3F001200
def rol32(v, n):
    v &= 0xFFFFFFFF
    return ((v << n) | (v >> (32 - n))) & 0xFFFFFFFF

def brew_hash(data):
    h = 0xC0FFEE42
    for b in data:
        h = (h ^ (b * 0x9E3779B1 & 0xFFFFFFFF)) & 0xFFFFFFFF
        h = rol32(h, 13)
        h = (h - 0x3F001200) & 0xFFFFFFFF
    return h


# block3 ^ val1 ^ val2 ^ val3 == 0xCAFEBABE
# where val1/val2 come from "espresso" (4 bytes each), val3 from "arabica" (4 bytes)
val1 = struct.unpack_from('<I', espresso, 0)[0]
val2 = struct.unpack_from('<I', espresso, 4)[0]
val3 = struct.unpack_from('<I', arabica,  0)[0]
block3 = (0xCAFEBABE ^ val1 ^ val2 ^ val3) & 0xFFFFFFFF


# block1 (check3)
XOR42   = 0xC0FFEE42
TARGET  = 0xDECAF
MASK    = 0xFFFFF
MAGIC   = 0x9E3779B1
SUB_VAL = 0x3F001200

def byte_le(val32, i):
    return ZeroExt(24, Extract(i*8+7, i*8, val32))

def brew_hash_z3(byte_exprs):
    h = BitVecVal(0xC0FFEE42, 32)
    for b in byte_exprs:
        h = h ^ (b * BitVecVal(MAGIC, 32))
        h = RotateLeft(h, 13)
        h = h - BitVecVal(SUB_VAL, 32)
    return h

b1 = BitVec('block1', 32)
b2 = b1 ^ BitVecVal(XOR42, 32)

data_bytes = [byte_le(b1, i) for i in range(4)] + [byte_le(b2, i) for i in range(4)]
h_expr = brew_hash_z3(data_bytes)

s = Solver()
s.add((h_expr & BitVecVal(MASK, 32)) == BitVecVal(TARGET, 32))

assert s.check() == sat, "z3 found no solution"
m = s.model()

b1_val = m[b1].as_long()
b2_val = (b1_val ^ XOR42) & 0xFFFFFFFF

# sanity
h = brew_hash(list(struct.pack('<II', b1_val, b2_val)))
assert (h & MASK) == TARGET, f"hash check failed: 0x{h:08X}"

key  = f"BREW-{b1_val:08X}-{b2_val:08X}-{block3:08X}"
flag = f"CODEBREW{{{b1_val:08X}-{b2_val:08X}-{block3:08X}}}" # it's = to the key

print(f"key:  {key}")
print(f"flag: {flag}")
