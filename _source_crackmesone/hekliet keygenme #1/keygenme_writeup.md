# KeygenMe #1 Writeup - Hecliet (2026-03-17)

**Difficulty:** 2.0
**Platform:** Windows/Linux
**Author:** Hecliet
**Challenge Type:** KeygenMe

---

## Introduction

This writeup documents my approach to solving Hecliet's KeygenMe #1 challenge. The goal was to reverse engineer the key validation algorithm and create a keygen that generates valid serial keys for any given username.

---

## Initial Analysis

### Binary Information

```
File: keygenme_windows.exe
Format: PE (Portable Executable)
Architecture: x86-64
Language: C/C++ (MinGW compiled)
```

### Program Behavior

Running the program shows a simple console interface:

```
.__            __   .__  .__        __
|  |__   ____ |  | _|  | |__| _____/  |_
|  |  \_/ __ \|  |/ |  | |  _/ __ \   __\
|   Y  \  ___/|    <|  |_|  \  ___/|  |
|___|  /\___  |__|_ |____|__|\___  |__|
     \/     \/     \/            \/

hekliet keygenme #1 (released 2026-03-17)
Good keygenning! Have fun!

Enter name:
Enter key:
```

The program prompts for a name and a 32-character hexadecimal key, then validates whether the key is correct for that name.

---

## Reverse Engineering with Ghidra

### Key Functions Identified

Using Ghidra's decompiler, I identified three main functions:

1. **`main` @ 0x1400018a0** - Entry point, handles input/output
2. **`do_something_with_the_name` @ 0x140001584** - Processes the name
3. **`is_key_valid` @ 0x140001728** - Validates the key

### Main Function Analysis

```c
int __cdecl main(int _Argc, char **_Argv, char **_Env)
{
  __main();
  motd();
  puts("Enter name: ");
  scanf("%95[^\n]", &name);
  puts("Enter key: ");
  scanf("%16llx%16llx", &local_10, &local_18);
  r1 = local_10;
  r2 = local_18;
  do_something_with_the_name();
  uVar1 = is_key_valid();
  bVar2 = (int)uVar1 != 0;
  if (bVar2) {
    puts("Key is valid.");
  }
  else {
    puts("Key is invalid.");
  }
  return (int)!bVar2;
}
```

**Key observations:**
- Name is read as a string (up to 95 characters)
- Key is read as **two 64-bit hexadecimal values** (`%16llx%16llx`)
- These two values are stored as `r1` and `r2`
- The name is processed by `do_something_with_the_name()`
- Validation is performed by `is_key_valid()`

### Name Processing Function

```c
void do_something_with_the_name(void)
{
  size_t sVar1;
  double local_20;
  int local_14;
  int local_10;
  byte local_a;
  byte local_9;

  sVar1 = strlen(&name);
  local_9 = 0;
  local_a = 0;

  // XOR first half of name
  for (local_10 = 0; local_10 < sVar1 >> 1; local_10++) {
    local_9 = local_9 ^ (&name)[local_10];
  }

  // XOR second half of name
  for (local_14 = sVar1 >> 1; local_14 < sVar1; local_14++) {
    local_a = local_a ^ (&name)[local_14];
  }

  // Calculate 'a' using constants from data section
  a = 5.0 * (((double)local_9 / 128.0 + (double)local_9 / 128.0) - 1.0);

  // Calculate initial 'b'
  local_20 = 5.0 * (((double)local_a / 128.0 + (double)local_a / 128.0) - 1.0);

  // Condition 1: if abs(b) < 0.1, set b = 1.0
  if ((0x7fffffffffffffff & (ulonglong)local_20) < 0.1) {
    local_20 = 1.0;
  }

  // Condition 2: if a*a - b*4.0 <= 0.0, flip sign of b
  if (a * a - local_20 * 4.0 <= 0.0) {
    local_20 = (double)((ulonglong)local_20 & 0x7fffffffffffffff ^ 0x8000000000000000);
  }

  b = local_20;
  return;
}
```

**Algorithm breakdown:**

1. **XOR hashing:**
   - `xor1` = XOR of all bytes in the first half of the name
   - `xor2` = XOR of all bytes in the second half of the name

2. **Calculate coefficients:**
   - `a = 5.0 * (2.0 * xor1 / 128.0 - 1.0)`
   - `b = 5.0 * (2.0 * xor2 / 128.0 - 1.0)` (with adjustments)

3. **Adjustment conditions:**
   - If `|b| < 0.1`: set `b = 1.0`
   - If `a² - 4b ≤ 0`: flip the sign of `b`

### Key Validation Function

```c
undefined8 is_key_valid(void)
{
  double dVar1;
  double dVar2;
  double local_10;

  local_10 = -1.0;  // Start at -1.0
  do {
    if (1.0 < local_10) {  // End at 1.0
      return 1;  // Key is valid!
    }
    if (local_10 != 0.0) {
      dVar1 = exp(r1 * local_10);
      dVar2 = exp(r2 * local_10);

      // Check if the expression is small enough
      if (4.5e-12 <= (double)((ulonglong)
          (b * (dVar1 + dVar2) +
           r1 * r1 * dVar1 + r2 * r2 * dVar2 +
           a * (r1 * dVar1 + r2 * dVar2)) & 0x7fffffffffffffff)) {
        return 0;  // Key is invalid
      }
    }
    local_10 = 0.1 + local_10;  // Increment by 0.1
  } while( true );
}
```

