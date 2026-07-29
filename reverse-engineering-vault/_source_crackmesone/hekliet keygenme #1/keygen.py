#!/usr/bin/env python3
"""
Keygen for keygenme_windows.exe
The key validation uses: exp(r1*t)*(b + r1^2 + a*r1) + exp(r2*t)*(b + r2^2 + a*r2)
This equals 0 when r1 and r2 are roots of: r^2 + a*r + b = 0
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

    # Calculate initial b = 5.0 * (2.0 * xor2 / 128.0 - 1.0)
    b = 5.0 * (2.0 * xor2 / 128.0 - 1.0)

    # Apply condition: if abs(b) < 0.1, set b = 1.0
    b_bits = struct.unpack('<Q', struct.pack('<d', b))[0]
    mask = 0x7fffffffffffffff
    if (mask & b_bits) < struct.unpack('<Q', struct.pack('<d', 0.1))[0]:
        b = 1.0

    # Apply condition: if a*a - b*4.0 <= 0.0, flip sign of b
    if a * a - b * 4.0 <= 0.0:
        b_bits = struct.unpack('<Q', struct.pack('<d', b))[0]
        sign_mask = 0x8000000000000000
        b_bits ^= sign_mask
        b = struct.unpack('<d', struct.pack('<Q', b_bits))[0]

    return a, b

def find_roots(a, b):
    """Find r1, r2 as roots of r^2 + a*r + b = 0"""
    discriminant = a * a - 4 * b
    if discriminant < 0:
        return None, None

    sqrt_disc = math.sqrt(discriminant)
    r1 = (-a + sqrt_disc) / 2
    r2 = (-a - sqrt_disc) / 2

    return r1, r2

def double_to_hex(d):
    """Convert double to 16-char hex string"""
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
