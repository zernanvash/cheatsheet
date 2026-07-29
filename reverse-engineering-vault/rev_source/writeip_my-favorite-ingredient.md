# My favorite ingredient

## Challenge Overview
Name: My favorite ingredient
Author: intrigus
Category: Reversing
Description: Just one ingredient that makes the magic.
Flag format: GPNCTF{}
Objective: Reverse the provided checker and recover the valid flag.

## Files Provided
- `my-favorite-ingredient.tar.gz`

## Solution Plan
1. Extract the provided archive and inspect the binary.
2. Reverse the flag-checking logic and identify the matrix transformation.
3. Decode the obfuscated matrix and target, then solve the 64×64 linear system modulo 256 to recover the flag.

## Code (Exploit Script)
```python
#!/usr/bin/env python3

from pathlib import Path
from z3 import BitVec, Solver, sat

BIN = Path("./my-favorite-ingredient").read_bytes()

MATRIX_OFFSET = 0x2170
TARGET_OFFSET = 0x3170

SIZE = 64

def decode_byte(b):
    return (13 * ((~b) & 0xff) + 223) & 0xff

matrix_raw = BIN[MATRIX_OFFSET:MATRIX_OFFSET + SIZE * SIZE]
target_raw = BIN[TARGET_OFFSET:TARGET_OFFSET + SIZE]

matrix = [decode_byte(b) for b in matrix_raw]
target = [decode_byte(b) for b in target_raw]

flag = [BitVec(f"flag_{i}", 8) for i in range(SIZE)]

s = Solver()

for i in range(SIZE):
    acc = 0
    for j in range(SIZE):
        acc += matrix[i * SIZE + j] * flag[j]
    s.add((acc & 0xff) == target[i])

for c in flag:
    s.add(c >= 0x20)
    s.add(c <= 0x7e)

assert s.check() == sat

model = s.model()
out = bytes([model[c].as_long() for c in flag])

print(out.decode())
```

## Flag
```txt
GPNCTF{juSt_ON3_0N5TRUCTi0ns_Is_aL1_YOu_NeEd_M4y8e1239794FKFNdh}
```

## Notes
The binary used AVX-512 instructions, so it could not be executed directly in the analysis environment because it crashed with `Illegal instruction`. The solution was done statically by reimplementing the checker logic.
