#!/usr/bin/env python3
"""
luv4u Crackme Keygen and Crypto Reimplementation

Reimplements the full crypto pipeline of the luv4u crackme to show
complete understanding of the application.

Architecture

  init_sbox_tables() builds a 256x256 S Box from the identity seed (0x00 through 0xFF).
  generate_license() creates a PRNG based 32 char uppercase license.
  The seed is getpid() ^ time(NULL) ^ rdtsc().
  hash_input() is a custom sponge style hash that outputs 32 bytes.
  validate_license() checks two conditions.
    First, hash(user_input) must match hash(license) on more than 27 of 32 bytes.
    Second, the XOR of 6 VM channel checksums must equal 0x42.
    The second condition uses rdtsc seeded random VM bytecodes so it is probabilistic.
    The LD_PRELOAD hook patches this out.

Anti debug layers

  _INIT_0 stores an rdtsc timestamp, calls ptrace(TRACEME), and checks TracerPid.
  _INIT_1 checks the CPUID hypervisor bit, getenv(LD_PRELOAD and LD_DEBUG),
  scans /proc/self/maps for frida, xposed, inject, and hook,
  then readlinks for qemu and wine.
  anti_debug_vm_check() runs uname checks for Microsoft, WSL, and QEMU,
  does rdtsc timing, reads the DMI product name, scans /proc/cpuinfo
  for hypervisor, QEMU, and TCG, and checks for Docker and container files.
  self_modify_and_exec() generates rdtsc seeded shellcode at an RWX page (0x12a000).

Usage

  Standalone (predict license from srand seed)
    python3 keygen.py --seed 0xDEADBEEF

  With the LD_PRELOAD hook (recommended, see keygen_hook.c)
    gcc -shared -fPIC -o luv4u_support.so keygen_hook.c -ldl
    LD_PRELOAD=./luv4u_support.so ./luv4u
"""

import argparse
import ctypes
import struct
import sys


# S Box Construction (reimplements init_sbox_tables at 0x101a10)
#
# The S Box seed data at 0x105210 is just the identity sequence, seed[i] = i.
# The formula becomes sbox[row][col] = col ^ row ^ ((col + row) & 0xFF).

def build_sbox():
    """Build the 256x256 forward S Box (DAT_00119000)."""
    sbox = bytearray(256 * 256)
    for row in range(256):
        for col in range(256):
            sbox[row * 256 + col] = (col ^ row ^ ((col + row) & 0xFF)) & 0xFF
    return sbox


def build_inv_sbox(sbox):
    """Build the inverse S Box (DAT_00109000) from the forward S Box."""
    inv = bytearray(256 * 256)
    for row in range(256):
        for col in range(256):
            # Map the output back to the input column
            out = sbox[row * 256 + col]
            inv[row * 256 + out] = col
    return inv


# Triple S Box lookup helper (used throughout the crackme)
def sbox_lookup3(sbox, val, key):
    """
    The characteristic triple S Box lookup that appears in hash_input,
    validate_license, and init_vm_bytecode.
    """
    step1 = sbox[key + val * 256]
    step2 = sbox[((key ^ 0xAA) & 0xFF) + step1 * 256]
    step3 = sbox[((key * 2) & 0xFE) + step2 * 256]
    return step3


# Hash Function (reimplements hash_input at 0x103990)
def hash_input(s, sbox):
    """
    Custom sponge style hash function.

    Takes an arbitrary length string and produces 32 bytes.

    Initializes a 32 byte buffer with 0x5A, then runs 8 rounds.
    Each round has an absorption phase that processes every input byte
    through triple S Box lookups with XOR and cross position mixing.
    Then a diffusion phase mixes all 32 positions using S Box lookups
    with offset dependent keys. The address dependent offset simplifies
    to (7 + j) % 32.
    """
    buf = bytearray([0x5A] * 32)
    input_bytes = s.encode('ascii') if isinstance(s, str) else s
    length = len(input_bytes)

    for _round in range(8):
        # Absorption
        for i in range(length):
            b = input_bytes[i]
            pos = i & 0x1F  # i % 32

            # Triple S Box lookup on buf[pos] keyed by input byte
            buf[pos] = sbox_lookup3(sbox, buf[pos], b)

            # XOR input byte into the next position
            buf[(pos + 1) & 0x1F] ^= b

            # Feed buf[pos] forward into position pos+2
            c = buf[pos]
            pos2 = (pos + 2) & 0x1F
            buf[pos2] = sbox_lookup3(sbox, buf[pos2], c)

        # Diffusion
        for j in range(32):
            k = buf[(7 + j) & 0x1F]
            buf[j] = sbox_lookup3(sbox, buf[j], k)

    return bytes(buf)