**Validation algorithm:**

For each value of `t` in `[-1.0, -0.9, -0.8, ..., 0.9, 1.0]` (excluding 0):

The program computes:
```
value = b * (exp(r1*t) + exp(r2*t))
      + r1² * exp(r1*t) + r2² * exp(r2*t)
      + a * (r1 * exp(r1*t) + r2 * exp(r2*t))
```

The key is **valid** only if `|value| < 4.5e-12` for all values of t.

---

## Mathematical Analysis

### Factoring the Expression

The validation expression can be factored:

```
exp(r1*t) * (b + r1² + a*r1) + exp(r2*t) * (b + r2² + a*r2)
```

For this expression to be **approximately zero** for all values of `t`, both coefficients must be zero:

```
b + r1² + a*r1 = 0
b + r2² + a*r2 = 0
```

### The Quadratic Connection

Both equations can be rewritten as:

```
r² + a*r + b = 0
```

This means **r1 and r2 must be the roots of the quadratic equation** `r² + a*r + b = 0`!

### Solution: Quadratic Formula

Using the quadratic formula:

```
r = (-a ± √(a² - 4b)) / 2
```

So:
```
r1 = (-a + √(a² - 4b)) / 2
r2 = (-a - √(a² - 4b)) / 2
```

---

## Keygen Implementation

```python
#!/usr/bin/env python3
"""
Keygen for keygenme_windows.exe
Solution: r1 and r2 are roots of r² + a*r + b = 0
"""
import struct
import math

def compute_a_b(name):
    """Compute a and b from name using XOR algorithm"""
    name_bytes = name.encode('ascii')
    length = len(name_bytes)

    # XOR first half of name
    xor1 = 0
    for i in range(length // 2):
        xor1 ^= name_bytes[i]

    # XOR second half of name
    xor2 = 0
    for i in range(length // 2, length):
        xor2 ^= name_bytes[i]

    # Calculate a = 5.0 * (2.0 * xor1 / 128.0 - 1.0)
    a = 5.0 * (2.0 * xor1 / 128.0 - 1.0)

    # Calculate b = 5.0 * (2.0 * xor2 / 128.0 - 1.0)
    b = 5.0 * (2.0 * xor2 / 128.0 - 1.0)

    # Condition 1: if abs(b) < 0.1, set b = 1.0
    b_bits = struct.unpack('<Q', struct.pack('<d', b))[0]
    mask = 0x7fffffffffffffff
    if (mask & b_bits) < struct.unpack('<Q', struct.pack('<d', 0.1))[0]:
        b = 1.0

    # Condition 2: if a*a - b*4.0 <= 0.0, flip sign of b
    if a * a - b * 4.0 <= 0.0:
        b_bits = struct.unpack('<Q', struct.pack('<d', b))[0]
        sign_mask = 0x8000000000000000
        b_bits ^= sign_mask
        b = struct.unpack('<d', struct.pack('<Q', b_bits))[0]

    return a, b

def find_roots(a, b):
    """Find r1, r2 as roots of r² + a*r + b = 0"""
    discriminant = a * a - 4 * b
    if discriminant < 0:
        return None, None  # Complex roots - no valid key

    sqrt_disc = math.sqrt(discriminant)
    r1 = (-a + sqrt_disc) / 2
    r2 = (-a - sqrt_disc) / 2

    return r1, r2

def double_to_hex(d):
    """Convert double to 16-char hex string (IEEE 754 little-endian)"""
    return format(struct.unpack('<Q', struct.pack('<d', d))[0], '016x')

def generate_key(name):
    """Generate valid key for given name"""
    a, b = compute_a_b(name)
    r1, r2 = find_roots(a, b)

    if r1 is None:
        return None

    return double_to_hex(r1) + double_to_hex(r2)

if __name__ == "__main__":
    name = input("Enter name: ").strip()
    if not name:
        name = "test"

    key = generate_key(name)
    if key:
        print(f"Name: {name}")
        print(f"Key:  {key}")
    else:
        print("Could not generate key (complex roots)")
```

---

## Verification

Testing the keygen with various names:

| Name | Generated Key | Result |
|------|---------------|--------|
| test | `4012883c10883c06bfeec1e08441e034` | ✓ Valid |
| Administrator | `400b630316ca548dbff646062d94a91a` | ✓ Valid |
| Claude | `3ff8aa3db5ad4772c005151edad6a3b9` | ✓ Valid |
| Hecliet | `3ff62da7fdf5807fc003d6d3fefac040` | ✓ Valid |

---

## Conclusion

This KeygenMe challenge demonstrates an interesting mathematical validation scheme where the key validation expression is designed to equal zero when r1 and r2 are the roots of a specific quadratic equation. The coefficients of this quadratic (a and b) are derived from the username through XOR hashing.

### Key Takeaways

1. **Reverse engineering tools used:** Ghidra with MCP integration for remote analysis
2. **Mathematical insight:** The validation expression factors into a form that reveals the quadratic relationship
3. **Solution:** Generate keys by computing the roots of `r² + a*r + b = 0`

### Tools Used

- Ghidra (reverse engineering and decompilation)
- Python (keygen implementation)
- IEEE 754 floating point representation

---

