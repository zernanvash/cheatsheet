# PhantomGate v1.0 Writeup By lbx

Challenge_URL: https://crackmes.one/crackme/6a09581717539b5175d122b9

## Overview

The binary asks for a serial in this format:

```text
XXXXX-XXXXX-XXXXX-XXXXX
```

If the serial passes the check, it prints:

```text
[+] Access Granted!  The gate yields.  Well played, Reverser.
```

The final valid serial I obtained is:

```text
4QJCG-P4R7Y-3VMY7-XRWHM
```

## Input Parsing

The main function first checks whether a debugger is present, then reads the user input and passes it to the validation function.

The validation function requires the input length to be greater than `0x16`, and checks for dashes at offsets `5`, `11`, and `17`. Therefore the serial is split into four 5-character groups:

```text
group0-group1-group2-group3
```

Each group is parsed by `sub_1400014C0`. The important part of this function is:

```c
value = value * 25 + index;
```

where `index` is the position of the current uppercase character in this alphabet:

```text
ACDEFGHJKLMNPQRTUVWXY3479
```

So each 5-character group is a base-25 number.

## VM Check

After parsing the four groups, the program builds a small bytecode program and executes it with a stack-based virtual machine.

The first four parsed integers are stored into VM slots `0`, `1`, `2`, and `3`. In normal execution, the anti-debug flag is `0`, so the values are used directly. If a debugger is detected, the low bit of the first parsed dword is flipped.

The VM bytecode then performs arithmetic and bit operations. Reducing the executed instructions gives this formula:

```python
target = 0x02D8EEC79A0331D6

v4 = (n0 * 2654435769) ^ n1
v5 = ror64(v4, 17) + n2
v6 = v5 ^ (n3 * 1818371886)
v7 = v6 ^ 2882400001

valid = v7 == target
```

All operations are done modulo `2^64`.

## Solver

The four parsed group values are constrained to the base-25 range:

```text
0 <= ni <= 25^5 - 1
```

The following Z3 script solves the equation and encodes the numeric values back into the custom alphabet:

```python
from z3 import BitVec, BitVecVal, Solver, ULE, ZeroExt, RotateRight, sat


ALPHABET = "ACDEFGHJKLMNPQRTUVWXY3479"
BASE = len(ALPHABET)
GROUP_LEN = 5
MAX_GROUP_VALUE = BASE**GROUP_LEN - 1


def encode_group(value: int) -> str:
    out = []
    for _ in range(GROUP_LEN):
        value, digit = divmod(value, BASE)
        out.append(ALPHABET[digit])
    return "".join(reversed(out))


parsed = [BitVec(f"p{i}", 32) for i in range(4)]
n = [ZeroExt(32, x) for x in parsed]

s = Solver()
for x in parsed:
    s.add(ULE(x, MAX_GROUP_VALUE))

expr = RotateRight((n[0] * BitVecVal(2654435769, 64)) ^ n[1], 17)
expr = expr + n[2]
expr = expr ^ (n[3] * BitVecVal(1818371886, 64))
expr = expr ^ BitVecVal(2882400001, 64)
s.add(expr == BitVecVal(0x02D8EEC79A0331D6, 64))

assert s.check() == sat
m = s.model()
groups = [m[x].as_long() for x in parsed]
serial = "-".join(encode_group(x) for x in groups)

print(groups)
print(serial)
```

One satisfying model is:

```text
[8801280, 5040595, 8475523, 7652035]
```

Encoding these values gives:

```text
4QJCG-P4R7Y-3VMY7-XRWHM
```

## Verification

Running the binary with this serial confirms the result:

```text
PhantomGate v1.0 -- Reverse Engineering Challenge
Enter serial (XXXXX-XXXXX-XXXXX-XXXXX):
[+] Access Granted!  The gate yields.  Well played, Reverser.
```

The constraint is not necessarily unique, so other valid serials may also exist.