# License Generation (reimplements generate_license at 0x1038d0)
class GlibcRand:
    """
    Exact reimplementation of glibc rand() and srand() (TYPE_3 algorithm).

    Uses a 31 entry state table of signed 32 bit words. SEP is 3 (the distance
    between front and rear pointers). fptr starts at state[3], rptr at state[0].
    Each rand() call computes (*fptr += *rptr) >> 1, then advances both pointers.

    Initialization uses Schrage's method to compute (16807 * x) mod 2147483647
    without overflow. All state values are signed int32_t throughout.
    """
    DEG = 31
    SEP = 3

    @staticmethod
    def _to_i32(x):
        """Convert to signed 32 bit integer (matching C int32_t)."""
        x = x & 0xFFFFFFFF
        return x - 0x100000000 if x >= 0x80000000 else x

    def __init__(self, seed=1):
        self.state = [0] * self.DEG
        self.fptr = 0
        self.rptr = 0
        self.srand(seed)

    def srand(self, seed):
        # Cast seed to signed int32
        self.state[0] = self._to_i32(seed)

        # Initialize remaining state with Schrage's method
        # state[i] = (16807 * state[i_1]) mod 2147483647
        for i in range(1, self.DEG):
            prev = self.state[i - 1]
            hi = prev // 127773   # Python truncates toward negative inf, need toward zero
            if prev < 0 and prev % 127773 != 0:
                hi += 1  # Adjust for C style truncation toward zero
            lo = prev - hi * 127773
            word = 16807 * lo - 2836 * hi
            if word < 0:
                word += 2147483647
            self.state[i] = word

        # Set front and rear pointers
        self.fptr = self.SEP
        self.rptr = 0

        # Warm up with 310 iterations (DEG * 10)
        for _ in range(self.DEG * 10):
            self.rand()

    def rand(self):
        # Add rear pointer into front pointer (signed 32 bit wrap)
        val = self._to_i32(self.state[self.fptr] + self.state[self.rptr])
        self.state[self.fptr] = val

        # Shift right and mask off the sign bit
        result = (val >> 1) & 0x7FFFFFFF

        # Advance both pointers circularly
        self.fptr += 1
        if self.fptr >= self.DEG:
            self.fptr = 0
        self.rptr += 1
        if self.rptr >= self.DEG:
            self.rptr = 0

        return result


def generate_license_from_seed(seed):
    """
    Generate the 32 character license from a given srand seed.

    Calls srand(seed), generates 32 chars as (rand() % 26) + 'A',
    then shuffles 16 times by swapping license[rand()%32] with license[rand()%32].
    """
    rng = GlibcRand(seed)

    # Generate 32 uppercase letters
    license_chars = []
    for _ in range(32):
        r = rng.rand()
        license_chars.append(chr((r % 26) + ord('A')))

    # Shuffle 16 times
    for _ in range(16):
        a = rng.rand() % 32
        b = rng.rand() % 32
        license_chars[a], license_chars[b] = license_chars[b], license_chars[a]

    return ''.join(license_chars)


# Validation Summary (explains validate_license at 0x103ba0)
def validate_license(user_input, license_key, sbox):
    """
    Simplified reimplementation of validate_license.

    The real function hashes both inputs, builds a 128 byte working buffer
    (two 32 byte hashes plus 64 bytes of rdtsc random data), applies forward
    transforms (S Box lookups, SIMD ROL 3, full buffer reversal), runs a VM
    on 6 channels of 16 bytes each (24 opcodes including XOR, ADD, rotations,
    conditional jumps, stack ops, and cross channel recursion), then applies
    inverse transforms to undo the forward step.

    The final comparison uses the ORIGINAL hashes at [RSP+0x20] and [RSP+0x40],
    not the transformed copies. So the forward and inverse transforms do not
    affect the hash match. More than 27 of 32 bytes must match.

    The VM checksum (XOR of all 6 channel results must equal 0x42) uses
    rdtsc seeded random bytecodes, making it effectively random at about
    1 in 2^32. The LD_PRELOAD hook patches this out.
    """
    user_hash = hash_input(user_input, sbox)
    lic_hash = hash_input(license_key, sbox)

    # Count matching bytes
    matches = sum(1 for a, b in zip(user_hash, lic_hash) if a == b)

    print(f"  User hash:    {user_hash.hex()}")
    print(f"  License hash: {lic_hash.hex()}")
    print(f"  Matching bytes: {matches}/32")
    print(f"  Hash match: {'YES' if user_hash == lic_hash else 'NO'}")

    return user_hash == lic_hash


# Seed brute force (for when we know approximate time and PID)
def bruteforce_seed(known_license, time_range, pid, sbox):
    """
    Try to find the srand seed given known parameters.

    The seed is getpid() ^ time(NULL) ^ (uint32_t)rdtsc().
    Since rdtsc is unpredictable we brute force the lower 32 bits.
    In practice use the LD_PRELOAD approach instead.
    """
    target_hash = hash_input(known_license, sbox)

    for t in time_range:
        base = pid ^ t
        # Try a range of rdtsc values (too slow for full 32 bit range)
        for rdtsc_low in range(0, 1000000):
            seed = (base ^ rdtsc_low) & 0xFFFFFFFF
            candidate = generate_license_from_seed(seed)
            if hash_input(candidate, sbox) == target_hash:
                print(f"Found seed: 0x{seed:08x} (time={t}, rdtsc_low={rdtsc_low})")
                print(f"License: {candidate}")
                return seed, candidate
    return None, None


# Main
def main():
    parser = argparse.ArgumentParser(
        description="luv4u Crackme Keygen and Crypto Reimplementation"
    )
    parser.add_argument("--seed", type=lambda x: int(x, 0),
                        help="Generate license from srand seed (hex or dec)")
    parser.add_argument("--verify", nargs=2, metavar=("INPUT", "LICENSE"),
                        help="Verify if INPUT matches LICENSE using our hash")
    parser.add_argument("--hash", type=str,
                        help="Compute hash_input for a given string")
    parser.add_argument("--test-sbox", action="store_true",
                        help="Print S Box samples for verification")
    args = parser.parse_args()

    print("=" * 60)
    print("  luv4u Crackme Keygen and Crypto Reimplementation")
    print("=" * 60)

    # Build crypto tables
    print("\n[*] Building S Box tables...")
    sbox = build_sbox()
    inv_sbox = build_inv_sbox(sbox)
    print(f"    Forward S Box: {len(sbox)} bytes")
    print(f"    Inverse S Box: {len(inv_sbox)} bytes")

    # The S Box is not a permutation per row. Row 0 maps everything to 0 because
    # col ^ 0 ^ (col+0) = 0. This looks like intentional obfuscation. The inverse
    # S Box is best effort and used in validate_license's reverse transforms, but
    # those transforms cancel out anyway.
    non_bijective = sum(1 for r in range(256) if len(set(sbox[r*256:(r+1)*256])) < 256)
    print(f"    Non bijective rows {non_bijective}/256 (expected, S Box is lossy by design)")

    if args.test_sbox:
        print("\n[*] S Box samples (row, col = value)")
        for row in [0, 1, 0x55, 0xAA, 0xFF]:
            vals = [sbox[row * 256 + c] for c in range(16)]
            print(f"    Row 0x{row:02x}  {' '.join(f'{v:02x}' for v in vals)} ...")

    if args.hash:
        h = hash_input(args.hash, sbox)
        print(f"\n[*] hash_input(\"{args.hash}\"):")
        print(f"    {h.hex()}")

    if args.seed is not None:
        print(f"\n[*] Generating license from seed 0x{args.seed:08x}...")
        license_key = generate_license_from_seed(args.seed)
        print(f"    License: {license_key}")
        h = hash_input(license_key, sbox)
        print(f"    Hash:    {h.hex()}")

    if args.verify:
        user_input, license_key = args.verify
        print(f"\n[*] Validating \"{user_input}\" against \"{license_key}\":")
        result = validate_license(user_input, license_key, sbox)
        print(f"    Result: {'VALID' if result else 'INVALID'}")

    if not any([args.seed is not None, args.verify, args.hash, args.test_sbox]):
        print("\n[*] Quick demo:")
        # Demo with a known seed
        demo_seed = 0xCAFEBABE
        license_key = generate_license_from_seed(demo_seed)
        print(f"    Seed:    0x{demo_seed:08x}")
        print(f"    License: {license_key}")

        h = hash_input(license_key, sbox)
        print(f"    Hash:    {h.hex()}")

        print(f"\n    Validation (correct key):")
        validate_license(license_key, license_key, sbox)

        print(f"\n    Validation (wrong key):")
        validate_license("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", license_key, sbox)

        print("""
[*] To use with the actual crackme

    LD_PRELOAD hook (recommended, fully automatic)
      $ gcc -shared -fPIC -o luv4u_support.so keygen_hook.c -ldl
      $ LD_PRELOAD=./luv4u_support.so ./luv4u

      The hook patches the VM checksum check (rdtsc random, never passes),
      captures rand() outputs to reconstruct the license (64 or 65 calls),
      auto injects via fgets() hook, and bypasses all anti debug checks
      (getenv, ptrace, /proc/self/maps, DMI product name, Docker detection).

    Seed prediction (if you know PID + time + rdtsc)
      $ python3 keygen.py --seed <captured_seed>
      Seed = getpid() ^ time(NULL) ^ (uint32_t)rdtsc()
""")


if __name__ == "__main__":
    main()
